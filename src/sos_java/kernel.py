from ._version import __version__
from sos.utils import short_repr, env
import math
import json
init_statements = ''

# Converting to Java. Returns [<java type as string>, value]
def convert_to_java(var_from_sos):
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
        if math.isnan(var_from_sos):
            return ['Double', 'Double.NaN']
        if var_from_sos == float('-inf'):
            return ['Double', 'Double.NEGATIVE_INFINITY']
        if var_from_sos == float('inf'):
            return ['Double', 'Double.POSITIVE_INFINITY']
        return ['double', repr(var_from_sos)]
    return None


        
class sos_java:
    background_color = '#ffaba3'
    supported_kernels = {'Java': ['java']}
    options = {'assignment_pattern': r'^\s*([A-Za-z0-9\.]+)\s*(=).*$'}
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
            
            type_and_value = convert_to_java(env.sos_dict[name]) 
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
        return None

    def expand(self, text, sigil):
        return None
    
    def preview(self, item):
        return None

    def sessioninfo(self):
        return None