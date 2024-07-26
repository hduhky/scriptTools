# -*- coding: utf-8 -*-

import os
import shutil
import hashlib
import zipfile
import time


def get_desktop_path():
    return os.path.join(os.path.expanduser(u"~"), u"Desktop")

def get_trash_path():
    return os.path.join(os.path.expanduser(u"~"), u".Trash")


ADHOC_KEY = u"Adhoc"
APPSTORE_KEY = u"Appstore"
PRODUCT_CODE = u"yushiyun_iOS-R2101"
TRASH_PATH = get_trash_path()
DESKTOP_PATH = get_desktop_path()


def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()


def get_md5(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path,'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5


# 是否包含某个字符串
def contains_str(ori_str, a_str):
    ori_str_low = ori_str.lower()
    a_str_low = a_str.lower()
    if a_str_low in ori_str_low:
        return True
    else:
        return False


def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        print u"文件夹已存在"
        exit(2)
    return dir_path


# 1.输入版本号
project_revision = raw_input('请输入版本号(Version)：').strip()
num_list = project_revision.split(u".")
if len(num_list) != 3:
    print u"输入版本号格式有误"
    exit(2)
print project_revision
# 2.在桌面上找到对应文件夹,并将其中文件复制到一个新的文件夹
print u"移动文件中..."
date_str = time.strftime("%y%m%d", time.localtime(time.time()))
new_adhoc_file_name = u"%s.%s_test.ipa" % (PRODUCT_CODE, project_revision)
new_app_file_name = u"%s.%s.ipa" % (PRODUCT_CODE, project_revision)
new_folder_name = u"%s.%s.%s" % (PRODUCT_CODE, project_revision, date_str)
new_folder_path = os.path.join(DESKTOP_PATH, new_folder_name)
new_adhoc_file_path = os.path.join(new_folder_path, new_adhoc_file_name)
new_app_file_path = os.path.join(new_folder_path, new_app_file_name)
check_dir(new_folder_path)
has_find_adhoc_file = False
has_find_appstore_file = False
for root, dirs, files in os.walk(DESKTOP_PATH):
    if has_find_adhoc_file and has_find_appstore_file:
        break
    if root != DESKTOP_PATH:
        continue
    for a_dir in dirs:
        if has_find_adhoc_file and has_find_appstore_file:
            break
        if contains_str(a_dir, ADHOC_KEY):
            adhoc_folder_path = os.path.join(root, a_dir)
            adhoc_file_path = os.path.join(adhoc_folder_path, u"宇视云.ipa")
            if os.path.exists(new_adhoc_file_path):
                print u"已存在adhoc ipa文件"
                exit(2)
            shutil.copy(adhoc_file_path, new_adhoc_file_path)
            current_time_str = time.strftime("-%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
            folder_trash_path = os.path.join(TRASH_PATH, (a_dir+current_time_str))
            shutil.move(adhoc_folder_path, folder_trash_path)
            has_find_adhoc_file = True
            print "Adhoc Folder:%s" % adhoc_folder_path
        elif contains_str(a_dir, APPSTORE_KEY):
            app_folder_path = os.path.join(root, a_dir)
            app_file_path = os.path.join(app_folder_path, u"宇视云.ipa")
            if os.path.exists(new_app_file_path):
                print u"已存在appstore ipa文件"
                exit(2)
            shutil.copy(app_file_path, new_app_file_path)
            current_time_str = time.strftime("-%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
            folder_trash_path = os.path.join(TRASH_PATH, (a_dir + current_time_str))
            shutil.move(app_folder_path, folder_trash_path)
            has_find_appstore_file = True
            print "Appstore Folder:%s" % app_folder_path
# 3.生成MD5签名并写入文件
print u"生成文件md5中..."
if (not os.path.exists(new_adhoc_file_path)) or (not os.path.exists(new_app_file_path)):
    print u"ipa文件不全"
    exit(2)
adhoc_file_md5 = get_md5(new_adhoc_file_path)
app_file_md5 = get_md5(new_app_file_path)
adhoc_readme = u"MD5 (%s) = %s" % (new_adhoc_file_name, adhoc_file_md5)
app_readme= u"MD5 (%s) = %s" % (new_app_file_name, app_file_md5)
readme_content = adhoc_readme + u"\n\n" + app_readme
readme_file_path = os.path.join(new_folder_path, u"md5.txt")
if os.path.exists(readme_file_path):
    print u"md5.txt已存在"
    exit(2)
with open(readme_file_path, 'w') as f:
    f.write(readme_content)
# 4.压缩为压缩包
print u"压缩文件中..."
if (not os.path.exists(new_adhoc_file_path)) or \
    (not os.path.exists(new_app_file_path)) or \
    (not os.path.exists(readme_file_path)):
    print u"文件不完整"
    exit(2)
zip_file_path = new_folder_path + u".zip"
if os.path.exists(zip_file_path):
    print u"压缩包已存在"
    exit(2)
zip_dir(new_folder_path, zip_file_path)
print u"处理完成"

