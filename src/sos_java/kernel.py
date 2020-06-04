from ._version import __version__
from sos.utils import short_repr, env
import math, os
import numpy as np
import json
from pathlib import Path
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
init_statements = f'''
    %loadFromPOM {os.path.join(__location__, 'pom.xml')}
    import com.fasterxml.jackson.databind.*;
    import javax.json.*;
    import java.util.stream.*;
'''+'''
    public JsonObject parseJsonString(String str){
        JsonReader jsonReader = Json.createReader(new StringReader(str));
        JsonObject jsonObj = jsonReader.readObject();
        jsonReader.close();
        return jsonObj;
    }

    public String convertJavaObjectToJsonString(Object obj){
        try{
            ObjectMapper mapper = new ObjectMapper();
            String jsonStr = mapper.writeValueAsString(obj);
            if (!jsonStr.startsWith("{")){
                jsonStr = "{\\"value\\":"+jsonStr+"}";
            }
            return jsonStr;
        } catch (Exception ex){
            return ex.toString();
        }
    }

    public String getJavaArrayValues(int[] array){
        String values = "";
        for (int i=0;i<array.length;++i){
            values += String.valueOf(array[i])+",";
        }
        values = values.substring(0, values.length()-1);
        return values;
    }
    
    public String getJavaArrayValues(byte[] array){
        String values = "";
        for (int i=0;i<array.length;++i){
            values += String.valueOf(array[i])+",";
        }
        values = values.substring(0, values.length()-1);
        return values;
    }

    public String getJavaArrayValues(short[] array){
        String values = "";
        for (int i=0;i<array.length;++i){
            values += String.valueOf(array[i])+",";
        }
        values = values.substring(0, values.length()-1);
        return values;
    }

    public String getJavaArrayValues(float[] array){
        String values = "";
        for (int i=0;i<array.length;++i){
            values += String.valueOf(array[i])+",";
        }
        values = values.substring(0, values.length()-1);
        return values;
    }
    
    public String getJavaArrayValues(double[] array){
        String values = "";
        for (int i=0;i<array.length;++i){
            values += String.valueOf(array[i])+",";
        }
        values = values.substring(0, values.length()-1);
        return values;
    }
    
    public String getJavaArrayValues(long[] array){
        String values = "";
        for (int i=0;i<array.length;++i){
            values += String.valueOf(array[i])+",";
        }
        values = values.substring(0, values.length()-1);
        return values;
    }
    
    public String getJavaArrayValues(boolean[] array){
        String values = "";
        for (int i=0;i<array.length;++i){
            if (array[i]){
                values += "True,";
            }else{
                values += "False,";
            }
        }
        values = values.substring(0, values.length()-1);
        return values;
    }
    
    public String getJavaArrayValues(String[] array){
        String values = "";
        for (int i=0;i<array.length;++i){
            values += "'"+array[i]+"',";
        }
        values = values.substring(0, values.length()-1);
        return values;
    }
    
    public <T> String getJavaListTypeValues(List<T> list){
        String elementType = ((Object)list.get(0)).getClass().getSimpleName();
        String values = "";
        switch(elementType){
            case "Byte":
                return list.toString();
            case "Short":
                return list.toString();
            case "Integer":
                return list.toString();
            case "Long":
                return list.toString();
            case "Float":
                return list.toString();
            case "Double":
                return list.toString();
            case "String":
                for (int i=0;i<list.size();++i){
                    values += "'"+list.get(i)+"',";
                }
                values = values.substring(0, values.length()-1);
                return values;
            case "Boolean":
                for (int i=0;i<list.size();++i){
                    if(Boolean.parseBoolean(list.get(i).toString())){   
                        values += "True,";
                    }else{
                         values += "False,";
                    }
                }
                values = values.substring(0, values.length()-1);
                return values;
            default:
                return "Unsupported type in list.";
        }
    }

    public <T> String getJavaSetTypeValues(Set<T> set){
        Object[] setElementArray = set.toArray();
        String elementType = setElementArray[0].getClass().getSimpleName();
        String values = "";
        switch(elementType){
            case "Byte":
                return set.toString();
            case "Short":
                return set.toString();
            case "Integer":
                return set.toString();
            case "Long":
                return set.toString();
            case "Float":
                return set.toString();
            case "Double":
                return set.toString();
            case "String":
                for (int i=0;i<setElementArray.length;++i){
                    values += "'"+setElementArray[i]+"',";
                }
                values = values.substring(0, values.length()-1);
                return values;
            case "Boolean":
                for (int i=0;i<setElementArray.length;++i){
                    if(Boolean.parseBoolean(setElementArray[i].toString())){   
                        values += "True,";
                    }else{
                         values += "False,";
                    }
                    
                }
                values = values.substring(0, values.length()-1);
                return values;
            default:
                return "Unsupported type in list.";
        }
    }
    
    public <T1, T2> String getJavaMapTypeValues(Map<T1,T2> map){
        String values = "";
        String keyType = map.entrySet().iterator().next().getKey().getClass().getSimpleName();
        String valueType = ( (Object)map.entrySet().iterator().next().getValue()).getClass().getSimpleName();
        String keyValue;
        String valueValue;
        for (Map.Entry<T1,T2> entry: map.entrySet() ){
            switch(keyType){
                case "Byte":
                    keyValue = entry.getKey().toString();
                    break;
                case "Short":
                    keyValue = entry.getKey().toString();
                    break;
                case "Integer":
                    keyValue = entry.getKey().toString();
                    break;
                case "Long":
                    keyValue = entry.getKey().toString();
                    break;
                case "Float":
                    keyValue = entry.getKey().toString();
                    break;
                case "Double":
                    keyValue = entry.getKey().toString();
                    break;
                case "String":
                    keyValue = "'"+entry.getKey()+"'";
                    break;
                case "Boolean":
                    if(Boolean.parseBoolean(entry.getKey().toString())){   
                        keyValue = "True,";
                    }else{
                        keyValue = "False,";
                    }
                    break;
                default:
                    keyValue = null;
                    break;
            }
            switch(valueType){
                case "Byte":
                    valueValue = entry.getValue().toString();
                    break;
                case "Short":
                    valueValue = entry.getValue().toString();
                    break;
                case "Integer":
                    valueValue = entry.getValue().toString();
                    break;
                case "Long":
                    valueValue = entry.getValue().toString();
                    break;
                case "Float":
                    valueValue = entry.getValue().toString();
                    break;
                case "Double":
                    valueValue = entry.getValue().toString();
                    break;
                case "String":
                    valueValue = "'"+entry.getValue()+"'";
                    break;
                case "Boolean":
                    if(Boolean.parseBoolean(entry.getValue().toString())){   
                        valueValue = "True";
                    }else{
                        valueValue = "False";
                    }
                    break;
                default:
                    valueValue = null;
                    break;
            }
            if (keyValue == null ||  valueValue == null){
                return "Unsupported type in Map.";
            }
            values += keyValue +":"+valueValue+",";
        }
        values = values.substring(0, values.length()-1);
        return values;
    }  
'''

