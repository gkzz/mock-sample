#! /usr/bin/env python
# -*- coding: utf-8 -*-
#from os import path
import os
import sys
import re
import yaml
import unittest
from mock import patch, MagicMock

sys.path.append('.')
sys.path.append('..')
sys.path.append('/usr/bin/python')
BASE_DIR = '/home/gkz/workspace/mock_sample'
sys.path.append(BASE_DIR)
sys.path.append(BASE_DIR + '/27/local/lib/python2.7/site-packages')
test_dir = BASE_DIR + '/tests'
sys.path.append(test_dir)
config_dir = test_dir + '/config'

from mock_sample.common import Common
from mock_sample.ls_dir import Demo

#https://cpython-test-docs.readthedocs.io/en/latest/library/unittest.mock.html


### load yam
def load_yaml(filename, category):
    dict = {}
    for key, value in yaml.safe_load(open(filename))[category].iteritems():
        dict[key] = value
    
    return dict

test_input = load_yaml(config_dir  + '/test_input.yml', 'sakura')
test_output = load_yaml(config_dir  + '/test_output.yml', 'ls')
response = load_yaml(config_dir  + '/response.yml', 'ls')
response_true = response['true']
response_false = response['false']

class TestLsDir(unittest.TestCase):

    """
    def test01_nomock(self):
        obj = Demo()
        outputs = obj.main()
        self.assertEqual(
            len(outputs[0]), len(test_output)
        )
        self.assertIn(
            "2019", outputs[0]["timestamp"]
        )
        self.assertEqual(
            outputs[0]["success"], test_output["success"]
        )
        self.assertEqual(
            outputs[0]["execute_conts"], test_output["execute_conts"]
        )
        self.assertEqual(
            outputs[0]["stdout"], test_output["stdout"]
        )
        self.assertEqual(
            outputs[0]["stderr"], test_output["stderr"]
        )
    """
    class_common = 'mock_sample.common.Common'
    method_params = class_common + '.get_input'
    method_execute_command = class_common + '.execute_command'
    method_log = class_common + '.log'

    
    @patch(method_log, return_value='method_log')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test01_ok_ls_demo_dir(self, params, execute, logger):
        
        def _get_input(_filename, _category):
            """
            test_input = {
                'hostname': '<ip_address>',
                'username': '<username>', 
                'password': '<password>', 
                'port': <port, e.g. 22>
                'key': '</path/.ssh/id_rsa>', 
                'allow_agent': False, 
                'look_for_keys': False, 
                'cmd_option': {
                    'ls': 'demo/'
                },
            }
            """

            return test_input


        def _execute_command(_input, _command):
            stdout = None
            stderr = None

            if re.search(
                r'^\s*(ls)\s+(-la)\s+(demo\/)\s*$', _command):
                stdout = ', '.join(response_true['stdout']['demo_la_opt'])
                stdout = stdout.lstrip('\n')
            elif re.search(
                r'^\s*(ls)\s+(demo\/)\s*$', _command):
                stdout = response_true['stdout']['demo']
                
            else:
                raise Error("_excute_command_error")
                
            
            return stdout, stderr

        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value

        obj = Demo()
        outputs = obj.main()


        self.assertEqual(
            len(outputs[0]), 6
        )
        self.assertIn(
            "2019", outputs[0]["timestamp"]
        )
        self.assertEqual(
            outputs[0]["success"], test_output["success"]
        )
        self.assertEqual(
            outputs[0]["execute_conts"], test_output["execute_conts"]
        )
        self.assertEqual(
            outputs[0]["stdout"], test_output["stdout"]['demo']
        )
        self.assertEqual(
            outputs[0]["stderr"], None
        )

    @patch(method_log, return_value='dummy')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test02_ok_ls_demo_la(self, params, execute, logger):
        
        def _get_input(_filename, _category):
            """
            test_input = {
                'hostname': '<ip_address>',
                'username': '<username>', 
                'password': '<password>', 
                'port': <port, e.g. 22>
                'key': '</path/.ssh/id_rsa>', 
                'allow_agent': False, 
                'look_for_keys': False, 
                'cmd_option': {
                    'ls': 'demo/'
                },
            }
            """
            test_input.update({
                'cmd_option': {
                    'ls': '-la demo/'
                }
            })

            return test_input


        def _execute_command(_input, _command):
            stdout = None
            stderr = None

            if re.search(
                r'^\s*(ls)\s+(-la)\s+(demo\/)\s*$', _command):
                stdout = ', '.join(response_true['stdout']['demo_la_opt'])
                stdout = stdout.lstrip('\n')
            elif re.search(
                r'^\s*(ls)\s+(demo\/)\s*$', _command):
                stdout = response_true['stdout']['demo']
            else:
                raise Exception("_excute_command_error")
                
            
            return stdout, stderr

        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value

        obj = Demo()
        outputs = obj.main()


        self.assertEqual(
            len(outputs[0]), 6
        )
        self.assertIn(
            "2019", outputs[0]["timestamp"]
        )
        self.assertEqual(
            outputs[0]["success"], test_output["success"]
        )
        self.assertEqual(
            outputs[0]["execute_conts"], test_output["execute_conts"]
        )
        self.assertEqual(
            outputs[0]["stdout"], 
            ', '.join(test_output["stdout"]["demo_la_opt"]).lstrip('\n')
        )
        self.assertEqual(
            outputs[0]["stderr"], None
        )


if __name__ == '__main__':
    unittest.main()