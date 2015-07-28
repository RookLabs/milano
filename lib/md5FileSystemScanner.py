import os
import stat
from resultsWriter import Results
from resultsWriter import PotentialFile
import ntpath
from time import sleep

class Md5FileSystemScanner(object):
    def __init__(self, md5Generator, fileSystemListGeneratorProvider, iocReader, logger):
        self.md5Generator = md5Generator
        self.fileSystemListGeneratorProvider = fileSystemListGeneratorProvider
        self.iocReader = iocReader
        self.logger = logger

        self.suspect_files = iocReader.get_suspect_filenames()


    def scan_file_system(self):
        results = Results()

        self.fileSystemListGeneratorProvider.prompt_for_paths_to_scan()

        self.logger.info('')
        self.logger.info('Commencing scan...\n')
        sleep(2)

        results.start()

        pathGenerator = self.fileSystemListGeneratorProvider.get_generator()
        for path in pathGenerator:
            try:
                if self.should_scan_file(path):
                    self.logger.info('Checking: ' + path)
                    my_md5 = self.md5Generator.compute_md5(path)
                    if self.iocReader.has_md5(my_md5):
                        self.logger.info('    Detected potentially malicious file at path: ' + path)
                        potential_category = self.iocReader.get_potential_category(my_md5)
                        source_ioc = self.iocReader.get_source_ioc(my_md5)
                        results.detected_file_paths.append(PotentialFile(path, potential_category, source_ioc))

            except IOError, err:
                # Socket error possibly
                # TODO - log these errors.
                pass
            except OSError, err:
                # File doesn't exist
                # TODO - log these errors.
                pass

        results.finish()
        return results


    def should_scan_file(self, path):
        st = os.lstat(path)
        if stat.S_ISREG(st.st_mode):
            return True

        return False


if __name__ == '__main__':
    fileSystemScanner = MD5FileSystemScanner()
    fileSystemScanner.scan_file_system()
