import os
from csv import reader
import json

# 把csv文件中的翻译转化为arb文件

csv_path = '/Users/smb-lsp/Desktop/本地化/l10n.csv'

target_path = os.path.dirname(csv_path) + '/l10n/'
prefix = 'intl_'
suffix = '.arb'

locales = []
keys = []
result = {}
def read_csvfile(csvpath):
    flag = False 
    with open(csv_path, encoding='gbk') as csvfile:
        spamreader = reader(csvfile)
        for row in spamreader:
            if not flag:
                set_key(row)
                flag = True
                continue
            set_value(row)
    csvfile.close()

def set_key(key_row):
    for key in key_row:
        if key == 'keys':
            continue
        locales.append(key)
        result[key] = {}

def set_value(value_row):
    for value_index in range(len(value_row)):
        key = value_row[0]
        if value_index == 0:
            if key in keys:
                print('warning! key ${key} already exists!')
                continue
            keys.append(value_row[value_index])
        result[locales[value_index - 1]][key] = value_row[value_index]

def export_to_arb():
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    os.system('cd %s' % target_path)
    for locale in locales:
        data = result[locale]
        json_str = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
        file_name = prefix + locale + suffix
        with open(target_path + file_name, mode='w') as file:
            file.write(json_str)
        file.close()

read_csvfile(csv_path)

print('locales:')
print(locales)
print('keys:')
print(keys)
print('result:')
print(result)

export_to_arb()