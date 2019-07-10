#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import datetime
import re
import yaml

from common import Common


class Demo:
    def __init__(self):
        self.common    = Common()
        self.filename  = 'input.yml'
        #self.category = 'localhost'
        self.category  = 'sakura'
        self.command   = 'ls'
        self.cmd_option_key = 'systemctl'
        self.conts     = 0
        self.max_conts = 3
        self.ptn = re.compile(r'\s*(Active:)\s+(active)\s+(\(running\))')

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


        self.column_order = [
            'timestamp', 'success', 'execute_conts', 'command', 'stdout', 'stderr' 
        ]

    
    def create_commmand(self, cmd_option=None):
        if cmd_option is None:
            return ""
        else:
            return " {opt}".format(opt = ' '.join(cmd_option))
    
        

    def main(self):
        outputs = []
        input = self.common.get_input(self.filename, self.category)
        self.command = self.command + self.create_commmand(
            input['cmd_option'][self.cmd_option_key]
        )
        while True:
            try:
                if self.conts < self.max_conts:
                    success, stdout, stderr = self.common.execute_command(
                        input, self.command, self.ptn
                    )
                    current_output = None
                    if success:
                        current_output = self.common.get_output(
                            success, self.conts, self.command, 
                            stdout, stderr, self.column_order
                        )
                        outputs.append(current_output)
                        break
                    else:
                        self.conts += 1
                        continue
                else:
                    success = False
                    current_output = self.common.get_output(
                        success, self.conts, self.command, 
                        stdout, stderr, self.column_order
                    )
                    outputs.append(current_output)
            except:
                outputs = None
                self.conts += 1
                continue


        
        if outputs is not None:
            self.common.log(self.cmd_option_key, outputs, self.column_order)
        else:
            pass
        
        self.common = None

        return outputs