# global variables to be used for Java variable conversion
_javaNumericTypes = ['Integer', 'Long', 'Float', 'Double', 'Short', 'Byte']
_javaStringTypes = ['String', 'Char']
_javaMapTypes = ['Map', 'ConcurrentHashMap', 'ConcurrentSkipListMap', 'EnumMap', 'HashMap', 'LinkedHashMap' 'IdentityHashMap', 'TreeMap', 'WeakHashMap']
_javaSetTypes = ['ConcurrentSkipListSet', 'CopyOnWriteArraySet', 'EnumSet', 'HashSet', 'LinkedHashSet','TreeSet']
_javaListTypes = [ 'List','AbstractSequentialList', 'LinkedList', 'ArrayList', 'ObservableListBase', 'Vector', 'Stack']
_javaBooleanTypes = ['boolean', 'Boolean']
# dict used as 'switch' to convert primitive numeric Java types to ther boxing class
_Java_primitive_to_BoxingClass = {
    'int':'Integer',
    'float': 'Float',
    'double': 'Double',
    'byte': 'Byte'
}

def _check_type_homogeneity_in_collection(var_from_sos):
    if isinstance(var_from_sos, (type({}.keys()),type({}.values()) )):
        iterator = iter(var_from_sos)
        type_of_first_element = type(next(iterator))
    else:
        type_of_first_element = type(var_from_sos[0])
    return all(isinstance(element, type_of_first_element) for element in var_from_sos)

#returns the type (class) of the variable if it exists or none.
def _check_user_variables(self, varName):
    response = self.sos_kernel.get_response(f'System.out.println( {varName}==null );', ('stream',), 
        name=('stdout','stderr') )
    if response != [] and response[0][1]['text'] == 'false':
        return self.sos_kernel.get_response(f'System.out.println( (Object){varName}.getClass().getSimpleName() );', ('stream',), 
        name=('stdout','stderr') )[0][1]['text']
    return None
