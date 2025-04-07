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

def extract_sensitive_words_by_quote(file_path):
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

def extract_sensitive_words_by_split(file_path):
    if not os.path.isfile(file_path):
        print(f"错误：文件不存在 -> {file_path}")
        return []

    encoding = detect_encoding(file_path)
    if not encoding:
        print("无法识别文件编码")
        return []

    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()

    # 先移除所有中英文双引号
    content = content.replace('"', '').replace('"', '').replace('"', '')
    
    separators = ['\n', '/', '、']
    for sep in separators:
        content = content.replace(sep, '|')

    words = [w.strip() for w in content.split('|') if w.strip()]
    return words

def save_words_to_file(words, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for word in words:
                f.write(word.strip() + '\n')
        print(f"敏感词已保存到：{output_path}")
        return True
    except Exception as e:
        print(f"保存文件时出错：{str(e)}")
        return False

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("用法：python extract_sensitive_words.py <敏感词txt路径> [mode/output] [output]")
        print("参数说明：")
        print("- mode可选：quote（默认，按引号提取），split（按换行/顿号/斜杠切分）")
        print("- output：输出文件路径")
        print("示例：")
        print("python extract_sensitive_words.py input.txt")
        print("python extract_sensitive_words.py input.txt output.txt")
        print("python extract_sensitive_words.py input.txt split")
        print("python extract_sensitive_words.py input.txt split output.txt")
        return

    file_path = sys.argv[1]
    mode = 'quote'
    output_path = None
    
    if len(sys.argv) == 3:
        # 判断第二个参数是mode还是output路径
        if sys.argv[2] in ['quote', 'split']:
            mode = sys.argv[2]
        else:
            output_path = sys.argv[2]
    elif len(sys.argv) == 4:
        mode = sys.argv[2]
        output_path = sys.argv[3]

    if mode == 'split':
        words = extract_sensitive_words_by_split(file_path)
    else:
        words = extract_sensitive_words_by_quote(file_path)

    if words:
        if output_path:
            save_words_to_file(words, output_path)
        else:
            print("提取出的敏感词：")
            for word in words:
                print(word.strip())
    else:
        print("没有提取到任何敏感词")

if __name__ == "__main__":
    main()