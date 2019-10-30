

from ifconf import configure_module, config_callback

@config_callback
def server(loader):
    loader.add_attr('server_addr', '0.0.0.0', help='server inet addr to bind')
    loader.add_attr_int('server_port', 8080, help='server inet port to bind')
    loader.add_attr_boolean('udp', False, help='True if use UDP otherwise TCP is used.')
    loader.add_attr_float('val_float', 0.8, help='float test value')
    loader.add_attr_dict('val_dict', {'a':1,'b':2,'c':3}, help='dict test value')
    loader.add_attr_list('val_list', [1,2,3], help='list test value')
    loader.add_attr_path('home', '../', help='path test value')

class Server:

    def __init__(self, conf = None):
        self.conf = configure_module(server, conf)

    @property 
    def addr(self):
        return self.conf.server_addr

    @property 
    def port(self):
        return self.conf.server_port

    @property 
    def udp(self):
        return self.conf.udp

    @property 
    def val_f(self):
        return self.conf.val_float

    @property 
    def val_d(self):
        return self.conf.val_dict

    @property 
    def val_l(self):
        return self.conf.val_list

    @property 
    def home(self):
        return self.conf.home

    
    
@config_callback(section='database')
def conf_database(loader):
    loader.add_attr('service_addr', '127.0.0.1', help='database server inet addr to connect')
    loader.add_attr_int('service_port', 3306, help='server inet port to connect')
    loader.add_attr('test', 'value', help='test value')

class Database:

    def __init__(self, conf = None):
        self.conf = configure_module(conf_database, conf, immutable=False)

    @property 
    def addr(self):
        return self.conf.service_addr

    @addr.setter
    def addr(self, addr):
        self.conf.service_addr = addr

    @property 
    def port(self):
        return self.conf.service_port

    @port.setter
    def port(self, port):
        self.conf.service_port = port