# Conversions TO JAVA
def _convert_None_to_Java(self, var_from_sos, varName):
     return ['Void','null']

def _convert_Integers_to_Java(self, var_from_sos, varName):
    if var_from_sos < -2**31 or var_from_sos > 2**31-1:
            return ['long', repr(var_from_sos)]    
    return ['int', repr(var_from_sos)]

def _convert_bool_to_Java(self, var_from_sos, varName):
    return ['boolean','true'] if var_from_sos else ['boolean','false']

def _convert_string_to_Java(self, var_from_sos, varName):
    return ['String', '"'+var_from_sos+'"']

def _convert_tuple_to_Java(self, var_from_sos, varName):
    if not _check_type_homogeneity_in_collection(var_from_sos):
        print(f'Java does not support collections (eg. Sets, Lists, Maps) with heterogenous types.')
        return None
    # At this point the tuple is homogenous at the first level of elements, thus the 1st element type applies to all
    converter = _typeToConverterSwitchPythonToJava[type(var_from_sos[0])]
    # Non-collection types can be converted directly, this means that the tuple is a tuple of primitives (more generally non collection type)
    if type(var_from_sos[0])not in (tuple, list, dict):
        # Primitive Java numeric types need to be converted to their Boxing type. Eg. int -> Integer.
        rawTypeInJava = converter(self,var_from_sos[0], varName )[0]
        elementTypeInJava = _Java_primitive_to_BoxingClass[rawTypeInJava] if rawTypeInJava in ('int', 'float', 'double', 'byte') else rawTypeInJava
        setInitString = 'Stream.of('    
        for element in var_from_sos:
            conversion = converter(self, element, varName )
            elementValue = conversion[1]
            setInitString += f'{elementValue},'
        setInitString = setInitString.rstrip(',')
        setInitString += ').collect(Collectors.toCollection(HashSet::new));'
        return [f'HashSet<{elementTypeInJava}>', setInitString]
    else:
        for index in range(0, len(var_from_sos)-1):
            if type(var_from_sos[index]!=type(var_from_sos[index+1])):
                print(f'Java does not support collections (eg. Sets, Lists, Maps) with heterogenous types.')
                return None
        # in this case the original tuple contained other collection(s). Eg tuple of tuples
        setInitString = 'Stream.of('  
        for element in var_from_sos:
            conversion = converter(self, element, varName )
            if conversion == None:
                break
            elementTypeInJava = conversion[0]
            elementValue = conversion[1]
            setInitString += f'{elementValue},'
        if conversion == None:
            return None
        setInitString = setInitString.rstrip(',')
        setInitString += ').collect(Collectors.toCollection(HashSet::new));'
        setInitString = setInitString.replace('<T>',f'<{elementTypeInJava}>')
        return [f'HashSet<{elementTypeInJava}>', setInitString]

def _convert_float_to_Java(self, var_from_sos, varName):
    # Checking for NaN, +/- infinity before returning actual value
    if math.isnan(var_from_sos):
        return ['Double', 'Double.NaN']
    if var_from_sos == float('-inf'):
        return ['Double', 'Double.NEGATIVE_INFINITY']
    if var_from_sos == float('inf'):
        return ['Double', 'Double.POSITIVE_INFINITY']
    return ['double', repr(var_from_sos)]
    
