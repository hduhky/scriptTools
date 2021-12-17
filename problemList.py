# -*- coding:UTF8 -*-

import os 
import re

file = open('/Users/smb-lsp/Desktop/b.txt', 'r+')
string = file.read()
pattern = re.compile(r'SMBD[\d]*')   # 查找数字
result = pattern.findall(string)
 
print(result)
