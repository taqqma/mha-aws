#!/usr/bin/env /usr/local/bin/python2.7
# coding:utf-8

import os
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--orig_master_host', type=str, nargs='?')
    parser.add_argument('--new_master_host', type=str, nargs='?')
    parser.add_argument('--new_slave_hosts', type=str, nargs='?')
    parser.add_argument('--subject', type=str, nargs='?')
    parser.add_argument('--body', type=str, nargs='?')

    args, unknown = parser.parse_known_args()

#    orig_node = args.orig_master_host
#    new_master_node = args.new_master_host
#    new_slave_node = args.new_slave_host
    subjects = args.subject
    message = args.body

    result = os.system(
        'cat <<EOF |'
        '/usr/sbin/sendmail -t To: 送信先メールアドレス\n'
        'From: 送信元メールアドレス \n'
        'Subject:' + subjects + '\n'
        '\n'
        + message + '\n'
        'EOF'
    )

if __name__ == "__main__":
    main()
