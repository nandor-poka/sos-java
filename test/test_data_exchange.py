#!/usr/bin/env python3
#
# Copyright (c) Dr. Nandor Poka
# Distributed under the terms of the 3-clause BSD License.

from sos_notebook.test_utils import NotebookTest
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
        assert "'ab c d'" == self.put_to_SoS(notebook,var_name, f'String {var_name}= "ab c d";')

    def test_get_dict(self, notebook):
        var_name = 'dictVar'
        assert '{two=2, one=1}' == self.get_from_SoS(notebook, var_name,"dict(one=1, two=2)")

    def test_put_dict(self, notebook):
        var_name = 'putDictVar'
        assert "{'a': 1, 'b': 2, 'c': 3}" == self.put_to_SoS(notebook, var_name, f'HashMap<String, Integer>{var_name} = new HashMap<String, Integer>();'
        +f'{var_name}.put("a",1);{var_name}.put("b",2);{var_name}.put("c",3)')

    def test_get_tuple(self, notebook):
        var_name = 'setVar'
        assert "[1, 2, 3, 4]" == self.get_from_SoS(notebook, var_name, "(1, 2, 3, 4)")

    def test_put_set(self, notebook):
        var_name = 'putSetVar'
        assert '[1, 2, 3, 4, 5]' == self.put_to_SoS(notebook, var_name, f'HashSet<Integer> {var_name} = new HashSet<Integer>();'
        +f'{var_name}.add(1);{var_name}.add(2);{var_name}.add(3);{var_name}.add(4);{var_name}.add(5);')
