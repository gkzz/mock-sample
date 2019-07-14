#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import yaml
import traceback

from common import Common


class Demo:
    def __init__(self):
        self.common    = Common()
        self.filename  = 'input.yml'
        #self.category = 'localhost'
        self.category  = 'sakura'
        self.command   = 'ls'
        self.cmd_option_key = self.command
        #self.cmd_option_key = None
        self.conts     = 0
        self.max_conts = 3
        self.column_order = [
            'timestamp', 'success', 'execute_conts', 'command', 'stdout', 'stderr' 
        ]

    def _set_option(self, input):
        if self.cmd_option_key is None:
            return ""
        else:
            return " {opt}".format(opt = input["cmd_option"][self.cmd_option_key])



    def set_filekey(self):
        if re.search(r'\s*(\S+)\s*', self.command):
            return '{filekey}'.format(
                filekey=re.search(r'\s*(\S+)\s*', self.command).group(1)
            )
        else:
            return 'unknown_command'
        

    def main(self):
        outputs = []
        success = False
        stdout = None
        stderr = None 

        input = self.common.get_input(self.filename, self.category)
        self._cmd_option = self._set_option(input)
        self.command = self.command + self._cmd_option
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
                stdout = None
                stderr = traceback.format_exc()
                continue

        if outputs is not None:
            filekey = self.set_filekey()
            self.common.log(filekey, outputs, self.column_order)
        else:
            pass

        self.common = None

        return outputs