def _convert_dict_to_Java(self, var_from_sos, varName):
    if not _check_type_homogeneity_in_collection(var_from_sos.keys()):
        self.sos_kernel.warn(f'Java does not support collections (eg. Sets, Lists, Maps) with heterogenous types. Keys in {varName} are of not the same types.')
        return None
    elif not _check_type_homogeneity_in_collection(var_from_sos.values()):
        self.sos_kernel.warn(f'Java does not support collections (eg. Sets, Lists, Maps) with heterogenous types. Values in {varName} are of not the same types.')
        return None
    items = var_from_sos.items()
    items_iterator = iter(items)
    fistItem = next(items_iterator)
    # At this point the map is homogenous at the first level of elements, thus the 1st element type applies to all
    keys_converter = _typeToConverterSwitchPythonToJava[type(fistItem[0])]
    values_converter = _typeToConverterSwitchPythonToJava[type(fistItem[1])]
    if type(fistItem[0]) not in (tuple, list, dict):
         # Primitive Java numeric types need to be converted to their Boxing type. Eg. int -> Integer.
        keys_rawTypeInJava = keys_converter(self,fistItem[0], varName )[0]
        keys_elementTypeInJava = _Java_primitive_to_BoxingClass[keys_rawTypeInJava] if keys_rawTypeInJava in ('int', 'float', 'double', 'byte') else keys_rawTypeInJava
    if type(fistItem[1]) not in (tuple, list, dict):
        values_rawTypeInJava = values_converter(self,fistItem[1], varName )[0]
        values_elementTypeInJava = _Java_primitive_to_BoxingClass[keys_rawTypeInJava] if values_rawTypeInJava in ('int', 'float', 'double', 'byte') else values_rawTypeInJava    
    mapInitString = f'new HashMap(Stream.of(' 
    for entry in  items:
        key_conversion = keys_converter(self, entry[0], varName )
        value_conversion  = values_converter(self, entry[1], varName )
        key_Value = key_conversion[1]
        value_Value = value_conversion[1]
        mapInitString+= f'new AbstractMap.SimpleEntry<{keys_elementTypeInJava}, {values_elementTypeInJava}>({key_Value}, {value_Value}),'
    mapInitString = mapInitString.rstrip(',')
    mapInitString += ').collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue)));'
    return [f'HashMap<{keys_elementTypeInJava},{values_elementTypeInJava}>', mapInitString]

def _convert_list_to_Java(self, var_from_sos, varName):
    if not _check_type_homogeneity_in_collection(var_from_sos):
        self.sos_kernel.warn(f'Java does not support collections (eg. Sets, Lists, Maps) with heterogenous types. Keys in {varName} are of not the same types.')
        return None
    # At this point the list is homogenous at the first level of elements, thus the 1st element type applies to all
    converter = _typeToConverterSwitchPythonToJava[type(var_from_sos[0])]
    # Primitive Java numeric types need to be converted to their Boxing type. Eg. int -> Integer.
    rawTypeInJava = converter(self,var_from_sos[0], varName )[0]
    listInitString = f'new {rawTypeInJava}[]'+'{' 
    for item in  var_from_sos:
        conversion = converter(self, item, varName )
        itemValue = conversion[1]
        listInitString+= f'{itemValue},'
    listInitString = listInitString.rstrip(',')
    listInitString += '};'
    return [f'{rawTypeInJava}[]', listInitString]

def _convert_list_to_Java_as_ArrayList(self, var_from_sos, varName):
    if not _check_type_homogeneity_in_collection(var_from_sos):
        self.sos_kernel.warn(f'Java does not support collections (eg. Sets, Lists, Maps) with heterogenous types. Keys in {varName} are of not the same types.')
        return None
    # At this point the list is homogenous at the first level of elements, thus the 1st element type applies to all
    converter = _typeToConverterSwitchPythonToJava[type(var_from_sos[0])]
    # Primitive Java numeric types need to be converted to their Boxing type. Eg. int -> Integer.
    rawTypeInJava = converter(self,var_from_sos[0], varName )[0]
    elementTypeInJava = _Java_primitive_to_BoxingClass[rawTypeInJava] if rawTypeInJava in ('int', 'float', 'double', 'byte') else rawTypeInJava
    listInitString = f'new ArrayList(Stream.of(' 
    for item in  var_from_sos:
        conversion = converter(self, item, varName )
        itemValue = conversion[1]
        listInitString+= f'{itemValue},'
    listInitString = listInitString.rstrip(',')
    listInitString += ').collect(Collectors.toList()));'
    return [f'ArrayList<{elementTypeInJava}>', listInitString]

# Conversions FROM JAVA
def _java_array_values(self, javaVar):
    response =  self.sos_kernel.get_response(f'''System.out.println( getJavaArrayValues({javaVar}) );''', ('stream',), 
        name=('stdout','stderr') )
    if response != []:
        return response[0][1]['text']
    self.sos_kernel.warn(f'Failed to get array values for {javaVar}.')
    return []

def _java_list_type_values(self, javaVar):
    return self.sos_kernel.get_response(f'System.out.println( getJavaListTypeValues({javaVar}) );', ('stream',), 
        name=('stdout','stderr') )[0][1]['text'] 

