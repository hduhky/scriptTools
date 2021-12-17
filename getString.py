# -*- coding:UTF8 -*-

import os 
import re

file = open('/Users/smb-lsp/Desktop/Switch/trunk_ezlive_switch/ios/EZViewer/EZViewer.pch', 'r+')
string = file.read()
pattern = re.compile(r'(?<=#import ")([^"]*)')   # 查找数字
result = pattern.findall(string)
 
print(result)