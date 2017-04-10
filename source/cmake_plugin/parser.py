from pyven.exceptions.parser_exception import ParserException
from pyven.plugins.plugin_api.parser import Parser

from cmake_plugin.cmake import CMake

class CMakeParser(Parser):
    COUNT = 0
    SINGLETON = None
    
    def __init__(self, cwd):
        CMakeParser.COUNT += 1
        super(CMakeParser, self).__init__(cwd)
    
    def parse(self, node, project):
        objects = []
        members = self.parse_process(node)
        errors = []
        generator_node = node.find('generator')
        if generator_node is None:
            errors.append('Missing CMake generator')
        else:
            generator = generator_node.text
        output_path_node = node.find('output-path')
        if output_path_node is None:
            errors.append('Missing CMake output directory path')
        else:
            output_path = output_path_node.text
        definitions = []
        for definition in node.xpath('definitions/definition'):
            definitions.append(definition.text)
        if len(errors) > 0:
            e = ParserException('')
            e.args = tuple(errors)
            raise e
        objects.append(CMake(self.cwd, members[0], generator, output_path, definitions))
        return objects
        
def get(cwd):
    if CMakeParser.COUNT <= 0 or CMakeParser.SINGLETON is None:
        CMakeParser.SINGLETON = CMakeParser(cwd)
    CMakeParser.SINGLETON.cwd = cwd
    return CMakeParser.SINGLETON