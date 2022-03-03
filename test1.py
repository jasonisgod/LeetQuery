
from tkinter import S
import requests

def get_contest(title):
    url = f'https://leetcode.com/contest/api/info/{title}/'
    req = requests.get(url)
    data = req.json()
    data = {'start': data['contest']['start_time'], 'questions': data['questions']}
    return data

def get_history(username):
    url = 'https://leetcode.com/graphql'
    json = {
        'operationName': "getContestRankingData",
        'query': 'query getContestRankingData($username: String!) { userContestRankingHistory(username: $username) { contest { title } ranking } }',
    }
    sess = requests.Session()
    csrf_token = sess.get(url).cookies['csrftoken']
    json.update({'csrfmiddlewaretoken': csrf_token})
    json.update({'variables': {'username': username}})
    req = sess.post(url, json=json, headers=dict(Referer=url))
    # print(req.json())
    data = req.json()['data']['userContestRankingHistory']
    data = [i for i in data if i['ranking'] > 0]
    data = [{'title': i['contest']['title'].lower().replace(" ","-"), 'ranking': i['ranking']} for i in data]
    return data

def get_submissions(title, ranking):
    pagination = (ranking-1) // 25 + 1
    index = (ranking-1) % 25
    url = f'https://leetcode.com/contest/api/ranking/{title}/?pagination={pagination}'
    req = requests.get(url)
    data = req.json()['submissions'][index]
    data = list(data.values())
    data = [{key: i[key] for key in ['question_id', 'date', 'submission_id', 'fail_count']} for i in data]
    return data

def get_time_diff(d1, d2):
    diff = abs(d1 - d2)
    return f'{diff // 3600:02d}:{diff // 60 % 60:02d}:{diff % 60:02d}'

def query(username, title):
    contest = get_contest(title)
    start = contest['start']
    history = get_history(username)
    ranking = [i['ranking'] for i in history if i['title'] == title][0]
    submissions = get_submissions(title, ranking)
    line = [str(title), str(ranking)]
    for s in submissions:
        line += [get_time_diff(s['date'], start)]
    print('\t'.join(line))

query('jasonisgod', 'weekly-contest-272')
query('jasonisgod', 'weekly-contest-273')




# 'operationName': "getContestRankingData",
# 'query': "query getContestRankingData($username: String!) 
# {\n  userContestRanking(username: $username) {\n    attendedContestsCount\n    rating\n    globalRanking\n    __typename\n  }\n  
# userContestRankingHistory(username: $username) {\n    contest {\n      title\n      startTime\n      __typename\n    }\n    rating\n    ranking\n    __typename\n  }\n}\n",

# data = req.json()['data']['data']


# req = requests.post(url, data = data)
# print(req)
# print(req.text)