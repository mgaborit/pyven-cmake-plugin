import zipfile, os
import cmake_plugin.constants

def zip_pvn():
    if not os.path.isdir(os.path.join(os.environ.get('PVN_HOME'), 'plugins')):
        os.makedirs(os.path.join(os.environ.get('PVN_HOME'), 'plugins'))
    zf = zipfile.ZipFile(os.path.join(os.environ.get('PVN_HOME'), 'plugins', 'cmake-plugin_' + cmake_plugin.constants.VERSION + '.zip'), mode='w')
    
    zf.write('__init__.py')
    
    zf.write('cmake_plugin/__init__.py')
    zf.write('cmake_plugin/constants.py')
    zf.write('cmake_plugin/parser.py')
    zf.write('cmake_plugin/cmake.py')
    
if __name__ == '__main__':
    zip_pvn()
