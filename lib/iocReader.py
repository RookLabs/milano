from openIOC import *
from lib.logger import get_logger
import os 

logger = get_logger()

class IocReader(object):
    Filename,Category,Reference,SHA1,MD5,SHA256 = (0,1,2,3,4,5)

    def __init__(self, ioc_filepath):
        self.ioc_filepath = ioc_filepath
        self.iocData = self.load_ioc_data()

    def load_ioc_data(self):
        data = []
        for path, subdirs, files in os.walk(self.ioc_filepath):
            for filename in files:
                fpath = os.path.join(path, filename)

                # future validation purposes, 1.1 validator/xsd in root of openico/
                if 'user-added' in fpath and '.ioc' in fpath:
                    if '1.1' in fpath:
                        try:
                            reader = OpenIOC(fpath)
                            data.append(reader.parse())
                        except:
                            
                            logger.info("\n============= ERROR =============\n")
                            logger.info("Invalid ioc file -> " + fpath)
                            logger.info("\n=================================\n")
                            exit(1)
                    else:
                        try:
                            reader = OpenIOC(fpath)
                            data.append(reader.parse())
                        except:
                            logger.info("\n============= ERROR =============\n")
                            logger.info("Invalid ioc file -> " + fpath)
                            logger.info("\n=================================\n")
                            exit(1)

                if 'downloaded' in fpath and '1.1' in fpath and '.ioc' in fpath:
                    try:
                        reader = OpenIOC(fpath)
                        data.append(reader.parse())
                    except:
                            logger.info("\n============= ERROR =============\n")
                            logger.info("Invalid ioc file -> " + fpath)
                            logger.info("\n=================================\n")
                            exit(1)
        return data

    def has_md5(self, md5):
        results = [ row for row in self.iocData if row[IocReader.MD5] == md5 ]
        return len(results) > 0

    def get_potential_category(self, md5):
        results = [ row for row in self.iocData if row[IocReader.MD5] == md5 ]
        return results[0][IocReader.Category]

    def get_suspect_filenames(self):
        filenames = []
        for row in self.iocData:
            for item in row:
                filenames.append(item[0])
        # removed duplicates
        return list(set(filenames))
