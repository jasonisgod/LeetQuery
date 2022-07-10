from common import *

signal.signal(signal.SIGINT, lambda a,b: exit())

contest_list = ['weekly-contest-301']
username_list = get_all_users()
query_contests(contest_list, username_list)
