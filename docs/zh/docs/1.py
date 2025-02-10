import os
import re
from bs4 import BeautifulSoup


def fix_unclosed_tags(markdown_content):
    """
    修复Markdown内容中未闭合的HTML标签
    """
    # 使用正则表达式提取HTML片段
    html_fragments = re.findall(r'<[^>]+>', markdown_content)

    # 将HTML片段组合成一个完整的HTML文档
    html_content = '<html><body>' + ''.join(html_fragments) + '</body></html>'

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html5lib')

    # 获取修复后的HTML内容
    fixed_html = str(soup.body)

    # 去除多余的<html>和<body>标签
    fixed_html = fixed_html.replace('<body>', '').replace('</body>', '')

    # 将修复后的HTML替换回Markdown内容
    for original, fixed in zip(html_fragments, re.findall(r'<[^>]+>', fixed_html)):
        markdown_content = markdown_content.replace(original, fixed)

    return markdown_content


def process_markdown_file(file_path):
    """
    处理单个Markdown文件
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    fixed_content = fix_unclosed_tags(content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(fixed_content)
    print(f"已修复文件: {file_path}")


def find_and_fix_markdown_files(root_dir):
    """
    递归查找并修复所有Markdown文件
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                process_markdown_file(file_path)


if __name__ == "__main__":
    root_directory = r'/Users/liujingrong/Desktop/docs/docs/zh/docs/1newStruct/Server/Network'  # 替换为你的Markdown文件根目录
    find_and_fix_markdown_files(root_directory)
    print("所有Markdown文件已修复完成！")