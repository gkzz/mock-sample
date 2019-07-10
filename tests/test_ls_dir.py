#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import unittest
from mock import patch, MagicMock

sys.path.append('.')
sys.path.append('..')
sys.path.append('../tests/common')
sys.path.append('../tests/ls_dir')
from common import Common
from ls_dir import Demo

#https://cpython-test-docs.readthedocs.io/en/latest/library/unittest.mock.html


BASE_DIR = '/home/gkz/workspace/mock-sample'
#sys.path.append(BASE_DIR)
test_dir = BASE_DIR + '/tests'
#sys.path.append(test_dir)
config_dir = test_dir + '/config'
#sys.path.append(config_dir)

### load yam
def load_yaml(filename, category):
    dict = {}
    for key, value in yaml.safe_load(open(filename))[category].iteritems():
        dict[key] = value
    
    return dict

import pdb; pdb.set_trace()
test_output = load_yaml(config_dir  + '/test_output.yml', 'ls')
response = load_yaml(config_dir  + '/response.yml', 'ls')
response_true = response['true']
response_false = response['false']

class TestLsDir(unittest.TestCase):
    method_execute_command = 'Common.execute_command'
    method_log = 'Common.log'

    @patch(method_log)
    @patch(method_execute_command) 
    def test01_ok_ls_dir(self, execute, logger):
        def execute_command_test(self, input, command):
            stdout = response_true['stdout']
            stderr = response_true['stderr']
            return stdout, stderr
        
        obj = Demo()
        outputs = obj.main()
        
        execute.side_effect = execute_command_test
        logger.return_value = test_output

        
        self.assertEqual(
            outputs[0]['timestamp'],
            test_output['timestamp']
        )


