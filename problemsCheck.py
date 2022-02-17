from csv import reader

problems = []
logs = []


def read_problems(csvpath):
    with open(csvpath, encoding='utf-8') as csvfile:
        spamreader = reader(csvfile)
        for row in spamreader:
            problems.append(row[0])
    csvfile.close()


log_keys = []


def read_logs(csvpath):
    flag = False
    with open(csvpath, encoding='utf-8') as csvfile:
        spamreader = reader(csvfile)
        for row in spamreader:
            if not flag:
                log_keys = row
                flag = True
                continue
            log_info = {}
            for key_index in range(len(row)):
                key = log_keys[key_index]
                log_info[key] = row[key_index]
            logs.append(log_info)
    csvfile.close()


read_problems('/Users/hky/Desktop/problem.csv')

read_logs('/Users/hky/Desktop/log.csv')

all_problems = []
solved_problems = []

for problem in problems:
    all_problems.append(problem)
    for log_info in logs:
        msg = log_info['msg']
        if problem in msg:
            if problem not in solved_problems:
                solved_problems.append(problem)

for solved_problem in solved_problems:
    # print('problem %s is in svn log' % solved_problem)
    if solved_problem in all_problems:
        all_problems.remove(solved_problem)

for unresolved_problem in all_problems:
    print('waring! problem %s is not in svn log' % unresolved_problem)
