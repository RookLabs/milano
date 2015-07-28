import os
import stat
import hashlib

class Md5Generator(object):
    def compute_md5(self, file_path):
        m = hashlib.md5()
        with os.fdopen(os.open(file_path, (os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)), 'rb', 0) as f:
            for chunk in iter(lambda: f.read(hashlib.md5().block_size * 128), b''):
                m.update(chunk)

        return m.hexdigest()

if __name__ == "__main__":
    g = Md5Generator()
    print g.compute_md5('/dev/urandom')
