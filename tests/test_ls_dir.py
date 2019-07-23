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

"""
try:
    from common import Common
    from ls_dir import Demo
except ImportError:
    from mock_sample.common import Common
    from mock_sample.ls_dir import Demo
except:
    sys.exit()
"""

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

    def setUp(self):
        # Read yml file
        self.test_input = load_yaml(
            config_dir  + '/test_input.yml', 'sakura'
        )
        # Set Object
        self.obj = Demo()
    
    def tearDown(self):
        self.test_input = None
        self.outputs = None

    """
    def test00_nomock(self):

        self.outputs = self.obj.main()
        self.assertEqual(
            len(self.outputs[0]), 6
        )
        self.assertIn(
            "2019", self.outputs[0]["timestamp"]
        )
        self.assertEqual(
            self.outputs[0]["success"], test_output["success"]
        )
        self.assertEqual(
            self.outputs[0]["execute_conts"], test_output["execute_conts"]
        )
        self.assertEqual(
            self.outputs[0]["command"], test_output["command"]
        )
        self.assertEqual(
            self.outputs[0]["stdout"], test_output["stdout"]["demo"]
        )
        self.assertEqual(
            self.outputs[0]["stderr"], None
        )
    """
    
    
    class_common = 'mock_sample.common.Common'
    method_params = class_common + '.get_input'
    method_execute_command = class_common + '.execute_command'
    method_log = class_common + '.log'

    
    @patch(method_log, return_value='dummy')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test01_ok_ls_demo_dir(self, params, execute, logger):
        
        def _get_input(_filename, _category):
            
            #self.test_input = {
            #    'hostname': '<ip_address>',
            #    'username': '<username>', 
            #    'password': '<password>', 
            #    'port': <port, e.g. 22>
            #    'key': '</path/.ssh/id_rsa>', 
            #    'allow_agent': False, 
            #    'look_for_keys': False, 
            #    'cmd_option': {
            #        'ls': 'demo/'
            #    },
            #}

            return self.test_input


        def _execute_command(_input, _command):
            _stdout = None
            _stderr = None

            if re.search(
                r'^\s*(ls)\s+(-la)\s+(demo\/)\s*$', _command):
                _stdout = ', '.join(response_true['stdout']['demo_la_opt'])
                _stdout = stdout.rstrip('\n')
            elif re.search(
                r'^\s*(ls)\s+(demo\/)\s*$', _command):
                _stdout = response_true['stdout']['demo']
                
            else:
                raise Error("_excute_command_error")
                
            
            return _stdout, _stderr

        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value


        self.outputs = self.obj.main()

        self.assertEqual(
            params.call_count, 1
        )
        self.assertEqual(
            execute.call_count, 1
        )
        self.assertEqual(
            logger.call_count, 1
        )
        
        params.assert_called_once_with('input.yml', 'sakura')
        execute.assert_called_once_with(self.test_input, 'ls demo/')
        logger.assert_called_once()


        self.assertEqual(
            len(self.outputs[0]), 6
        )
        self.assertIn(
            "2019", self.outputs[0]["timestamp"]
        )
        self.assertEqual(
            self.outputs[0]["success"], test_output["success"]
        )
        self.assertEqual(
            self.outputs[0]["execute_conts"], test_output["execute_conts"]
        )
        self.assertEqual(
            self.outputs[0]["command"], test_output["command"]
        )
        self.assertEqual(
            self.outputs[0]["stdout"], test_output["stdout"]['demo']
        )
        self.assertEqual(
            self.outputs[0]["stderr"], None
        )
    
    @patch(method_log, return_value='dummy')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test02_ok_ls_demo_la(self, params, execute, logger):
        
        def _get_input(_filename, _category):
            
            #self.test_input = {
            #    'hostname': '<ip_address>',
            #    'username': '<username>', 
            #    'password': '<password>', 
            #    'port': <port, e.g. 22>
            #    'key': '</path/.ssh/id_rsa>', 
            #    'allow_agent': False, 
            #    'look_for_keys': False, 
            #    'cmd_option': {
            #        'ls': 'demo/'
            #    },
            #}
            
            self.test_input.update({
                'cmd_option': {
                    'ls': '-la demo/'
                }
            })
            

            return self.test_input


        def _execute_command(_input, _command):
            _stdout = None
            _stderr = None

            if re.search(
                r'^\s*(ls)\s+(-la)\s+(demo\/)\s*$', _command):
                _stdout = ', '.join(response_true['stdout']['demo_la_opt'])
                _stdout = _stdout.rstrip('\n')
            elif re.search(
                r'^\s*(ls)\s+(demo\/)\s*$', _command):
                _stdout = response_true['stdout']['demo']
            else:
                raise Exception(response_false['stderr'])
                
            
            return _stdout, _stderr

        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value


        self.outputs = self.obj.main()

        self.assertEqual(
            params.call_count, 1
        )
        self.assertEqual(
            execute.call_count, 1
        )
        self.assertEqual(
            logger.call_count, 1
        )
        
        params.assert_called_once_with('input.yml', 'sakura')
        execute.assert_called_once_with(self.test_input, 'ls -la demo/')
        logger.assert_called_once()


        self.assertEqual(
            len(self.outputs[0]), 6
        )
        self.assertIn(
            "2019", self.outputs[0]["timestamp"]
        )
        self.assertEqual(
            self.outputs[0]["success"], test_output["success"]
        )
        self.assertEqual(
            self.outputs[0]["execute_conts"], test_output["execute_conts"]
        )
        self.assertEqual(
            self.outputs[0]["command"], 'ls -la demo/'
        )
        self.assertEqual(
            self.outputs[0]["stdout"], 
            ', '.join(test_output["stdout"]["demo_la_opt"]).lstrip('\n')
        )
        self.assertEqual(
            self.outputs[0]["stderr"], None
        )
    
    
    @patch(method_log, return_value='dummy')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test11_ng_ls_demo_dir(self, params, execute, logger):
        
        def _get_input(_filename, _category):
            
            #self.test_input = {
            #    'hostname': '<ip_address>',
            #    'username': '<username>', 
            #    'password': '<password>', 
            #    'port': <port, e.g. 22>
            #    'key': '</path/.ssh/id_rsa>', 
            #    'allow_agent': False, 
            #    'look_for_keys': False, 
            #    'cmd_option': {
            #        'ls': 'demo/'
            #    },
            #}

            return self.test_input


        def _execute_command(_input, _command):
            raise Exception(response_false['stderr'])


        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value

        self.outputs = self.obj.main()

        self.assertEqual(
            params.call_count, 1
        )
        self.assertEqual(
            execute.call_count, 4
        )
        self.assertEqual(
            logger.call_count, 1
        )
        
        params.assert_called_once_with('input.yml', 'sakura')
        execute.assert_called()
        logger.assert_called_once()

        self.assertEqual(
            len(self.outputs[0]), 6
        )
        self.assertIn(
            "2019", self.outputs[0]["timestamp"]
        )
        self.assertEqual(
            self.outputs[0]["success"], False
        )
        self.assertEqual(
            self.outputs[0]["execute_conts"], 4
        )
        self.assertEqual(
            self.outputs[0]["command"], test_output["command"]
        )
        self.assertEqual(
            self.outputs[0]["stdout"], None
        )
        self.assertIn(
            test_output["stderr"], self.outputs[0]["stderr"]
        )


if __name__ == '__main__': 
    import pdb; pdb.set_trace() 
    unittest.main()