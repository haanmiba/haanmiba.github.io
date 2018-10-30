from datetime import datetime
import re
import sys
import shutil


ERROR_STR = 'usage: python Utilities.py [--generate | --publish | --unpublish] <path>\n'


def generate_draft():
    post_title = input('Title of post: ')
    post_url = '-'.join((re.sub('[^A-Za-z0-9_ ]+', '', post_title.strip().lower())).split(' '))
    
    categories = input('Categories (each separated by a space): ').lower().strip()
    
    now = datetime.now()
    post_date = now.strftime('%Y-%m-%d')
    post_time = now.strftime('%H:%M:%S -4000')
    post_url = post_date + '-' + post_url

    yml_header = '''---
layout: post
title: "{}"
date: {} {}
categories: {}
preview: "Enter preview here."
---

'''.format(post_title, post_date, post_time, categories, post_title)

    with open('_drafts/{}.markdown'.format(post_url), 'w') as f:
        for line in yml_header.split('\n'):
            f.write(line.strip() + '\n')


def move_file(path, dest):
    file_name = path.split('/')[-1]
    new_path = '{}/{}'.format(dest, file_name)
    shutil.move(path, new_path)

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(ERROR_STR)
        sys.exit(1)

    action = sys.argv[1].lower()
    file_path = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        if action == '--generate':
            generate_draft()
        elif action == '--publish':
            if len(sys.argv) < 3 or not file_path:
                print('error: missing <path>')
                print(ERROR_STR)
                sys.exit(1)

            if not file_path.startswith('_drafts/'):
                print('error: <path> must start with `_drafts/`\n')
                sys.exit(1)

            move_file(file_path, dest='_posts')
        elif action == '--unpublish':
            if len(sys.argv) < 3 or not file_path:
                print('error: missing <path>')
                print(ERROR_STR)
                sys.exit(1)

            if not file_path.startswith('_posts/'):
                print('error: <path> must start with `_posts/`\n')
                sys.exit(1)

            move_file(file_path, dest='_drafts')
        else:
            print('error: unknown option `{}`'.format(action))
            print(ERROR_STR)
            sys.exit(1)

    except FileNotFoundError as e:
        print('error: {}\n'.format(str(e).split(']')[-1].strip()))
        sys.exit(1)


if __name__ == '__main__':
    main()
