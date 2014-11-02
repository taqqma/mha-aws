#!/usr/bin/env /usr/local/bin/python2.7
# coding: utf-8

import sys
import argparse
from Route_table import RouteTable
from Admin import Admin
from Remoteshell import InteractiveCommand


logger = Admin()


def main():
    """
    - MHA側から、--commandオプションを渡される
    　-- status : MHA起動時、特に何もしない
      -- stop/stopssh : MHAがmaster-MySQL死亡と判断した時。Routing-Tableを削除する
      -- start : MHAが新masterを選出した後。新Routing-Tableを作成する
    """
    m = RouteTable()

    status_parser = argparse.ArgumentParser()
    status_parser.add_argument('--command', type=str, nargs='?')
    status_parser.add_argument('--orig_master_ip', type=str, nargs='?')
    status_parser.add_argument('--orig_master_host', type=str, nargs='?')
    status_parser.add_argument('--orig_master_port', type=str, nargs='?')
    status_parser.add_argument('--new_master_ip', type=str, nargs='?')
    status_parser.add_argument('--new_master_host', type=str, nargs='?')
    status_parser.add_argument('--new_master_port', type=str, nargs='?')
    status_parser.add_argument('--new_master_password', type=str, nargs='?')
    status_parser.add_argument('--ssh_users', type=str, nargs='?')

    args, unknown = status_parser.parse_known_args()

    mha_status = args.command
    mha_master_node = args.new_master_ip
    orig_node = args.orig_master_ip
    orig_port = args.orig_master_port
    ssh_user = args.ssh_users

    if mha_status == 'start':
        m.create_route(mha_master_node)
    elif mha_status == 'stopssh':
        try:
            shell = InteractiveCommand(orig_node, orig_port, ssh_user, '~/.ssh/id_rsa')
            shell.run('shutdown -h now')
        except Exception:
            pass
        m.delete_route()
    elif mha_status == 'stop':
        m.delete_route()
    else:
        sys.exit()



if __name__ == "__main__":
    main()