def _java_map_type_values(self, javaVar):
    result = self.sos_kernel.get_response(f'System.out.println( getJavaMapTypeValues({javaVar}) );''', ('stream',), 
        name=('stdout','stderr') )
    if result != []:
        return result[0][1]['text'] 
    self.sos_kernel.warn(f'Failed to get map values for {javaVar}.')
    return {}
def _java_set_type_values(self, javaVar):
    return self.sos_kernel.get_response(f'System.out.println( getJavaSetTypeValues({javaVar}) );', ('stream',), 
        name=('stdout','stderr') )[0][1]['text'] 
        
def _get_java_type_and_value(self, javaVar):
    try:
        javaVarType = self.sos_kernel.get_response('try{System.out.println(((Object)'+f'{javaVar}'+''').getClass().getSimpleName());
                                                    }catch (NullPointerException e){
                                                        System.out.println("Void");
                                                    }''', ('stream',), 
        name=('stdout','stderr') )[0][1]['text']
        javaVarValue = self.sos_kernel.get_response('try{System.out.println('+f'{javaVar}'+''');
                                                    }catch (NullPointerException e){
                                                        System.out.println("null");
                                                    }''', ('stream',), 
        name=('stdout', ' stderr') )[0][1]['text']
        return {'type':javaVarType, 'value':javaVarValue}
    except Exception as e:
        self.sos_kernel.warn(f'Exception occured when determining Java type of {javaVar}. {e.__str__()}')

def _convert_from_java_to_Python(self, javaVar, as_type):
    if as_type != None and as_type.lower() == 'json':
        return f'{javaVar} = json.loads(\'{_convertJavaToJSONString(self, javaVar)}\')'
    javaVarTypeAndValue = _get_java_type_and_value(self, javaVar)
    if javaVarTypeAndValue["type"] == 'Void':
        return f'{javaVar} = None\n'
    if javaVarTypeAndValue["type"] in _javaNumericTypes:
        return f'{javaVar} = {javaVarTypeAndValue["value"]}\n'
    if javaVarTypeAndValue["type"] in _javaStringTypes:
        return f'{javaVar} = "{javaVarTypeAndValue["value"]}"\n'
    if javaVarTypeAndValue["type"] in _javaBooleanTypes:
        if javaVarTypeAndValue["value"] in ['True', 'true', 'TRUE']:
            return f'{javaVar} = "True"\n'
        else:
            return f'{javaVar} = "False"\n'
    # array eg int[] convert to list in python []
    if '[]' in javaVarTypeAndValue["type"]:
        return f'{javaVar} = [{_java_array_values(self, javaVar)}]'
    if javaVarTypeAndValue["type"] in _javaListTypes:
        return f'{javaVar} = [{_java_list_type_values(self, javaVar)}]'
    if javaVarTypeAndValue["type"] in _javaMapTypes:
        #self.sos_kernel.warn(f'{javaVar} = '+'{'+f'{_java_map_type_values(self, javaVar)}'+'}')
        return f'{javaVar} = '+'{'+f'{_java_map_type_values(self, javaVar)}'+'}'
    if javaVarTypeAndValue["type"] in _javaSetTypes:
        return f'{javaVar} = '+'('+f'{_java_set_type_values(self, javaVar)}'+')'

def _convertJavaToJSONString(self, javaVar):
    return self.sos_kernel.get_response(f'System.out.println( convertJavaObjectToJsonString({javaVar}));', ('stream',), 
        name=('stdout','stderr') )[0][1]['text']

def _convert_from_java_to_SoS(self, javaVar, as_type):
    if as_type != None and as_type.lower() == 'json':
        return f'\'{_convertJavaToJSONString(self, javaVar)}\''
    javaVarTypeAndValue = _get_java_type_and_value(self, javaVar)
    if javaVarTypeAndValue["type"] == 'Void':
        return f'None'
    if javaVarTypeAndValue["type"] in _javaNumericTypes:
       return f'{javaVarTypeAndValue["value"]}'
    if javaVarTypeAndValue["type"] in _javaStringTypes:
       return f'"{javaVarTypeAndValue["value"]}"'
    if javaVarTypeAndValue["type"] in _javaBooleanTypes:
        if javaVarTypeAndValue["value"] in ['True', 'true', 'TRUE']:
            return 'True'
        else:
            return 'False'
    if '[]' in javaVarTypeAndValue["type"]:
        return f'[{_java_array_values(self, javaVar)}]'
    if javaVarTypeAndValue["type"] in _javaListTypes:
        return f'[{_java_list_type_values(self, javaVar)}]'
    if javaVarTypeAndValue["type"] in _javaMapTypes:
        return '{'+f'{_java_map_type_values(self, javaVar)}'+'}'
    if javaVarTypeAndValue["type"] in _javaSetTypes:
        return '('+f'{_java_set_type_values(self, javaVar)}'+')'

