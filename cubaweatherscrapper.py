#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imp
import inspect
import logging
import os
import sys

import atexit
from logging import Logger

APP_NAME = "cubaweather-scrapper"

PID_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mailproc.pid")

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "services"))

__SERVICES_FOLDER__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "services")

class CubaweatherScrapperProcessor:

    def __init__(self):
        self.process_run()

        # folders
        self.system_service_folder = __SERVICES_FOLDER__
        self.service_folder = [self.system_service_folder]

        # services main service name
        self.main_service = "__init__"

        # create folders if don't exist
        if not os.path.exists(self.system_service_folder):
            os.makedirs(self.system_service_folder)

    def process_run(self):

        pid = str(os.getpid())
        pid_file = PID_FILE

        if os.path.isfile(pid_file):
            print("%s already exists, exiting" % pid_file)
            sys.exit()
        else:
            with open(pid_file, 'w+') as pid_f:
                pid_f.write(pid)


        atexit.register(self.process_exit, pid_file)

    def process_exit(self, pid_file):
        os.unlink(pid_file)

    def get_services(self):
        """
        Obtain services from folders
        :return: List of available services info
        """
        services = []
        for folder in self.service_folder:
            possible_services = os.listdir(folder)
            for i in possible_services:
                location = os.path.join(folder, i)
                if not os.path.isdir(location) or not self.main_service + ".py" in os.listdir(location):
                    continue
                info = imp.find_module(self.main_service, [location])
                services.append({"name": i, "info": info})
        return services

    def load_service(self, service):
        """
        Get service main service
        :return: Service main service
        """
        return imp.load_module(self.main_service, *service["info"])

    def call_services(self):
        """
        Services callback
        """
        for i in self.get_services():
            service = self.load_service(i)
            service.run()

class CubaweatherScrapper:

    __service_name__: str = 'Default'
    __service_version__: str = None

    logger: Logger = None
    logger_level: int = logging.WARNING

    def __init__(self):
        self._init_logger()

    def _init_logger(self):
        if not self.logger:
            self.logger = logging.getLogger(self.__service_name__)
            fh = logging.FileHandler(os.path.join(self.get_service_path(), 'service.log'))
            self.logger.addHandler(fh)
            self.logger.setLevel(self.logger_level)

    def get_service_path(self) -> str:
        return os.path.dirname(inspect.getfile(self.__class__))

def add(service_name):
    service_name_upper_camel_case = service_name.title().replace(' ','')
    service_name_camel_case = service_name.lower().replace(' ','_')
    service_file = os.path.join(__SERVICES_FOLDER__, service_name_camel_case)
    if not os.path.exists(service_file):
        os.makedirs(service_file)

    init_file_template = """# -*- coding: utf-8 -*-

def run():
    from %s.service import %s
    srv = %s()
    srv.run()""" % (service_name_camel_case, service_name_upper_camel_case, service_name_upper_camel_case)

    init_file_path = os.path.join(service_file, '__init__.py')
    init_file = open(init_file_path, 'w+')
    init_file.write(init_file_template)

    service_file_template = """# -*- coding: utf-8 -*-

from cubaweatherscrapper import CubaweatherScrapper

__service_name__ = '%s'
__service_version__ = '0.1'

class %s(CubaweatherScrapper):
    
    # service info
    __service_name__ = __service_name__
    __service_version__ = __service_version__

    def __init__(self):
        
        # init framework parent class
        CubaweatherScrapper.__init__(self)

    def run(self):
        print('Hello World {name}'.format(name=__service_name__))
""" % (service_name, service_name_upper_camel_case)

    service_file_path = os.path.join(service_file, 'service.py')
    service_file = open(service_file_path, 'w+')
    service_file.write(service_file_template)

def main():

    prog = APP_NAME
    version = '%(prog)s 0.0.1'
    description = 'Cubaweather Scrapper services.'
    epilog = version+' - (C) 2020 xxxxxxxx.'

    import argparse

    parser = argparse.ArgumentParser(prog=prog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=description,
                                     epilog=epilog)

    parser.add_argument('--version', action='version', version=version,
                        help='show program\'s version number and exit')
    parser.add_argument('-a', '--add', action='store', default=False, dest='add',
                        metavar="'Service name'",
                        help='Create a new service base template')

    args = parser.parse_args()

    start(args)


def start(args):
    if args.add:
        add(args.add)
    else:
        cws_proc = CubaweatherScrapperProcessor()
        cws_proc.call_services()

if __name__ == '__main__':
    main()