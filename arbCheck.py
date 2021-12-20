import os
import json

# 用于检查arb文件是否翻译齐全

def locale_from_file_name(file_name):
    prefix = 'intl_'
    suffix = '.arb'
    temp_str = str.replace(file_name, prefix, '')
    locale = str.replace(temp_str, suffix, '')
    return locale

def dic_from_file(file_path):
    with open(file_path) as file:
        dic = json.loads(file.read())
        file.close()
        return dic
    
def traverse(root_path):
    result = {}
    for dirname, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            locale = locale_from_file_name(filename)
            dic = dic_from_file(os.path.join(dirname, filename))
            result[locale] = dic
    return result

def all_keys_from_basic_locale_result(basic_locale_result):
    return dict.keys(basic_locale_result)

def check_locale_result(locale):
    locale_values = all_locale_result[locale]
    for key in all_keys:
        if key not in dict.keys(locale_values):
            print('warning! key: %s not exist in locale: %s' % (key, locale))
            continue
        if len(locale_values[key]) == 0:
            print('warning! value for key: %s not exist in locale: %s' % (key, locale))
            continue

all_locale_result = traverse('/Users/smb-lsp/Desktop/Flutter_Localization/lib/l10n')
basic_locale = 'en'

all_keys = all_keys_from_basic_locale_result(all_locale_result[basic_locale])

for locale_result in all_locale_result:
    check_locale_result(locale_result)