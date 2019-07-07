#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import sys
import paramiko
import yaml

from common import Common


class Demo:
    def __init__(self):
        self.common    = Common()
        self.filename  = 'input.yml'
        #self.category = 'localhost'
        self.category  = 'sakura'
        self.conts     = 0
        self.max_conts = 3
        self.cmd_option_key = 'systemctl'

        try:      
            if sys.argv[1] == 'httpd' or sys.argv[1] == 'firewalld':
                self.command = 'systemctl status {service}'.format(service=sys.argv[1])
            elif sys.argv[2] == 'httpd' or sys.argv[2] == 'firewalld':
                self.command = 'systemctl status {service}'.format(service=sys.argv[2])
            else:
                sys.exit(1)
        except:
            raise IndexError(
                "Three command arguments are required. {args}".format(args=' '.join(sys.argv[0])) 
            )


    def get_input(self):
        input = {}
        for key, value in yaml.safe_load(open(self.filename))[self.category].iteritems():
            input[key] = value
        
        return input
    
    def create_commmand(self, cmd_option=None):
        if cmd_option is None:
            if sys.arg[1]:
                return " {service}".format(tar)
        else:
            return " {opt}".format(opt = ' '.join(cmd_option))
    
    
    def get_output(self, stdout):
        output = {}
        for key in [
            'timestamp', 'bool', 'execute_conts', 'cmd', 'response'
            ]:
            output[key] = ""

        response = []
        try:
            stdout = stdout.read()
            if type(stdout) == str:
                if re.search(r'\s*(.*)(\n*)\s*', stdout):
                    response.append(re.search(r'\s*(.*)(\n*)\s*', stdout).group(1))
                else:
                    response.appned(stdout)
            else:
                pass
        except:
            pass
        
        if 1 <= len(response) and re.search(r'\s*(Active:)\s+(active)\s+(\(running\))', response[0]):
            output.update({
                'bool'    : True,
                'response': ', '.join(response)
            })
        elif 1 <= len(response):
            output.update({
                'bool'    : False,
                'response': ', '.join(response)
            })
        else:
            output.update({
                'bool'    : False,
                'response': None
            })

        
        output.update({
            'cmd': self.command,
            'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        return output
    

    def main(self):
        outputs = []
        input = self.get_input()
        self.command = self.command + self.create_commmand(input['cmd_option'][self.cmd_option_key])
        while True:
            try:
                stdin, stdout, stderr = self.common.execute_command(input, self.command)
                current_output = self.get_output(stdout)
                self.conts += 1
                if current_output['bool']:
                    current_output.update({'execute_conts': self.conts})
                    break
                else:
                    if self.conts < self.max_conts:
                        current_output = None
                        continue
                    else:
                        current_output.update({'execute_conts': self.conts})
                        break
            except:
                current_output = None
                break

        if current_output is None:
            outputs = None
        else:
            outputs.append(current_output)

        return outputs