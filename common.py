#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import paramiko
import pandas as pd

class Common:
    def open_session(self, input):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())
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
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdin, stdout, stderr
    
    def log(self, outputs, log_dir):
        if len(outputs) != 0:
            df = pd.DataFrame(outputs)
            df.to_json(log_dir + '/log_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.json', force_ascii=False)
        else:
            pass