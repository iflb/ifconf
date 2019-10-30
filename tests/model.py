
from ifconf import configure_module, config_callback

@config_callback(section='server')
def configure(loader):
    loader.add_attr('server_addr', '0.0.0.0', help='server inet addr to bind')
    loader.add_attr_int('server_port', 8080, help='server inet port to bind')
    loader.add_attr_boolean('udp', False, help='True if use UDP otherwise TCP is used.')
    loader.add_attr_float('val_float', 0.8, help='float test value')
    loader.add_attr_dict('val_dict', {'a':1,'b':2,'c':3}, help='dict test value')
    loader.add_attr_list('val_list', [1,2,3], help='list test value')
    loader.add_attr_path('home', '../', help='path test value')

class Server:

    def __init__(self, conf = None):
        self.conf = configure_module(configure, conf)

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

    

