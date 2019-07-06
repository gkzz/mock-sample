#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import paramiko
import yaml

from common import Common


class Demo:
    def __init__(self):
        self.common = Common()
        self.filename = 'input.yml'
        #self.category = 'localhost'
        self.category = 'sakura'
        self.command  = 'ls demo/'

    def get_input(self):
        input = {}
        for key, value in yaml.safe_load(open(self.filename))[self.category].iteritems():
            input[key] = value
        
        return input
    
    
    def get_output(self, stdout):
        success = True
        output = {}
        #
        #                      #1   #2
        ptn = re.compile(r'\s*(\S+)(\n*)\s*')
        #How to enumerate a range of numbers starting at 1
        #https://stackoverflow.com/questions/3303608/how-to-enumerate-a-range-of-numbers-starting-at-1
        #enumerate(sequence, start=1)
        for num, line in enumerate(stdout, start = 1):
            """
            print('num:{num}, line:{line}'.format(
                num=num, line=line
            ))
            """
            #line = None
            if line is None:
                success = False
                break
            elif ptn.search(str(line)):
                output[num] = str(ptn.search(line).group(1))
            else:
                output[num] = str(line)
        
        return success, output
    

    def main(self):
        input = self.get_input()
        stdin, stdout, stderr = self.common.execute_command(input, self.command)
        
        success, output = self.get_output(stdout)
        if success:
            output.update({'bool': True})
        else:
            output.update({'bool': False})
            
        
        output.update({
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        return output
          