def _readSettings():
    settingsFilePath = Path(os.path.join(__location__, 'settings.json'))
    settings = None
    try:
        if not settingsFilePath.is_file():
            return settings
        with open(settingsFilePath, 'r') as settingsFile:
            settings = settingsFile.read()
            settingsFile.close
    except Exception as exception:
            print(exception.__str__())
    return json.loads(settings, encoding='utf-8')

# Dict that maps python types to functions that will do the conversions
_typeToConverterSwitchPythonToJava = {
    'NoneType': _convert_None_to_Java,
    'bool': _convert_bool_to_Java,
    'np.bool': _convert_bool_to_Java,
    'int': _convert_Integers_to_Java,
    'np.int8': _convert_Integers_to_Java,
    'np.int16': _convert_Integers_to_Java,
    'np.int32': _convert_Integers_to_Java,
    'np.int64': _convert_Integers_to_Java,
    'float': _convert_float_to_Java,
    'str': _convert_string_to_Java,
    'tuple': _convert_tuple_to_Java,
    'dict': _convert_dict_to_Java,
    'list': _convert_list_to_Java
}  
class sos_java:
    settings = _readSettings()
    background_color = settings["color"] if settings else '#ffaba3'
    allow_overwrite = settings["allowOverwrite"] if settings else False
    supported_kernels = {'Java': ['java']}
    options = {'assignment_pattern': r'^\s*([A-Za-z0-9\.]+)\s*(=).*$'}
    #options = {}
    cd_command = ''
    __version__ = __version__
    java_vars = dict()
    
    def __init__(self, sos_kernel, kernel_name='Java'):
        self.sos_kernel = sos_kernel
        self.kernel_name = 'Java'
        self.init_statements = init_statements
    
    def get_vars(self, names):
        try:
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
                converter = _typeToConverterSwitchPythonToJava[str(type(env.sos_dict[name])).split("'")[1]]
                type_and_value = converter(self, env.sos_dict[name], name) if converter else None
                if type_and_value is None:
                    self.sos_kernel.warn(f'Unsupported datatype {repr(env.sos_dict[name])} by {self.kernel_name}')
                    continue
                else:
                    if newname in sos_java.java_vars and sos_java.java_vars[newname] != type_and_value[0]:
                        oldname = newname
                        typename = type_and_value[0].split('[')[0].split('<')[0]
                        
                        newname = newname + "_" +typename
                        self.sos_kernel.warn(f'Variable {name} is passed from SoS to kernel {self.kernel_name} already exists as {sos_java.java_vars[oldname]} type. Variable is saved as {newname}')
                    result = self.sos_kernel.run_cell(
                        f'{type_and_value[0]} {newname} = {type_and_value[1]};',
                        True,
                        False,
                        on_error=f'Failed to get variable {name} to Java, could not convert to Java type.')
                    if result["status"] == 'ok':
                        sos_java.java_vars[newname] = type_and_value[0]
        except Exception as e:
            self.sos_kernel.warn(f'''Failed to get variable {name} to Java, could not convert to Java type.\n
The following exception occured: {e}\n''')

    def put_vars(self, items, to_kernel=None, as_type=None):
        if not items:
            return {}
        if to_kernel in ['python3', 'Python3']:
            pythonCmd = ''
            try:
                for varName in items:
                    varName = varName.rstrip(',')
                    #self.sos_kernel.warn(_convert_from_java_to_Python(self, varName, as_type=as_type ))
                    pythonCmd += _convert_from_java_to_Python(self, varName, as_type=as_type )+'\n'
            except Exception as e:
                self.sos_kernel.warn(f'Exception occurred when transferring `{varName}` from Java to {to_kernel}. {e.__str__()}')
            return pythonCmd
        else:
            dictToSos = dict()
            try:
                for varName in items:
                    dictToSos[varName] = eval(_convert_from_java_to_SoS(self, varName, as_type ))
            except Exception as e:
                self.sos_kernel.warn(f'Exception occurred when transferring `{varName}` from Java to SoS Kernel. {e.__str__()}')

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