# Integrated Framework for Configuration

Alternative configuration framework using argparse and configparser.
Designed for the following purposes.

* Integration of command line args and configuration files
* Generation of default configuration files
* Class initialization procedure using parameter object pattern

## SAMPLE

* main.py 

        from ifconf import configure_main
        if __name__ == "__main__":
                configure_main()

* server.py
        
        from ifconf import configure_module, config_callback
        
        @config_callback(section='server')
        def conf(loader):
            loader.add_attr('server_addr', '0.0.0.0', help='server inet addr to bind')
                loader.add_attr_int('server_port', 8080, help='server inet port to bind')
                loader.add_attr_boolean('udp', False, help='True if use UDP otherwise TCP is used.')
                loader.add_attr_float('val_float', 0.8, help='float test value')
                loader.add_attr_dict('val_dict', {'a':1,'b':2,'c':3}, help='dict test value')
                loader.add_attr_list('val_list', [1,2,3], help='list test value')
                loader.add_attr_path('home', '../', help='path test value')
        
        class MyClass:
                def __init__(self):
                        self.conf = configure_module(conf)
                        self.addr = self.conf.addr
                        self.port = self.conf.port
                        self.conf.logger.info(self.conf)
        
* config.ini

        [server_conf]
        #addr = 0.0.0.0
        port = 8888


## config file generation

You can print config.ini template

        python -m ifconf server.config


----

This is the README file for the project.

The file should use UTF-8 encoding and can be written using
[reStructuredText][rst] or [markdown][md use] with the appropriate [key set][md
use]. It will be used to generate the project webpage on PyPI and will be
displayed as the project homepage on common code-hosting services, and should be
written for that purpose.

Typical contents for this file would include an overview of the project, basic
usage examples, etc. Generally, including the project changelog in here is not a
good idea, although a simple “What's New” section for the most recent version
may be appropriate.

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/pypa/sampleproject
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
