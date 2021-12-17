import os
from git import Repo

# 用于检测三方库版本号

repo_dir = '/Users/smb-lsp/Desktop/Others/TBPlayer'
base_dir = '/Users/smb-lsp/Desktop/Others/TBPlayer/TBPlayer/Classes'
comp_dir = '/Users/smb-lsp/Desktop/Base/trunk2.0/ios/ThirdLibrary/Foundation/TBPlayer/Classes'

def cmp_file(f1, f2):
    if not os.path.exists(f2):
        return False

    st1 = os.stat(f1)
    st2 = os.stat(f2)

    # 比较文件大小
    if st1.st_size != st2.st_size:
        return False

    bufsize = 8*1024
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)  # 读取指定大小的数据进行比较
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True

def tag_match(tag_name):
    if not os.path.exists(base_dir):
        return -1;
    diff_results = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        if dirpath.endswith('.git'):
            continue
        for filename in filenames:        
            base_file_path = os.path.join(dirpath, filename)
            if base_file_path.endswith('plist'):
                continue
            comp_file_path = base_file_path.replace(base_dir, comp_dir)
            # print(base_file_path + '\n' + comp_file_path)
            same = cmp_file(base_file_path, comp_file_path)
            if not same:
                diff_results.append(base_file_path)
                continue

    diff_count = len(diff_results)
    if diff_count == 0:
        print('version match: ' + tag_name)
        repo.git.checkout('master')
        exit()
    return diff_count

repo = Repo(repo_dir)
assert not repo.bare

comp_dir += '/'
base_dir += '/'

tag_names = []
diff_count_min = 10000
closet_tag = ''

assert len(repo.tags)
for tag_ref in repo.tags:
    tag_names.append(tag_ref.name)

tag_names.reverse()
for tag_name in tag_names:
    repo.git.checkout(tag_name)
    diff_count = tag_match(tag_name)
    if diff_count == -1:
        continue
    if diff_count < diff_count_min:
        diff_count_min = diff_count
        closet_tag = tag_name

print('version match end, most likely tag is ' + closet_tag)
repo.git.checkout(closet_tag)
os.system('bcomp %s %s' % (base_dir, comp_dir))

