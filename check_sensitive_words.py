# -*- coding: utf-8 -*-
import os
import sys

def load_keywords(keyword_file):
    with open(keyword_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return set(line.strip() for line in lines if line.strip())

def scan_file(file_path, keywords):
    hits = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for lineno, line in enumerate(f, start=1):
                for word in keywords:
                    if word in line:
                        hits.append((file_path, lineno, word, line.strip()))
    except Exception as e:
        print(f"[跳过] 无法读取文件: {file_path}，原因: {e}")
    return hits

def scan_directory(root_dir, keywords):
    # 定义要扫描的文件扩展名
    allowed_extensions = {'.dart', '.ets', '.java', '.kt', '.swift', '.h', '.m', '.cpp'}
    
    # 定义要忽略的文件名模式
    ignore_patterns = {
        'test', 'mock', 'generated', 'build',  # 测试和构建文件
        '.git', '.svn', '.idea', '.vscode',    # 版本控制和IDE文件
        'node_modules', 'pods', 'gradle', 'oh_modules',       # 依赖目录
    }
    
    results = []
    total_files = 0
    skipped_files = 0
    
    def should_ignore(path):
        path_lower = path.lower()
        return any(pattern in path_lower for pattern in ignore_patterns)
    
    # 统计需要扫描的文件总数
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if should_ignore(dirpath):
            continue
        total_files += sum(1 for f in filenames 
                          if os.path.splitext(f)[1].lower() in allowed_extensions 
                          and not should_ignore(f))
    
    print(f"\n开始扫描，共发现 {total_files} 个源代码文件需要处理...\n")
    
    # 扫描文件并显示进度
    processed_files = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if should_ignore(dirpath):
            continue
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in allowed_extensions:
                if should_ignore(filename):
                    skipped_files += 1
                    continue
                filepath = os.path.join(dirpath, filename)
                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"\r当前进度: {progress:.1f}% ({processed_files}/{total_files}) - 正在扫描: {filename}", end='')
                hits = scan_file(filepath, keywords)
                results.extend(hits)
    
    print(f"\n\n扫描完成！(已忽略 {skipped_files} 个匹配忽略规则的文件)")
    return results

def output_results(results, output_file=None):
    print(f"\n共发现 {len(results)} 处敏感词命中：\n")
    
    # 准备输出内容
    output_lines = []
    for filepath, lineno, word, line in results:
        output_line = f"[{filepath}:{lineno}] 命中词：{word}，内容：{line}"
        output_lines.append(output_line)
    
    # 根据是否指定输出文件来决定输出方式
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))
            print(f"扫描结果已保存到：{output_file}")
        except Exception as e:
            print(f"保存结果到文件失败：{e}")
            print("将结果打印到控制台：\n")
            print('\n'.join(output_lines))
    else:
        print('\n'.join(output_lines))

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("用法: python3 check_sensitive_words.py <项目目录> <敏感词.txt> [输出文件路径]")
        return

    project_dir = sys.argv[1]
    keyword_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) == 4 else None

    if not os.path.exists(keyword_file):
        print(f"敏感词文件不存在: {keyword_file}")
        return

    if not os.path.isdir(project_dir):
        print(f"项目目录无效: {project_dir}")
        return

    keywords = load_keywords(keyword_file)
    results = scan_directory(project_dir, keywords)
    output_results(results, output_file)

if __name__ == '__main__':
    main()