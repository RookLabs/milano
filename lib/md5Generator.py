import os
import hashlib
from lib.logger import get_logger

logger = get_logger()

class Md5Generator(object):
    def compute_md5(self, file_path):
        m = hashlib.md5()

        fd = -1
        if os.name == 'posix':
            fd = os.open(file_path, (os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW))
        else:
            fd = os.open(file_path, os.O_RDONLY)

        with os.fdopen(fd) as f:
            for chunk in iter(lambda: f.read(hashlib.md5().block_size * 512), b''):
                m.update(chunk)

        return m.hexdigest()

if __name__ == "__main__":
    g = Md5Generator()
    logger.info('/dev/urandom md5 -> {}'.format(g.compute_md5('/dev/urandom')))
    logger.info('/boot/vmlinuz-3.16.0-43-generic md5 -> {}'.format(g.compute_md5('/boot/vmlinuz-3.16.0-43-generic')))
