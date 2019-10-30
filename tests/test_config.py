# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest
from pathlib import Path

from ifconf import configure_main, clear_main_cofig, configure_module
import model

class TestConfigureModule(unittest.TestCase):

    def setUp(self):
        clear_main_cofig()
                            
    def test_default_value_load(self):
        configure_main()
        server = model.Server()
        self.assertEqual(server.addr, '0.0.0.0')
        self.assertEqual(server.port, 8080)
        self.assertEqual(server.udp, False)
        self.assertEqual(server.val_f, 0.8)
        self.assertEqual(server.val_d, {'a':1,'b':2,'c':3})
        self.assertEqual(server.val_l, [1,2,3])
        self.assertEqual(server.home, Path('..'))

    def test_file_path_value_load(self):
        configure_main(config_path=['test.ini'], config_arg=None)
        server = model.Server()
        self.assertEqual(server.addr, '127.0.0.1')
        self.assertEqual(server.port, 80)
        self.assertEqual(server.udp, True)
        self.assertEqual(server.val_f, 0.5)
        self.assertEqual(server.val_d, {'a':10,'b':20,'c':30})
        self.assertEqual(server.val_l, [1,2,3,4,5,6])
        self.assertEqual(server.home, Path('../../..'))

    def test_file_arg_value_load(self):
        configure_main(config_arg='test.ini')
        server = model.Server()
        self.assertEqual(server.addr, '127.0.0.1')
        self.assertEqual(server.port, 80)
        self.assertEqual(server.udp, True)
        self.assertEqual(server.val_f, 0.5)
        self.assertEqual(server.val_d, {'a':10,'b':20,'c':30})
        self.assertEqual(server.val_l, [1,2,3,4,5,6])
        self.assertEqual(server.home, Path('../../..'))

    def test_no_main_config(self):
        with self.assertRaises(RuntimeError):
            configure_module(model.configure)

if __name__ == '__main__':
    unittest.main()

