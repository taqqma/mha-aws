#!/usr/bin/env /usr/local/bin/python2.7
# coding: utf-8

import time
import paramiko
from Admin import Admin

logger = Admin()

class InteractiveCommand(object):

    def __init__(self, host, port, user, key_file):
        self.transport = paramiko.Transport((host, port))
        self.transport.connect(username=user, key_filename=key_file)
        self.channel = self.transport.open_session()

    def run(self, command):
        out = ''
        self.channel.setblocking(0)
        self.channel.invoke_shell()
        self.channel.send(command + '\n')
        t_check = 0

        while not self.channel.recv_ready():
            time.sleep(5)
            t_check += 1

            if 3 < t_check:
                logger.logging("error", "command time out")
                return False

            out = self.channel.recv(1024)
            return out