from openIOC import *

class IocReader(object):
    Filename,Category,Reference,SHA1,MD5,SHA256 = (0,1,2,3,4,5)

    def __init__(self, ioc_filepath):
        self.iocData = self.load_ioc_data()


    def load_ioc_data(self):
        data = []
        reader = OpenIOC('./openioc/downloaded/openioc_1.1/ht_ioc_1-1_WithParams.ioc')
        data = reader.parse()
        # for row in res:
        #     data.append(row)
        print data
        return data


    def has_md5(self, md5):
        results = [ row for row in self.iocData if row[IocReader.MD5] == md5 ]
        return len(results) > 0


    def get_potential_category(self, md5):
        results = [ row for row in self.iocData if row[IocReader.MD5] == md5 ]
        return results[0][IocReader.Category]


    def get_suspect_filenames(self):
        filenames = [ row[IocReader.Filename].lower() for row in self.iocData ]
        return filenames
