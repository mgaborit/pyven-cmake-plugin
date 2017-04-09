import os, subprocess, time, shutil
import pyven.constants

from pyven.plugins.plugin_api.process import Process

from pyven.logging.logger import Logger
from pyven.results.block_logs_parser import BlockLogsParser

class CMake(Process):

    def __init__(self, cwd, name, generator, output_path, definitions):
        super(CMake, self).__init__(cwd, name)
        self.duration = 0
        self.type = 'cmake'
        self.target_generator = generator
        self.output_path = output_path
        self.definitions = definitions
        self.parser = BlockLogsParser(begin_error_patterns=['-- Configuring incomplete, errors occurred!'],\
                                    end_error_patterns=[],\
                                    begin_warning_patterns=[],\
                                    end_warning_patterns=[])
    
    def process(self, verbose=False, warning_as_error=False):
        Logger.get().info('CMake : ' + self.type + ':' + self.name)
        self.duration, out, err, returncode = self._call_command(self._format_call())
        
        if verbose:
            for line in out.splitlines():
                Logger.get().info('[' + self.type + ']' + line)
            for line in err.splitlines():
                Logger.get().info('[' + self.type + ']' + line)
        
        self.parser.parse(out.splitlines() + err.splitlines())
        self.warnings = self.parser.warnings
        
        if returncode != 0:
            self.status = pyven.constants.STATUS[1]
            self.errors = self.parser.errors
            Logger.get().error('CMake failed : ' + self.type + ':' + self.name)
        else:
            self.status = pyven.constants.STATUS[0]
        return returncode == 0
    
    def clean(self, verbose=False):
        Logger.get().info('Cleaning : ' + self.type + ':' + self.name)
        if os.path.isdir(os.path.join(self.cwd, self.output_path)):
            shutil.rmtree(os.path.join(self.cwd, self.output_path))
        return True
        
    def report_summary(self):
        return self.report_title()
    
    def report_title(self):
        return self.name
        
    def report_properties(self):
        properties = []
        properties.append(('Generator', self.target_generator))
        properties.append(('Duration', str(self.duration) + ' seconds'))
        return properties
        
    def _call_command(self, command):
        tic = time.time()
        out = ''
        err = ''
        try:
            
            sp = subprocess.Popen(command,\
                                  stdin=subprocess.PIPE,\
                                  stdout=subprocess.PIPE,\
                                  stderr=subprocess.PIPE,\
                                  universal_newlines=True,\
                                  cwd=self.cwd,\
                                  shell=pyven.constants.PLATFORM == pyven.constants.PLATFORMS[1])
            out, err = sp.communicate(input='\n')
            returncode = sp.returncode
        except FileNotFoundError as e:
            returncode = 1
            self.errors.append(['Unknown command'])
        toc = time.time()
        return round(toc - tic, 3), out, err, returncode
        
    def _format_call(self):
        call = [self.type, '-H.', '-B'+self.output_path, '-G']
        if pyven.constants.PLATFORM == 'windows':
            call.append(self.target_generator)
        elif pyven.constants.PLATFORM == 'linux':
            call.append('"'+self.target_generator+'"')
        for definition in self.definitions:
            call.append('-D'+definition)
        if pyven.constants.PLATFORM == 'linux':
            call = [' '.join(call)]
        Logger.get().info(' '.join(call))
        return call
        