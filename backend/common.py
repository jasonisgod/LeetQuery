import requests, json, signal, sys, os, threading, datetime, time
from flask import Flask, request, render_template
from flask_cors import CORS

DIR_DATA = 'files'
DIR_CONFIG = 'config'
PAGE_RANGE = list(range(1,400+1))
# PAGE_RANGE = list(range(120,130))
SPACES = " "*100
TIME_SLEEP = 60 * 10 # 10 mins
TIME_CONTEST = 60 * 60 * 2 # 2 hrs
THREAD = True

def now(): return datetime.datetime.now()
def t2s(t): return t.strftime("%Y-%m-%d %H:%M:%S")
def s2t(s): return datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")

def log(text):
    ts = t2s(now())
    line = f'[{ts}] {text}'
    print(line)

def my_reqeust(url):
    res = requests.get(url)
    log(f'Request: {url} ({res.status_code}) ')
    return res

def get_all_contests():
    return json.load(open(DIR_CONFIG + '/contest.json', 'r'))

def get_all_users():
    return json.load(open(DIR_CONFIG + '/username.json', 'r'))

def get_time_diff(d1, d2):
    diff = abs(d1 - d2)
    return f'{diff // 3600:02d}:{diff // 60 % 60:02d}:{diff % 60:02d}'

def get_code(json_obj):
    try:
        code = json_obj['code']
        return code
    except Exception as e: print(e)
    return ''

def get_lang(json_obj):
    try:
        lang = json_obj['lang']
        return lang
    except Exception as e: print(e)
    return ''

def get_submission(submission_id):
    try:
        url = f'https://leetcode.com/api/submissions/{submission_id}/'
        res = my_reqeust(url)
        json_obj = res.json()
        return json_obj
    except Exception as e: print(e)
    return ''

def get_start_time(contest):
    url = f'https://leetcode.com/contest/api/info/{contest}/'
    res = my_reqeust(url)
    json_obj = res.json()
    return json_obj['contest']['start_time']

def get_questions(contest):
    url = f'https://leetcode.com/contest/api/ranking/{contest}/?region=global'
    res = my_reqeust(url)
    json_obj = res.json()
    return json_obj['questions']

def get_records(contest, username_list):
    records = {}
    user_n = len(username_list)
    for page in PAGE_RANGE:
        if user_n == 0: break
        url = f'https://leetcode.com/contest/api/ranking/{contest}/?region=global&pagination={page}'
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
                    log(f'Found page:{page} rank:{rank}+ user:{username}')
                    # print(f'\r{records[username]["submissions"]}')
    return records

def get_scoreboard(contest, username_list, start_time, questions, records):
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
            submissions_json = get_submission(question['submission_id'])
            row[f'Q{i+1}'] = {
                'solve_time': get_time_diff(start_time, question['date']),
                'fail_count': question['fail_count'],
                'lang': get_lang(submissions_json),
                'code': get_code(submissions_json)
            }
        # print(row)
        scoreboard.append(row)
    return scoreboard

def query_contest(contest, username_list):
    start_time = get_start_time(contest)
    questions = get_questions(contest)
    records = get_records(contest, username_list)
    scoreboard = get_scoreboard(contest, username_list, start_time, questions, records)
    return scoreboard

def query_contests(contest_list, username_list):
    log('Start Crawling ...')
    log(str(contest_list))
    log(str(username_list))
    for contest in contest_list:
        try:
            log(contest)
            scoreboard = query_contest(contest, username_list)
            # print(scoreboard)
            for row in scoreboard:
                text = json.dumps(row, indent=4)
                username = row["username"]
                open(f'{DIR_DATA}/{contest}-{username}.json', 'w').write(text + '\n')
        except Exception as e: print();print(e);print()
    log('Finished')
    return

def _thread():
    while True:
        cc = get_all_contests()
        now_ = now()
        tmp = [(key, s2t(cc[key])) for key in cc]
        tmp = [key for key,vtime in tmp if now_ > vtime and (now_ - vtime).seconds < TIME_CONTEST]
        if len(tmp) == 1:
            contest_list = [tmp[0]]
            username_list = get_all_users()
            query_contests(contest_list, username_list)
        for i in range(TIME_SLEEP):
            if not THREAD: return
            time.sleep(1)

def get_thread():
    return threading.Thread(target=_thread)

def stop_thread():
    global THREAD
    THREAD = False