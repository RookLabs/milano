import hashlib
from functools import partial

class Md5Generator(object):
    def compute_md5(self, file_path):
        m = hashlib.md5()
        with open(file_path, 'rb', buffering=-1) as f:
            for chunk in iter(lambda: f.read(hashlib.md5().block_size * 128), b''):
                m.update(chunk)

        return m.hexdigest()

#class Md5Generator(object):
#    def compute_md5(self, file_path):
#        f = open(file_path, "rb+")
#
#        m = hashlib.md5()
#        for chunk in iter(lambda: f.read(hashlib.md5().block_size * 128), b''):
#            m.update(chunk)
#
#        f.close()
