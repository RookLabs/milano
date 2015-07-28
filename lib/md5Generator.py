import os
import stat
import hashlib

class Md5Generator(object):
    def compute_md5(self, file_path):
        m = hashlib.md5()
        with os.fdopen(os.open(file_path, (os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW))) as f:
            for chunk in iter(lambda: f.read(hashlib.md5().block_size * 512), b''):
                m.update(chunk)

        return m.hexdigest()

if __name__ == "__main__":
    g = Md5Generator()
    print '/dev/urandom md5 -> {}'.format(g.compute_md5('/dev/urandom'))
    print '/boot/vmlinuz-3.16.0-43-generic md5 -> {}'.format(g.compute_md5('/boot/vmlinuz-3.16.0-43-generic'))
