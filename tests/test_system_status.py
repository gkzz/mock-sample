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
from mock_sample.system_status import Demo

#https://cpython-test-docs.readthedocs.io/en/latest/library/unittest.mock.html


### load yam
def load_yaml(filename, category):
    dict = {}
    for key, value in yaml.safe_load(open(filename))[category].iteritems():
        dict[key] = value
    
    return dict

test_output = load_yaml(config_dir  + '/test_output.yml', 'system')
response = load_yaml(config_dir  + '/response.yml', 'system')
response_true = response['true']
response_false = response['false']


class TestSytemStatus(unittest.TestCase):

    def setUp(self):
        # Read yml file
        self.test_input = load_yaml(
            config_dir  + '/test_input.yml', 'sakura'
        )

    def tearDown(self):
        self.test_input = None
        self.outputs = None

    
    """
    def test001_nomock_httpd(self):
        #service = "httpd"
        service = "firewalld"
        # Set Object
        self.obj = Demo(service)

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
            self.outputs[0]["command"], 
            "{base} {service} | grep Active".format(
                base=test_output["command"],
                service=service
            )
        )
        self.assertIn(
            "Active: active (running)",
            self.outputs[0]["stdout"]
        )
        self.assertEqual(
            self.outputs[0]["stderr"], None
        )
    

    def test002_nomock_firewalld(self):
        service = "firewalld"
        # Set Object
        self.obj = Demo(service)

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
            self.outputs[0]["command"], 
            "{base} {service} | grep Active".format(
                base=test_output["command"],
                service=service
            )
        )
        self.assertIn(
            "Active: active (running)",
            self.outputs[0]["stdout"]
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
    def test011_ok_httpd(self, params, execute, logger):
        service = "httpd"
        
        def _get_input(_filename, _category):
            #test_input = load_yaml(
            #    config_dir  + '/test_input.yml', 'sakura'
            #)
            
            #self.test_input = {
            #    'hostname': '<ip_address>',
            #    'username': '<username>', 
            #    'password': '<password>', 
            #    'port': <port, e.g. 22>
            #    'key': '</path/.ssh/id_rsa>', 
            #    'allow_agent': False, 
            #    'look_for_keys': False, 
            #    'cmd_option': {
            #        'systemctl': '| grep Active'
            #    },
            #}

            self.test_input.update({
                'cmd_option': {
                    'systemctl': '| grep Active'
                }
            })

            return self.test_input


        def _execute_command(_input, _command):
            _stdout = None
            _stderr = None
            
            _stdout = response_true['stdout']['active']
            #raise Error("_excute_command_error")
            
            return _stdout, _stderr

        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value


        # Set Object
        self.obj = Demo(service)
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
        execute.assert_called_once_with(
            self.test_input, 
            '{base} {service} | grep Active'.format(
                base=test_output["command"],
                service=service
            )
        )
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
            self.outputs[0]["command"], 
            "{base} {service} | grep Active".format(
                base=test_output["command"],
                service=service
            )
        )
        self.assertEqual(
            self.outputs[0]["stdout"], test_output["stdout"]['active']
        )
        self.assertEqual(
            self.outputs[0]["stderr"], None
        )
    
    @patch(method_log, return_value='dummy')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test012_ok_firewalld(self, params, execute, logger):
        service = "firewalld"
        
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
            #        'systemctl': '| grep Active'
            #    },
            #}
            
            self.test_input.update({
                'cmd_option': {
                    'systemctl': '| grep Active'
                }
            })
            

            return self.test_input


        def _execute_command(_input, _command):
            _stdout = None
            _stderr = None

            _stdout = response_true['stdout']['active']
            #raise Error("_excute_command_error")
            
            return _stdout, _stderr

        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value


        # Set Object
        self.obj = Demo(service)
        self.outputs = self.obj.main()

        self.assertEqual(
            params.call_count, 1
        )
        self.assertEqual(
            execute.call_count, 3
        )
        self.assertEqual(
            logger.call_count, 1
        )
        
        params.assert_called_once_with('input.yml', 'sakura')
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
            self.outputs[0]["execute_conts"], 3
        )
        self.assertEqual(
            self.outputs[0]["command"], 
            "{base} {service} | grep Active".format(
                base=test_output["command"],
                service=service
            )
        )
        self.assertEqual(
            self.outputs[0]["stdout"], test_output["stdout"]['active']
        )
        self.assertEqual(
            self.outputs[0]["stderr"], None
        )


    @patch(method_log, return_value='dummy')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test013_ok_restart_httpd(self, params, execute, logger):
        service = "httpd"
        
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
            #        'systemctl': '| grep Active'
            #    },
            #}
            
            self.test_input.update({
                'cmd_option': {
                    'systemctl': '| grep Active'
                }
            })
            

            return self.test_input


        def _execute_command(_input, _command):
            _stdout = None
            _stderr = None

            if execute.call_count == 1:
                _stdout = response_true['stdout']['inactive']
            elif execute.call_count == 2:
                _stdout = response_true['stdout']['restart']
            elif execute.call_count == 3:
                _stdout = response_true['stdout']['active']
            else:
                raise Error("_excute_command_error")
            
            return _stdout, _stderr

        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value


        # Set Object
        self.obj = Demo(service)
        self.outputs = self.obj.main()

        self.assertEqual(
            params.call_count, 1
        )
        self.assertEqual(
            execute.call_count, 3
        )
        self.assertEqual(
            logger.call_count, 1
        )
        
        params.assert_called_once_with('input.yml', 'sakura')
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
            self.outputs[0]["execute_conts"], 3
        )
        self.assertEqual(
            self.outputs[0]["command"], 
            "{base} {service} | grep Active".format(
                base=test_output["command"],
                service=service
            )
        )
        self.assertEqual(
            self.outputs[0]["stdout"], test_output["stdout"]['active']
        )
        self.assertEqual(
            self.outputs[0]["stderr"], None
        )



    @patch(method_log, return_value='dummy')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test013_ok_restart_firewalld(self, params, execute, logger):
        service = "firewalld"
        
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
            #        'systemctl': '| grep Active'
            #    },
            #}
            
            self.test_input.update({
                'cmd_option': {
                    'systemctl': '| grep Active'
                }
            })
            

            return self.test_input


        def _execute_command(_input, _command):
            _stdout = None
            _stderr = None

            if execute.call_count == 1:
                _stdout = response_true['stdout']['inactive']
            elif execute.call_count == 2:
                _stdout = response_true['stdout']['restart']
            elif execute.call_count == 3:
                _stdout = response_true['stdout']['active']
            else:
                raise Error("_excute_command_error")
            
            return _stdout, _stderr

        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value


        # Set Object
        self.obj = Demo(service)
        self.outputs = self.obj.main()

        self.assertEqual(
            params.call_count, 1
        )
        self.assertEqual(
            execute.call_count, 3
        )
        self.assertEqual(
            logger.call_count, 1
        )
        
        params.assert_called_once_with('input.yml', 'sakura')
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
            self.outputs[0]["execute_conts"], 3
        )
        self.assertEqual(
            self.outputs[0]["command"], 
            "{base} {service} | grep Active".format(
                base=test_output["command"],
                service=service
            )
        )
        self.assertEqual(
            self.outputs[0]["stdout"], test_output["stdout"]['active']
        )
        self.assertEqual(
            self.outputs[0]["stderr"], None
        )
    
    
    @patch(method_log, return_value='dummy')
    @patch(method_execute_command) 
    @patch(method_params) 
    def test11_ng_raise_httpd(self, params, execute, logger):
        service = "httpd"
        
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
            #        'systemctl': '| grep Active'
            #    },
            #}
            
            self.test_input.update({
                'cmd_option': {
                    'systemctl': '| grep Active'
                }
            })

            return self.test_input


        def _execute_command(_input, _command):
            raise Exception(response_false['stderr'])


        params.side_effect = _get_input
        execute.side_effect = _execute_command
        logger.return_value

        # Set Object
        self.obj = Demo(service)
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
    unittest.main()