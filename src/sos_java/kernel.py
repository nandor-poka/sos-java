from ._version import __version__
from sos.utils import short_repr, env
import math, os
import json
init_statements = ''
# global variables to be used for Java variable conversion
_javaNumericTypes = ['Integer', 'Long', 'Float', 'Double', 'Short', 'Byte']
_javaStringTypes = ['String', 'Char']

# Converting to Java. Returns [<java type as string>, value]
def _convert_to_java(var_from_sos):
    if var_from_sos is None:
        return ['Void','NULL']
    if isinstance(var_from_sos, bool):
        return ['boolean','true'] if var_from_sos else ['boolean','false']
    if isinstance(var_from_sos, int):
        # Differentiate between 32-bit and 64-bit integers to avoid over / underflow
        if var_from_sos < -2^31 or var_from_sos > 2^31-1:
            return ['long', repr(var_from_sos)]    
        return ['int', repr(var_from_sos)]
    if isinstance(var_from_sos, str):
        return ['String', '"'+var_from_sos+'"']
    if isinstance(var_from_sos, float):
        # Checking for NaN, +/- infinity before returning actual value
        if math.isnan(var_from_sos):
            return ['Double', 'Double.NaN']
        if var_from_sos == float('-inf'):
            return ['Double', 'Double.NEGATIVE_INFINITY']
        if var_from_sos == float('inf'):
            return ['Double', 'Double.POSITIVE_INFINITY']
        return ['double', repr(var_from_sos)]
    return None

def _get_java_type_and_value(self, javaVar):
    try:
        javaVarType = self.sos_kernel.get_response(f'System.out.println(((Object){javaVar}).getClass().getSimpleName());', ('stream',), 
        name=('stdout','stderr') )[0][1]['text']
        javaVarValue = self.sos_kernel.get_response(f'System.out.println({javaVar});', ('stream',), 
        name=('stdout', ' stderr') )[0][1]['text']
        return {'type':javaVarType, 'value':javaVarValue}
    except Exception as e:
        self.sos_kernel.warn(f'Exception occured when determining Java type of {javaVar}. {e.__str__()}')

def _convert_from_java_to_Python(self, javaVar):
    javaVarTypeAndValue = _get_java_type_and_value(self, javaVar)
    if javaVarTypeAndValue["type"] in _javaNumericTypes:
        return f'{javaVar} = {javaVarTypeAndValue["value"]}\n'
    if javaVarTypeAndValue["type"] in _javaStringTypes:
        return f'{javaVar} = "{javaVarTypeAndValue["value"]}"\n'
        

def _convert_from_java_to_SoS(self, javaVar):
    javaVarTypeAndValue = _get_java_type_and_value(self, javaVar)
    if javaVarTypeAndValue["type"] in _javaNumericTypes:
       return f'{javaVarTypeAndValue["value"]}'
    if javaVarTypeAndValue["type"] in _javaStringTypes:
       return f'"{javaVarTypeAndValue["value"]}"'

def _readSettings():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    settingsFilePath = os.path.join(__location__, 'settings.json')
    settings = None
    try:
        with open(settingsFilePath, 'r') as settingsFile:
            settings = settingsFile.read()
            settingsFile.close
    except Exception as exception:
            print(exception.__str__())
    return json.loads(settings, encoding='utf-8')
        
class sos_java:
    settings = _readSettings()
    background_color = settings["color"] if settings else '#ffaba3'
    allow_overwrite = settings["allowOverwrite"] if settings else False
    supported_kernels = {'Java': ['java']}
    #options = {'assignment_pattern': r'^\s*([A-Za-z0-9\.]+)\s*(=).*$'}
    options = {}
    cd_command = ''
    __version__ = __version__
    java_vars = dict()
    
    def __init__(self, sos_kernel, kernel_name='Java'):
        self.sos_kernel = sos_kernel
        self.kernel_name = 'Java'
        self.init_statements = init_statements
    
    def get_vars(self, names):
        for name in names:
            newname = name
            changed = False
            if newname.startswith('_') or newname.startswith('$'):
                newname = newname[1:]
                changed = True 
            if newname[0].isupper():
                newname = newname[0].lower()+newname[1:]
                changed = True 
            if changed:
                 self.sos_kernel.warn(f'Variable "{name}" from SoS to kernel {self.kernel_name} has been renamed to "{newname}" to follow language conventions')
            
            type_and_value = _convert_to_java(env.sos_dict[name]) 
            if type_and_value is None:
                self.sos_kernel.warn(f'Unsupported datatype {repr(env.sos_dict[name])} by {self.kernel_name}')
            else:
                if newname in sos_java.java_vars and sos_java.java_vars[newname] != type_and_value[0]:
                    oldname = newname
                    newname = newname + "_" +type_and_value[0]
                    self.sos_kernel.warn(f'Variable {name} is passed from SoS to kernel {self.kernel_name} already exists as {sos_java.java_vars[oldname]} type. Variable is saved as {newname}')
                
                result = self.sos_kernel.run_cell(
                    f'{type_and_value[0]} {newname} = {type_and_value[1]}',
                    True,
                    False,
                    on_error=f'Failed to get variable {name} to Java, could not convert to Java type.') 
                if result["status"] == 'ok':
                    sos_java.java_vars[newname] = type_and_value[0]

    def put_vars(self, items, to_kernel=None):
        if not items:
            return None
        if to_kernel in ['python3', 'Python3']:
            pythonCmd = ''
            try:
                for varName in items:
                    pythonCmd += _convert_from_java_to_Python(self, varName )
            except Exception as e:
                self.sos_kernel.warn(f'Exception occurred when transferring {varName} from Java to {to_kernel}. {e.__str__()}')
            return pythonCmd
        elif to_kernel == None:
            dictToSos = dict()
            try:
                for varName in items:
                    dictToSos[varName] += _convert_from_java_to_Python(self, varName )
            except Exception as e:
                self.sos_kernel.warn(f'Exception occurred when transferring {varName} from Java to {to_kernel}. {e.__str__()}')
            return dictToSos
            
    def expand(self, text, sigil):
        if sigil != '{ }':
            from sos.parser import replace_sigil
            text = replace_sigil(text, sigil)
        tmpExp = text.split('{')
        javaExpressions = []
        for exp in tmpExp:
            if '}' in exp:
                javaExpressions.append(exp.split('}')[0])
        javaResults = []
        try:
            for exp in javaExpressions:
                javaResults.append(self.sos_kernel.get_response(
                    f'System.out.println({exp});', ('stream',), name=('stdout', ' stderr') )[0][1]["text"])
            
            for index in range(0, len(javaResults)):
                text = text.replace('{'+javaExpressions[index]+'}',javaResults[index])
            
            return text
        except Exception:
            err_msg = self.sos_kernel.get_response(
               f'System.out.println({text});', ('stream',), name=('stdout',))[0][1]['text']
            self.sos_kernel.warn(f'Failed to expand "{text}": {err_msg}')
            return text
    
    def preview(self, item):
        javaVarTypeAndValue = _get_java_type_and_value(self,item)
        return (javaVarTypeAndValue["type"], javaVarTypeAndValue["value"])

    def sessioninfo(self):
        native_java = ''
        for prop in ['java.vm.name','java.runtime.version']:
            native_java += self.sos_kernel.get_response(f'System.out.println(System.getProperty("{prop}"));', ('stream',), 
            name=('stdout', ' stderr') )[0][1]["text"] +" "
        return [('Native Java', native_java), ("JupyterLab sos-java settings",f'{self.settings}')]