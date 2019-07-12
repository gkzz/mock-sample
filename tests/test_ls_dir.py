#! /usr/bin/env python
# -*- coding: utf-8 -*-
#from os import path
import os
import sys
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
    #method_input = class_common + '.input'
    method_execute_command = class_common + '.execute_command'
    method_log = class_common + '.log'

    #"""
    @patch(method_log, return_value='method_log')
    @patch(method_execute_command) 
    #@patch(method_input) 
    def test01_ok_ls_dir(self, execute, logger):

        """
        def _get_input(_filename, _category):
            input = {}
            for key, value in yaml.safe_load(open(filename))[category].iteritems():
                input[key] = value
        
            return input
        """

        def _execute_command(_input, _command):
            stdout = response_true['stdout']
            stderr = None
            return stdout, stderr
        
        
        execute.side_effect = _execute_command
        dummy = logger.return_value
        print('logger.return_value: {val}'.format(val=dummy))

    #"""

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

if __name__ == '__main__':
    unittest.main()


