import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

with open('prompts.json') as f:
    prompts = json.load(f)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model_gemini_flash = genai.GenerativeModel('gemini-1.5-flash')

def check_is_valid_code(code: str, language: str) -> bool:
    try:
        prompt = prompts['check_is_valid_code'].format(language, code)
        response = model_gemini_flash.generate_content(
            prompt,
            generation_config = genai.types.GenerationConfig(
                max_output_tokens = 100, # limit on the total number of words generated
                temperature = 0.5, # creativity level of the model ~ controls the randomness of the generated text
                top_p = 0.8, # influences the model to choose the next word based on its probability
                top_k = 30, # considers only the top K most probable words at each step
            )
        )
        return 'true' in response.text.lower()
    except Exception as e:
        return False

def get_complexity_analysis(code: str, language: str) -> dict:
    try:
        if not check_is_valid_code(code, language):
            raise ValueError('Invalid code snippet')
        time_complexity_prompt = prompts['get_time_complexity'].format(language, prompts['complexity_options'], code)
        memory_complexity_prompt = prompts['get_memory_complexity'].format(language, prompts['complexity_options'], code)
        time_complexity = model_gemini_flash.generate_content(
            time_complexity_prompt,
            generation_config = genai.types.GenerationConfig(
                max_output_tokens = 100,
                temperature = 0.8, 
                top_p = 0.8, 
                top_k = 30, 
            )
        ).text
        memory_complexity = model_gemini_flash.generate_content(
            memory_complexity_prompt,
            generation_config = genai.types.GenerationConfig(
                max_output_tokens = 100,
                temperature = 0.5, 
                top_p = 0.8, 
                top_k = 30, 
            )
        ).text
        complexity_description_prompt = prompts['get_description'].format(time_complexity, memory_complexity, code)
        complexity_description = model_gemini_flash.generate_content(
            complexity_description_prompt,
            generation_config = genai.types.GenerationConfig(
                temperature = 0.7, 
                top_p = 0.8, 
                top_k = 30, 
            )
        ).text
        print(f"Time Complexity: {time_complexity}"
              f"\nMemory Complexity: {memory_complexity}"
              f"\nDescription: {complexity_description}")
        return {
            'status': 'success',
            'time': time_complexity,
            'memory': memory_complexity,
            'description': complexity_description
        }
    except Exception as e:
        return {
            'status': 'error',
            'time': None,
            'memory': None,
            'description': str(e)
        }

def main():
    code = '''
            class Solution:
                def maxTotalReward(self, nums: List[int]) -> int:
                    nums.sort()
                    ma = nums[-1]
                    dp = [0] * (ma * 2 + 1)
                    for v in nums:
                        for i in range(v):
                            if dp[i+v] < dp[i] + v:
                                dp[i+v] = dp[i] + v
                    return max(dp)
            nums = [1, 2, 3, 4, 5]
            sol = Solution()
            print(sol.maxTotalReward(nums))
            '''
    print(check_is_valid_code(code, 'python'))
    # print(get_complexity_analysis(code))

if __name__ == '__main__':
    main()