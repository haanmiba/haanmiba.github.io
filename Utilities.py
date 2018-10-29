from datetime import datetime
import re
import sys
import shutil


ERROR_STR = 'You need to enter the commands properly: python Utilities.py [generate/publish/unpublish] (file_path)'

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
preview: 
---

# {}
'''.format(post_title, post_date, post_time, categories, post_title)

    print(yml_header)

    with open('_drafts/{}.markdown'.format(post_url), 'w') as f:
        for line in yml_header.split('\n'):
            f.write(line.strip() + '\n')


def publish():
    orig_file_path = sys.argv[2]
    file_name = orig_file_path.split('/')[-1]
    new_file_path = '_posts/{}'.format(file_name)
    shutil.move(orig_file_path, new_file_path)


def unpublish():
    orig_file_path = sys.argv[2]
    file_name = orig_file_path.split('/')[-1]
    new_file_path = '_drafts/{}'.format(file_name)
    shutil.move(orig_file_path, new_file_path)


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(ERROR_STR)
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == 'generate':
        generate_draft()
    elif action == 'publish' and len(sys.argv) == 3:
        publish()
    elif action == 'unpublish' and len(sys.argv) == 3:
        unpublish()
    else:
        print(ERROR_STR)
        sys.exit(1)


if __name__ == '__main__':
    main()
