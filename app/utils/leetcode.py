import requests


def get_leetcode_user_stats(username: str) -> dict:
    data = {"status": "error"}
    try:
        url = 'https://leetcode.com/graphql'
        query = """
        query getUserStats($username: String!) {
          allQuestionsCount {
            difficulty
            count
          }
          matchedUser(username: $username) {
            username
            githubUrl
            twitterUrl
            linkedinUrl
            profile {
              reputation
              ranking
              userAvatar
              realName
              countryName
              company
              jobTitle
              skillTags
              postViewCount
            }
            contributions {
              points
            }
            submitStatsGlobal {
              acSubmissionNum {
                difficulty
                count
              }
            }
          }
        }
      """
        variables = {"username": username}
        response = requests.post(url,
                                 json={
                                     "query": query,
                                     "variables": variables
                                 })
        if response.json().get(
                "errors") is not None or response.status_code != 200:
            return {"status": "error"}
        data = response.json()["data"]
        total_solved = data["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][
            0]["count"]
        total_questions = data["allQuestionsCount"][0]["count"]
        easy_solved = data["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][
            1]["count"]
        total_easy = data["allQuestionsCount"][1]["count"]
        medium_solved = data["matchedUser"]["submitStatsGlobal"][
            "acSubmissionNum"][2]["count"]
        total_medium = data["allQuestionsCount"][2]["count"]
        hard_solved = data["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][
            3]["count"]
        total_hard = data["allQuestionsCount"][3]["count"]
        ranking = data["matchedUser"]["profile"]["ranking"]
        contribution_points = data["matchedUser"]["contributions"]["points"]
        reputation = data["matchedUser"]["profile"]["reputation"]
        github_url = data["matchedUser"]["githubUrl"]
        twitter_url = data["matchedUser"]["twitterUrl"]
        linkedin_url = data["matchedUser"]["linkedinUrl"]
        userAvatar = data["matchedUser"]["profile"]["userAvatar"]
        realName = data["matchedUser"]["profile"]["realName"]
        countryName = data["matchedUser"]["profile"]["countryName"]
        company = data["matchedUser"]["profile"]["company"]
        jobTitle = data["matchedUser"]["profile"]["jobTitle"]
        skillTags = data["matchedUser"]["profile"]["skillTags"]
        postViewCount = data["matchedUser"]["profile"]["postViewCount"]
        best_lang = __get_leetcode_user_planguages(username)
        data = {
            "status": "success",
            "username": username,
            "totalSolved": total_solved,
            "totalQuestions": total_questions,
            "easySolved": easy_solved,
            "totalEasy": total_easy,
            "mediumSolved": medium_solved,
            "totalMedium": total_medium,
            "hardSolved": hard_solved,
            "totalHard": total_hard,
            "ranking": ranking,
            "contributionPoints": contribution_points,
            "reputation": reputation,
            "githubUrl": github_url,
            "twitterUrl": twitter_url,
            "linkedinUrl": linkedin_url,
            "userAvatar": userAvatar,
            "realName": realName if realName else 'ANONYMOUS',
            "countryName": countryName if countryName else 'UNKNOWN',
            "company": company if company else 'COMPANY',
            "jobTitle": jobTitle if company else 'SWE',
            "skillTags": skillTags if skillTags else [best_lang],
            "postViewCount": postViewCount,
            "bestLanguage": best_lang
        }
    except Exception as e:
        print("Error in get_leetcode_user_stats: ", e)
    finally:
        return data


def __get_leetcode_user_planguages(username):
    url = 'https://leetcode.com/graphql'
    query = """
      query languageStats($username: String!) {
      matchedUser(username: $username) {
          languageProblemCount {
          languageName
          problemsSolved
          }
      }
      }
      """
    variables = {"username": username}
    response = requests.post(
        url, json={"query": query, "variables": variables})
    try:
        if response.json().get(
                "errors") is not None or response.status_code != 200:
            return 'Not Found'
        data = response.json()["data"]["matchedUser"]["languageProblemCount"]
        return max(data, key=lambda x: x['problemsSolved'])['languageName'].strip()
    except Exception as e:
        print(f'Error in get_leetcode_user_planguages: {str(e)}')
        return 'Not Found'


if __name__ == '__main__':
    print(get_leetcode_user_stats('nobodyxxxx'))
