from distutils.core import setup
import py2exe
import shutil
import os

src = "dist"
dst = "win32"

if os.path.isdir(dst):
    shutil.rmtree(dst)
os.makedirs(dst)

# setup(console=['milano.py'])
setup(
    console=[{'script': 'milano.py'}],
    options={
        'py2exe':
        {
            'includes': ['lxml.etree', 'lxml._elementpath', 'gzip'],
        }
    }
)

files = os.listdir(src)
for file in files:
    full_file_name = os.path.join(src, file)
    if (os.path.isfile(full_file_name)):
        shutil.copy2(full_file_name, dst)

shutil.copytree('openioc', 'win32\\openioc', False, None)
shutil.copy2('logo.txt', 'win32\\logo.txt')
shutil.copy2('milano.cfg', 'win32\\milano.cfg')
shutil.copy2('LEGAL.txt', 'win32\\LEGAL.txt')
shutil.copy2('version.txt', 'win32\\version.txt')
