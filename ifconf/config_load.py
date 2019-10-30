# -*- coding: utf-8 -*-

import collections
from collections import namedtuple
from recordclass import recordclass

import logging

from ifconf.config import Config

from ifconf.config_print import PrintConfigAction
from ifconf.config_logging import configure_logging

__MAIN_CONFIG__ = None

def config_callback(section = None):
    def _decorator(func):
        if hasattr(func, '__SECTION__'):
            return func
        if func.__module__  == '__main__':
            try:
                func.__MODULE_NAME__ = os.path.splitext(os.path.basename(sys.modules['__main__'].__file__))[0]
            except:
                func.__MODULE_NAME__ = os.path.splitext(os.path.basename(sys.executable))[0]
        else:
            func.__MODULE_NAME__ = func.__module__
        func.__SECTION__ = '_'.join((func.__MODULE_NAME__, str(section) if section else func.__name__))
        return func
    return _decorator

def configure_main(argparser = None
                   , with_default_args = True
                   , config_arg = 'config.ini'
                   , config_path = []
                   , with_config_logging = True
                   , callback_methods = []):
    global __MAIN_CONFIG__
    __MAIN_CONFIG__ = Config(argparser)
    callback_methods = callback_methods if hasattr(callback_methods, '__iter__') else [callback_methods]
    callback_methods = [config_callback()(m) for m in callback_methods]
    if with_default_args:
        add_default_argument(__MAIN_CONFIG__.argparser, config_arg)
        PrintConfigAction.set_callback_methods(callback_methods)
    __MAIN_CONFIG__.parse(config_path)
    if with_config_logging:
        configure_logging(__MAIN_CONFIG__)
    for m in callback_methods:
        loader = ConfigLoader.load(m, __MAIN_CONFIG__)
        try:
            loader.configure()
        except Exception as e:
            __MAIN_CONFIG__.err.append('モジュール[{}]の設定取得に失敗しました。エラー：{}'.format(loader.section, e))
    for e in __MAIN_CONFIG__.err:
        __MAIN_CONFIG__.logger.warning(e)
    __MAIN_CONFIG__.logger.info('設定が完了しました。設定ファイル：{}'.format(__MAIN_CONFIG__.config_path))
    return __MAIN_CONFIG__

def configure_main_custom(argparser = None):
    global __MAIN_CONFIG__
    __MAIN_CONFIG__ = Config(argparser)
    return __MAIN_CONFIG__

def clear_main_cofig():
    global __MAIN_CONFIG__
    __MAIN_CONFIG__ = None

def configure_module(callback_methods
                     , config = None
                     , immutable = True):
    if config:
        config = config
    elif __MAIN_CONFIG__:
        config = __MAIN_CONFIG__
    else:
        raise RuntimeError('Main configuration must be done before calling configure_module.')
    if hasattr(callback_methods, '__iter__'):
        return [ConfigLoader.load(config_callback()(callback), config).configure(immutable) for callback in callback_methods]
    else:
        return ConfigLoader.load(config_callback()(callback_methods), config).configure(immutable)



def add_default_argument(argparser, config_path = None):
    if config_path is not None:
        argparser.add_argument('-c', '--config'
                               , metavar='PATH'
                               , default=config_path
                               , help='設定ファイルへのパス')
    argparser.add_argument('--verbose', '-v'
                           , action='count'
                           , default=False
                           , help='詳細なデータを出力')
    argparser.add_argument('--current_dir'
                           , default='.'
                           , help='カレントディレクトリを指定して実行')
    argparser.add_argument('--debug'
                           , action="store_true"
                           , default=False
                           , help='デバグモードで実行')
    argparser.add_argument('--debug_file'
                           , metavar='FILE'
                           , help='デバグモードで実行しファイル出力')
    argparser.add_argument('--print_conf'
                           , action=PrintConfigAction
                           , default=False
                           , help='設定ファイルの内容を出力')
    return argparser

    

class ConfigLoader:
    
    @classmethod
    def load(cls, callback_method, config):
        assert callback_method is not None, 'callback_method cannot be null.'
        assert hasattr(callback_method, '__MODULE_NAME__'), 'MODULE_NAME must be set for callback_method.'
        assert hasattr(callback_method, '__SECTION__'), 'SECTION must be set for callback_method.'
        loader = ConfigLoader(callback_method.__SECTION__, callback_method.__MODULE_NAME__, config)
        callback_method(loader)
        return loader
        
    def __init__(self, section, module_name, config):
        assert section is not None, 'section cannot be null.'
        assert module_name is not None, 'module_name cannot be null.'
        assert config is not None, 'config cannot be null.'
        assert type(config) is Config, 'invalid config type:[{}]'.format(type(config))
        self.section = section
        self.main_config = config
        self.names = ['main_config', 'logger']
        self.values = [lambda config: config, lambda config: logging.getLogger(module_name)]

    def configure(self, immutable):
        assert self.main_config is not None, 'main_config cannot be null.'
        ntp = namedtuple(self.section.replace('.','_'), self.names) if immutable else recordclass(self.section.replace('.','_'), self.names) 
        args = [f(self.main_config) for f in self.values]
        conf = ntp(*args)
        conf.logger.debug(conf)
        return conf

    def add_attr(self, name, default=None, required=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr(self.section, name, default, required))

    def add_attr_boolean(self, name, default=False, required=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_boolean(self.section, name, default, required))

    def add_attr_int(self, name, default=0, required=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_int(self.section, name, default, required))

    def add_attr_float(self, name, default=0.0, required=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_float(self.section, name, default, required))

    def add_attr_dict(self, name, default={}, required=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_dict(self.section, name, default, required))
        
    def add_attr_list(self, name, default=[], required=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_list(self.section, name, default, required))
        
    def add_attr_path(self, name, default=None, required=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_path(self.section, name, default, required))

