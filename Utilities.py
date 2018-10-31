import re
import os
import sys
import shutil
import fileinput
from datetime import datetime


USAGE_STR = 'usage: python Utilities.py [--generate | --publish | --unpublish] <path>\n'
MISSING_PATH_STR = 'error: missing <path>\n'
INCORRECT_PATH_STR = 'error: <path> must start with `{root_folder}/`\n'
UNKNOWN_ARG_STR = 'error: unknown option `{arg}`'


def create_url(title):
    return '-'.join((re.sub('[^A-Za-z0-9_ ]+', '', title.strip().lower())).split(' '))

def get_current_date_time():
    now = datetime.now()
    post_date = now.strftime('%Y-%m-%d')
    post_time = now.strftime('%H:%M:%S -4000')
    return post_date, post_time    

def generate_draft():
    post_title = input('Title of post: ')
    post_url = create_url(post_title)
    categories = re.sub(' +', ' ', input('Categories (each separated by a space): ').lower().strip())

    post_date, post_time = get_current_date_time()
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


def publish(file_path, src='_drafts', dest='_posts'):
    file_name = file_path.split('/')[-1]

    post_date, post_time = get_current_date_time()
    for line in fileinput.input(file_path, inplace=True):
        if line.startswith('date:'):
            print('date: {} {}'.format(post_date, post_time))
        else:
            print(line, end='')

    new_file_name = post_date + '-' + file_name[11:]
    os.rename(file_path, '_posts/{}'.format(new_file_name))


def move_file(file_name, src, dest):
    src_file_path = '{}/{}'.format(src, file_name)
    dest_file_path = '{}/{}'.format(dest, file_name)
    shutil.move(src_file_path, dest_file_path)


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(USAGE_STR)
        sys.exit(1)

    action = sys.argv[1].lower()
    rel_file_path = sys.argv[2] if len(sys.argv) >= 3 else None
    file_name = rel_file_path.split('/')[-1] if rel_file_path else None

    try:
        if action == '--generate':
            generate_draft()
        elif action == '--publish':
            if len(sys.argv) < 3 or not rel_file_path:
                print(MISSING_PATH_STR)
                print(USAGE_STR)
                sys.exit(1)

            if not rel_file_path.startswith('_drafts/'):
                print(INCORRECT_PATH_STR.format(root_folder='_drafts'))
                sys.exit(1)

            publish(rel_file_path)
        elif action == '--unpublish':
            if len(sys.argv) < 3 or not rel_file_path:
                print(MISSING_PATH_STR)
                print(USAGE_STR)
                sys.exit(1)

            if not rel_file_path.startswith('_posts/'):
                print(INCORRECT_PATH_STR.format(root_folder='_posts'))
                sys.exit(1)

            move_file(file_name, src='_posts', dest='_drafts')
        else:
            print(UNKNOWN_ARG_STR.format(arg=action))
            print(USAGE_STR)
            sys.exit(1)

    except FileNotFoundError as e:
        print('error: {}\n'.format(''.join(str(e).split(']')[1:]).strip()))
        sys.exit(1)


if __name__ == '__main__':
    main()
