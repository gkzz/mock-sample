#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime
import paramiko as pm
import yaml
import pandas as pd
import csv

class Common:
    def get_input(self, filename, category):
        input = {}
        for key, value in yaml.safe_load(open(filename))[category].iteritems():
            input[key] = value
        
        return input

    def open_session(self, input):
        self.client = pm.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(pm.WarningPolicy())
        self.client.connect(
            input['hostname'], port=input['port'] , 
            username=input['username'], password=input['password'], key_filename=input['key'],
            #
            # cf. paramiko no existing session exception
            #     https://stackoverflow.com/questions/6832248/paramiko-no-existing-session-exception
            allow_agent=input['allow_agent'],look_for_keys=input['look_for_keys']
        )

    def execute_command(self, input, command):
        self.open_session(input)
        #stdin, stdout, stderr = self.client.exec_command(command)
        _, stdout, stderr = self.client.exec_command(command)
        stdout = stdout.read()
        stderr = stderr.read()
        if stderr == '':
            stdout = stdout.replace('\n', ', ').strip()
            stderr = None
        elif stdout == '':
            stdout = None 
            stderr = stderr.replace('\n', ', ').strip()
        else:
            stdout = None
            stderr = None
        
        return stdout, stderr
    
    def get_output(self, success, conts, command, stdout, stderr, column_order):
        output = {}
        for key in column_order:
            output[key] = ""

        output.update({
            'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'success': success,
            'execute_conts': conts,
            'command': command,
            'stdout': stdout,
            'stderr': stderr
        })

        return output
    
    
    def log(self, key, outputs, column_order=None):
        filename = 'logs/log_'+ key + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        if len(outputs) == 0:
            pass
        else:
            df = pd.DataFrame(outputs)
            if column_order is None:
                df.to_json(
                    filename + '.json', force_ascii=False, orient='split'
                )
            else:
                df.to_csv(
                    filename + '.csv', sep=',', encoding='UTF-8', 
                    index=False, quoting=csv.QUOTE_ALL, columns=column_order
                )