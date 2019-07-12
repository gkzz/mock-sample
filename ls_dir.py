#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
        self.cmd_option_key = self.command
        self.conts     = 0
        self.max_conts = 3
        self.column_order = [
            'timestamp', 'success', 'execute_conts', 'command', 'stdout', 'stderr' 
        ]

    
    def create_commmand(self, cmd_option=None):
        if cmd_option is None:
            return ""
        else:
            return " {opt}".format(opt = cmd_option)    
        

    def main(self):
        outputs = []
        success = False
        stdout = None
        stderr = None 

        import pdb; pdb.set_trace()
        input = self.common.get_input(self.filename, self.category)
        self.command = self.command + self.create_commmand(
            input['cmd_option'][self.cmd_option_key]
        )
        while True:
            current_output = {}
            try:
                if self.conts <= self.max_conts:
                    self.conts += 1
                    stdout, stderr = self.common.execute_command(
                        input, self.command
                    )
                    if stdout is not None and stderr is None:
                        success = True
                        current_output = self.common.get_output(
                            success, self.conts, self.command, 
                            stdout, stderr, self.column_order
                        )
                        outputs.append(current_output)
                        break
                    else:
                        continue
                else:
                    success = False
                    current_output = self.common.get_output(
                        success, self.conts, self.command, 
                        stdout, stderr, self.column_order
                    )
                    outputs.append(current_output)
                    break
            except:
                continue

        if outputs is not None:
            self.common.log(self.cmd_option_key, outputs, self.column_order)
        else:
            pass

        self.common = None

        return outputs