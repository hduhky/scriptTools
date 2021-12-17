# -*-coding:utf-8-*-
import os
import shutil

#用于根据日志把修改图片保存到目标路径

result = []
with open('/Users/smb-lsp/Desktop/log.txt') as file:
    lines = file.readlines()
    for line in lines:
        if '/branches_vvdbugfix/h06560_workspace/Uniarch_ChangeColor/' not in line:
            continue
        line = line.strip('\n')
        path = line.split('/branches_vvdbugfix/h06560_workspace/Uniarch_ChangeColor')[1]
        if path not in result:
            result.append(path)
    
srcPath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor'
dstPath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images'

print('start copy images...')
for path in result:
    if path.endswith(('png', 'jpg', 'jpeg', 'gif', 'pdf')):
        fileSrcPath = srcPath + path
        if not os.path.exists(fileSrcPath):
            print('warning! 该文件已被删除 ' + path)
            continue
        fileDstPath = os.path.dirname(dstPath + path)
        if not os.path.exists(fileDstPath):
            os.makedirs(fileDstPath)
        shutil.copy(fileSrcPath, fileDstPath)
print('copy images finished')
