#!/usr/bin/env python3
#
# Copyright (c) Dr. Nandor Poka
# Distributed under the terms of the 3-clause BSD License.

from sos_notebook.test_utils import NotebookTest
import time

class TestDataExchange(NotebookTest):

    def get_from_SoS(self, notebook, var_name, sos_expr):
        notebook.call(f'{var_name} = {sos_expr}', kernel='SoS')
        if 'Array' in var_name:
            return notebook.check_output(f'''\
            %get {var_name}
            System.out.println(Arrays.toString({var_name}))''', kernel='Java')
        return notebook.check_output(f'''\
            %get {var_name}
            System.out.println({var_name})''', kernel='Java')

    def put_to_SoS(self, notebook, var_name,javaExpr):

        notebook.call(f'''\
            %put {var_name}
            {javaExpr}
            ''', kernel='Java')
        return notebook.check_output(f'print(repr({var_name}))', kernel='SoS')

    def test_get_none(self, notebook):
        var_name = 'nullVar'
        result = self.get_from_SoS(notebook, var_name, 'None')
        assert 'null' == result
    
    def test_put_null(self, notebook):
        var_name = 'putnullVar'
        assert 'None' == self.put_to_SoS(notebook, var_name, f'Void {var_name} = null;')
        
    
    def test_get_numpy_inf(self, notebook):
        var_name = 'infVar'
        notebook.call('import numpy', kernel='SoS')
        assert 'Infinity' == self.get_from_SoS(notebook, var_name, 'numpy.inf')
    
    def test_put_inf(self, notebook):
        var_name = 'putinfVar'
        assert 'inf' == self.put_to_SoS(notebook, var_name, f'double {var_name} = Double.POSITIVE_INFINITY')
    
    def test_get_nan(self, notebook):
        var_name = 'nanVar'
        assert 'NaN' == self.get_from_SoS(notebook, var_name, 'float("nan")')    
    
    def test_put_nan(self, notebook):
        var_name = 'putnanVar'
        assert 'nan' == self.put_to_SoS(notebook, var_name, f'double {var_name} = Double.NaN')
    
    def test_get_int1(self, notebook):
        var_name = 'intVar'
        assert '123' == self.get_from_SoS(notebook, var_name, '123')
        

    def test_get_int2(self, notebook):
        var_name = 'longVar'
        assert '1234567891234' == self.get_from_SoS(notebook, var_name, '1234567891234')

    def test_get_int3(self, notebook):
        var_name = 'longVar'
        assert '123456789123456789' == self.get_from_SoS(notebook, var_name, '123456789123456789')
    
    def test_put_int1(self, notebook):
        var_name = 'putintVar'
        assert '123' == self.put_to_SoS(notebook, var_name, f'int {var_name} = 123')

    def test_put_int2(self, notebook):
        var_name = 'putlongVar'
        assert '1234567891234' == self.put_to_SoS(notebook, var_name, f'long {var_name} = 1234567891234L')
    
    def test_put_int3(self, notebook):
        var_name = 'putlongVar'
        assert '123456789123456789' == self.put_to_SoS(notebook, var_name, f'long {var_name} = 123456789123456789L')
    
    def test_get_pos_double1(self, notebook):
        var_name = 'doubleVar'
        assert '1.0E-9' == self.get_from_SoS(notebook, var_name, '1e-09')

    def test_put_double1(self, notebook):
        var_name = 'putdoubleVar'
        assert '1e-09' == self.put_to_SoS(notebook, var_name, f'double {var_name} = 1e-09')

    def test_get_pos_double2(self, notebook):
        var_name = 'doubleVar'
        assert '1.0E-12' == self.get_from_SoS(notebook, var_name, '1e-12')

    def test_put_double2(self, notebook):
        var_name = 'putdoubleVar'
        assert '1e-12' == self.put_to_SoS(notebook, var_name, f'double {var_name} = 1e-12')

    def test_get_pos_double3(self, notebook):
        var_name = 'doubleVar'
        assert '1.0E-16' == self.get_from_SoS(notebook, var_name, '1e-16')

    def test_put_double3(self, notebook):
        var_name = 'putoubleVar'
        assert '1e-16' == self.put_to_SoS(notebook, var_name, f'double {var_name} = 1e-16')
    
    def test_get_logic_true(self, notebook):
        var_name = 'boolVar'
        assert 'true' == self.get_from_SoS(notebook, var_name, 'True')
        

    def test_get_logic_false(self, notebook):
        var_name = 'boolVar'
        assert 'false' == self.get_from_SoS(notebook, var_name, 'False')

    def test_put_logic_true(self, notebook):
        var_name = 'putBoolVar'
        assert 'True' == self.put_to_SoS(notebook, var_name,f'boolean {var_name} = true;')


    def test_put_logic_false(self, notebook):
        var_name = 'putBoolVar'
        assert 'False' == self.put_to_SoS(notebook, var_name,f'boolean {var_name} = false;')
    
    
    def test_get_int_array1(self, notebook):
        var_name = 'intArray'
        assert '[1]' == self.get_from_SoS(notebook, var_name,'[1]')

    def test_get_int_array2(self, notebook):
        var_name = 'intArray'
        assert '[1, 2, 3, 4, 5]' == self.get_from_SoS(notebook, var_name,'[1, 2, 3, 4, 5]')

    def test_put_int_array1(self, notebook):
        var_name = 'putIntArray'
        assert '[1]' == self.put_to_SoS(notebook, var_name, f'int[] {var_name}'+' = new int[]{1}')

    def test_put_int_array2(self, notebook):
        var_name = 'putIntArray'
        assert '[1, 2, 3, 4, 5, 6]' == self.put_to_SoS(notebook, var_name, f'int[] {var_name}'+' = new int[]{1,2,3,4,5,6}')

    def test_get_logic_array1(self, notebook):
        var_name = 'boolArray'
        assert '[true]' == self.get_from_SoS(notebook, var_name, '[True]')
    
    def test_get_logic_array2(self, notebook):
        var_name = 'boolArray'
        assert '[true, false, false, true]' == self.get_from_SoS(notebook, var_name, '[True, False, False, True]')

    def test_put_logic_array1(self, notebook):
        var_name = 'putBoolArray'
        assert '[True]' == self.put_to_SoS(notebook, var_name,  f'boolean[]{var_name}= new boolean[]'+'{true};')

    def test_put_logic_array2(self, notebook):
        var_name = 'putBoolArray'
        assert '[True, False, True, False]' == self.put_to_SoS(notebook, var_name,  f'boolean[]{var_name}= new boolean[]'+'{true, false, true,false};')
    
    def test_get_str1(self, notebook):
        var_name = 'stringVar'
        assert "ab c d" == self.get_from_SoS(notebook, var_name, "'ab c d'")

    def test_put_str(self, notebook):
        var_name = 'putStringVar'
        assert "'ab c d'" == self.put_to_SoS(notebook,var_name, f'String {var_name}= "ab c d"')

    '''
    def test_get_mixed_list(self, notebook):
        assert "1.4\nTRUE\n'asd'" == self.get_from_SoS(notebook, '[1.4, True, "asd"]')

    def test_put_mixed_list(self, notebook):
        # R does not have mixed list, it just convert everything to string.
        assert "['1.4', 'TRUE', 'asd']" == self.put_to_SoS(notebook, 'c(1.4, TRUE, "asd")')

    def test_get_dict(self, notebook):
        # Python does not have named ordered list, so get dictionary
        assert "$a\n1\n$b\n2\n$c\n'3'" == self.get_from_SoS(notebook, "dict(a=1, b=2, c='3')")

    def test_put_named_list(self, notebook):
        assert "{'a': 1, 'b': 2, 'c': '3'}" == self.put_to_SoS(notebook, "list(a=1, b=2, c='3')")

    def test_get_set(self, notebook):
        output = self.get_from_SoS(notebook, "{1.5, 'abc'}")
        assert "1.5\n'abc'" == output or "'abc'\n1.5" == output

    def test_put_unnamed_list(self, notebook):
        output = self.put_to_SoS(notebook, "list(1.5, 'abc')")
        assert "[1.5, 'abc']" == output or "['abc', 1.5]" == output

    def test_get_complex(self, notebook):
        assert "1+2.2i" == self.get_from_SoS(notebook, "complex(1, 2.2)")

    def test_put_complex(self, notebook):
        assert "(1+2.2j)" == self.put_to_SoS(notebook, "complex(real=1, imaginary=2.2)")

    def test_get_recursive(self, notebook):
        assert "$a\n1\n$b\n$c\n3\n$d\n'whatever'" == self.get_from_SoS(notebook, "{'a': 1, 'b': {'c': 3, 'd': 'whatever'}}")

    def test_put_recursive(self, notebook):
        assert "{'a': 1, 'b': {'c': 3, 'd': 'whatever'}}" == self.put_to_SoS(notebook, "list(a=1, b=list(c=3, d='whatever'))")

    def test_get_series(self, notebook):
        notebook.call('import pandas as pd', kernel='SoS')
        assert "0\n5\n1\n6\n2\n7" == self.get_from_SoS(notebook, 'pd.Series([5 ,6, 7])')

    def test_put_series(self, notebook):
        output = self.put_to_SoS(notebook, "setNames(c(11, 22, 33), c('a', 'b', 'c'))")
        assert 'a    11' in output and 'b    22' in output and 'c    33' in output

    def test_get_matrix(self, notebook):
        notebook.call('import numpy as np', kernel='SoS')
        assert "0 1\n1 2\n3 4" == self.get_from_SoS(notebook, 'np.matrix([[1,2],[3,4]])')

    def test_put_matrix(self, notebook):
        output = self.put_to_SoS(notebook, "matrix(c(2, 4, 3, 1, 5, 7), nrow=2)")
        assert 'array' in output and '[2., 3., 5.]' in output and '[4., 1., 7.]' in output

    def test_get_dataframe(self, notebook):
        notebook.call('\
  #          %put df --to R
  #          import pandas as pd
  #          import numpy as np
  #          arr = np.random.randn(1000)
  #          arr[::10] = np.nan
  #          df = pd.DataFrame({'column_{0}'.format(i): arr for i in range(10)})
            ', kernel='SoS')
        assert '1000' == notebook.check_output('dim(df)[1]', kernel='R')
        assert '10' == notebook.check_output('dim(df)[2]', kernel='R')

    def test_put_dataframe(self, notebook):
        notebook.call('%put mtcars', kernel='R')
        assert '32' == notebook.check_output('mtcars.shape[0]', kernel='SoS')
        assert '11' == notebook.check_output('mtcars.shape[1]', kernel='SoS')
        assert "'Mazda RX4'" == notebook.check_output('mtcars.index[0]', kernel='SoS')

    def test_get_dict_with_special_keys(self, notebook):
        output = self.get_from_SoS(notebook, "{'11111': 1, '_1111': 'a', 11112: 2, (1,2): 3}")
        assert '$X11111' in output and '$X_1111' in output and '$X11112' in output and '$X_1__2_' in output
    '''
