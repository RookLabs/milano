#!/usr/bin/python

import argparse
import os
from lib.logger import get_logger
from lib.new_iocReader import IocReader
from lib.md5FileSystemScanner import Md5FileSystemScanner
from lib.fileSystemListGeneratorProvider import FileSystemListGeneratorProvider
from lib.md5Generator import Md5Generator
from lib.resultsWriter import ResultsWriter, Results
from lib.iocBundleDownloader import IocBundleDownloader

logger = get_logger()


class Main(object):
    ioc_hashes_file = 'openioc/downloaded/openioc_1.1/ht_ioc_1-1_WithParams.ioc'

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Sentinel scans for and reports the presence of malware-related and malware-modified files.')

        md5Generator = Md5Generator()
        fileSystemListGeneratorProvider = FileSystemListGeneratorProvider()
        iocReader = IocReader(Main.ioc_hashes_file)
        self.fileSystemScanner = Md5FileSystemScanner(md5Generator, fileSystemListGeneratorProvider, iocReader, logger)

        self.resultsWriter = ResultsWriter(logger)


    def execute(self):
        app.process_arguments()

        app.print_logo()

        logger.info('')
        raw_input('Press enter to continue...')

        logger.info('')
        app.print_legal()

        logger.info('')
#        should_update_ioc_bundle_and_contents = (raw_input('Download updated OpenIOC files? [Y/n] ').lower() == 'y')
#        if should_update_ioc_bundle_and_contents:
#            ioc_bundle_downloader = IocBundleDownloader('http://**********/milano_openioc_bundle.tar.gz')
#            ioc_bundle_downloader.conditionally_update_bundle_and_contents()

        results = self.fileSystemScanner.scan_file_system()

        self.resultsWriter.write_results(results)

        logger.info('')
        logger.info('Results will be printed to ./last_scan_results.txt')

        logger.info('')
        raw_input('Press enter to exit...')


    def process_arguments(self):
        args = self.parser.parse_args()


    def print_from_file(self, file_path, prefix=''):
        f = open(file_path)
        for line in f:
            logger.info(prefix + line.rstrip())
        f.close()


    def print_logo(self):
        logger.info('===============================================================================')
        self.print_from_file('logo.txt')
        logger.info('')
        self.print_from_file('version.txt', ' ' * 32)
        logger.info('')
        logger.info('                           Powered by Rook Security')
        logger.info('===============================================================================')
        logger.info('')
        logger.info('Copyright 2015 Rook Security, LLC. All rights reserved.')


    def print_legal(self):
        self.print_from_file('LEGAL.txt')


if __name__ == '__main__':
    app = Main()
    app.execute()
