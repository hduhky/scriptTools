# -*-coding:utf-8-*-
import os
import codecs
import chardet
import commands
#from common_tool import *

# 忽略文件夹、文件列表(文件、路径中饮食此列表中的字符将会被忽略，不区分大小写)
ignore_file_list = [".a", ".png", ".json", ".xcscheme", ".pbxproj"]
#统计区间,如："16160:16207"
# revision_interval = "16160:16207"


# #######工具#######
# 获取文件夹svn地址
def get_branch_for_folder(folder_path):
    cmd = "cd %s;svn info --show-item url" % folder_path
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        return output
    else:
        return None


# 显示第page_index页的log，每页数目为page_number
# page_index 从0开始
def show_log_with_page(branch_path, page_number, page_index):
    log_cmd = "svn log %s" % (branch_path)
    (status, output) = commands.getstatusoutput(log_cmd)
    line_list = output.split("\n")
    start_index = page_number * page_index
    end_index = start_index + page_number
    count = 0
    for line in line_list:
        if count >= start_index and count <= end_index:
            print line
        if contains_str(line, "----------"):
            count = count + 1
        if count > end_index:
            return


# 显示最近的log
def show_log(branch_path, page_number):
    current_page_index = 0;
    while(1) :
        show_log_with_page(branch_path, page_number, current_page_index)
        current_page_index = current_page_index + 1
        more_log = raw_input('show more logs(y/n)：')
        more_log = more_log.strip()
        if contains_str(more_log, "y"):
            show_log_with_page(branch_path, page_number, current_page_index)
        else:
            break;


# 判断是否是一个版本号字符串, r29943，类型会被认为是版本号
def revision_from_str(revision_str):
    pure_str = revision_str.strip()
    if not revision_str:
        return revision_str
    if pure_str[0] == "r":
        return pure_str[1:]
    return pure_str


# 获取文件编码格式
def get_file_encode_format(file_path):
    f = open(file_path, 'rb')
    data = f.read()
    # TD 有精确度参数，后面可以判断一下，这里不影响
    format_str = chardet.detect(data)['encoding']
    f.close()
    return format_str


def contains_str(ori_str, str):
    ori_str_low = ori_str.lower()
    str_low = str.lower()
    if str_low in ori_str_low:
        return True
    else:
        return False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    
    return False

# #######工具#######


def get_diff_line_numer(output):
    line_list = output.split("\n")
    dict = {}
    for line in line_list:
        if line.startswith("Index:"):
            key = line.split(':')[-1].strip()
            if key not in dict:
                dict[key] = [0, 0]
        if line.startswith('+') and len(line.strip()) > 1:
            dict[key][0] += 1
        if line.startswith('+++'):
            dict[key][0] -= 1
        if line.startswith('-') and len(line.strip()) > 1:
            dict[key][1] += 1
        if line.startswith('---'):
            dict[key][1] -= 1
    ExcludeFileNum = 0
    AddLineNum = 0
    DelLineNum = 0
    TotalLineNum = 0
    TotalFileNum = len(dict.keys())
    for file in dict.keys():
        if file == '.':
            TotalFileNum -= 1
        elif need_ignore_file(file):
#            print u"Skipping file : %s" % file
            ExcludeFileNum += 1
        else:
            print file
            AddLineNum += dict[file][0]
            DelLineNum += dict[file][1]
    TotalLineNum = AddLineNum + DelLineNum
    result_dic = {
        u"add_line" : AddLineNum,
        u"delete_line" : DelLineNum,
        u"total_change": TotalLineNum,
        u"add_file": TotalFileNum,
        u"delete_file": ExcludeFileNum,
        u"total_file": TotalFileNum
    }
    print "\n\n===============代码差异统计================="
    print "新增的代码行 = ", AddLineNum, " 行"
    print "删除的代码行 = ", DelLineNum, " 行"
    print "代码行变更总计 = ", TotalLineNum, " 行"
    print "变更文件总数 = ", TotalFileNum, " 个"
    print "排除文件总数 = ", ExcludeFileNum, " 个"
    print "计入文件总数 = ", TotalFileNum - ExcludeFileNum, " 个"
    print "===============代码差异统计=================\n"
    return TotalLineNum


def get_code_change_number(project_path, start_revision, end_revision):
    if (not is_number(start_revision)):
        print "输入版本号非数字"
        exit(1)
    if not is_number(end_revision):
        end_revision = "HEAD"
    revision_str = u"%s:%s" % (start_revision, end_revision)
    diff_cmd = u"cd %s;svn diff -r %s" % (project_path, revision_str)
    (status, output) = commands.getstatusoutput(diff_cmd)
    return get_diff_line_numer(output)


def need_ignore_file(file_name):
    # 1.过滤掉的文件夹，未考虑文件夹重名（在不同层次）
    for key_word in ignore_file_list:
        if contains_str(file_name, key_word):
            return True
    return False


def main():
    project_path = raw_input('请输入工程文件路径：')
    project_path = project_path.strip()
    branch_path = get_branch_for_folder(project_path)
    if branch_path:
        show_log(branch_path, 5)
    else:
        print "\'%s\' is not a working copy" % project_path
        exit(1)
    start_revision = raw_input('请输入开始版本号(统计时不包括此次提交):')
    start_revision = revision_from_str(start_revision)
    end_revision = raw_input('请输入终止版本号(统计时包括此次提交,最新可以直接回车):')
    end_revision = revision_from_str(end_revision)
    get_code_change_number(project_path, start_revision, end_revision)


if __name__ == "__main__":
    main()
