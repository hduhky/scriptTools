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

unresolved_problems = []

for problem in problems:
    for log_info in logs:
        msg = log_info['msg']
        if problem not in msg:
            if problem not in unresolved_problems:
                unresolved_problems.append(problem)

for unresolved_problem in unresolved_problems:
    print('waring! problem %s is not in svn log' % unresolved_problem)