from common import *

signal.signal(signal.SIGINT, lambda a,b: exit())

contest_list = ['weekly-contest-301']
username_list = json.load(open(DIR_CONFIG + '/username.json', 'r'))
print(contest_list)
print(username_list)
query_contests(contest_list, username_list)
print(f'\r{SPACES}')
