import requests
import json
import signal

signal.signal(signal.SIGINT, lambda a,b: exit())

DIR = 'files'
PAGE_RANGE = list(range(100,500)) ## + list(range(460,470))
SPACES = " "*100

def my_reqeust(url):
    print(f'\rrequest: {url} ... ', end='')
    res = requests.get(url)
    print(f'code: {res.status_code:3d} ', end='')
    return res

def get_time_diff(d1, d2):
    diff = abs(d1 - d2)
    return f'{diff // 3600:02d}:{diff // 60 % 60:02d}:{diff % 60:02d}'

def get_code(submission_id):
    try:
        url = f'https://leetcode.com/api/submissions/{submission_id}/'
        res = my_reqeust(url)
        json_obj = res.json()
        code = json_obj['code']
        return code
    except Exception as e: print(e)
    return ''

def get_start_time(contest_name):
    url = f'https://leetcode.com/contest/api/info/{contest_name}/'
    res = my_reqeust(url)
    json_obj = res.json()
    return json_obj['contest']['start_time']

def get_questions(contest_name):
    url = f'https://leetcode.com/contest/api/ranking/{contest_name}/?region=global'
    res = my_reqeust(url)
    json_obj = res.json()
    return json_obj['questions']

def get_records(contest_name, username_list):
    records = {}
    user_n = len(username_list)
    for page in PAGE_RANGE:
        if user_n == 0: break
        url = f'https://leetcode.com/contest/api/ranking/{contest_name}/?region=global&pagination={page}'
        res = my_reqeust(url)
        json_obj = res.json()
        for repeat in range(1):
            if user_n == 0: break
            total_rank = json_obj['total_rank']
            for index, obj in enumerate(total_rank):
                if user_n == 0: break
                for username in username_list:
                    if user_n == 0: break
                    if username != obj['username']: continue
                    records[username] = {}
                    records[username]['submissions'] = json_obj['submissions'][index]
                    records[username]['info'] = obj
                    user_n -= 1
                    rank = max(0, int(page * 25 // 100) * 100 - 100)
                    print(f'\rFound in page: {page:3d} rank:{rank:5d}+ user: {username} {SPACES}')
                    # print(f'\r{records[username]["submissions"]}')
    return records

def get_scoreboard(contest_name, username_list, start_time, questions, records):
    scoreboard = []
    for username in username_list:
        if username not in records.keys(): continue
        row = {}
        info = records[username]['info']
        row['rank'] = info['rank']
        row['username'] = username
        row['score'] = info['score']
        row['finish_time'] = get_time_diff(start_time, info['finish_time'])
        for i, question in enumerate(questions):
            row[f'Q{i+1}'] = {}
            question_id_str = str(question['question_id'])
            submissions = records[username]['submissions']
            if question_id_str not in submissions.keys():
                continue
            question = submissions[question_id_str]
            row[f'Q{i+1}'] = {
                'solve_time': get_time_diff(start_time, question['date']),
                'fail_count': question['fail_count'],
                'code': get_code(question['submission_id']),
            }
        # print(row)
        scoreboard.append(row)
    return scoreboard

def query_contest(contest_name, username_list):
    start_time = get_start_time(contest_name)
    questions = get_questions(contest_name)
    records = get_records(contest_name, username_list)
    scoreboard = get_scoreboard(contest_name, username_list, start_time, questions, records)
    return scoreboard

def query_contests(contest_name_list, username_list):
    for contest_name in contest_name_list:
        try:
            print(f'\r{contest_name} {SPACES}')
            scoreboard = query_contest(contest_name, username_list)
            # print(scoreboard)
            for row in scoreboard:
                text = json.dumps(row, indent=4)
                username = row["username"]
                open(f'{DIR}/{contest_name}-{username}.json', 'w').write(text + '\n')
        except Exception as e: print();print(e);print()
    return

def main():
    print(f'\rStart {SPACES}')
    username_list = ['leovincentseles','jackycaelum','qm4zirQ15o','seali','jasonisgod','yoyo6245a','wubinray87']
    # username_list = ['seali']
    contest_name_list = ['biweekly-contest-73']
    query_contests(contest_name_list, username_list)
    print(f'\rFinished {SPACES}')

for i in range(5): main()

# contest_name_list = [f'biweekly-contest-{i}' for i in range(66,71+1)]
# json.dumps(scoreboard, indent=4)
# ['jasonisgod','leovincentseles']
# [f'weekly-contest-{i}' for i in range(269,282+1)]
# [f'biweekly-contest-{i}' for i in range(66,71+1)]