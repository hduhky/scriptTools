# -*- coding: utf-8 -*-
import re
import sys
import os

try:
    import chardet
except ImportError:
    print("请先安装 chardet：pip install chardet")
    sys.exit(1)

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read(4096)
        result = chardet.detect(raw)
        return result['encoding']

def extract_sensitive_words(file_path):
    if not os.path.isfile(file_path):
        print(f"错误：文件不存在 -> {file_path}")
        return []

    encoding = detect_encoding(file_path)
    if not encoding:
        print("无法识别文件编码")
        return []

    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()

    # 支持中英文双引号匹配，提取被配对的引号中的词
    words = re.findall(r'[“"]([^“”"]+)[”"]', content)
    return words

def main():
    if len(sys.argv) != 2:
        print("用法：python extract_sensitive_words.py <敏感词txt路径>")
        return

    file_path = sys.argv[1]
    words = extract_sensitive_words(file_path)

    if words:
        print("提取出的敏感词：")
        for word in words:
            print(word.strip())
    else:
        print("没有提取到任何敏感词（请确保使用成对的引号）")

if __name__ == "__main__":
    main()