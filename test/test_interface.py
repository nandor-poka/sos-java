#!/usr/bin/env python3
#
# Copyright (c) Dr. Nandor Poka
# Distributed under the terms of the 3-clause BSD License.

import os
import tempfile
from sos_notebook.test_utils import NotebookTest
import time

class TestInterface(NotebookTest):

    def test_prompt_color(self, notebook):
        '''test color of input and output prompt'''
        idx = notebook.call(
            '''\
            System.out.println("this is Java");
            ''', kernel="Java")
        assert [255, 171, 163] == notebook.get_input_backgroundColor(idx)
        assert [255, 171, 163] == notebook.get_output_backgroundColor(idx)

    def test_var_name_with_underscore(self, notebook):
        '''Test  _varName -> varName'''
        # _varName -> varName
        notebook.call(
            '''\
            %put _varName --to java
            _varName = 5
            ''',
            kernel="SoS",
            expect_error=True)
        assert '5' == notebook.check_output('System.out.println(varName)', kernel='Java')
    def test_var_name_with_captial_letter(self, notebook):
        '''Test  CapitalStart -> capitalStart'''
        notebook.call(
            '''\
            %put CapitalStart --to java
            CapitalStart = 500
            ''',
            kernel="SoS",
            expect_error=True)
        assert '500' == notebook.check_output('System.out.println(capitalStart)', kernel='Java')
        
    def test_expand(self, notebook):
        '''Test %expand --in java'''
        notebook.call('int var = 100;', kernel="Java")
        assert 'value is 102' in notebook.check_output(
            '''\
            %expand --in Java
            value is {var + 2}
            ''',
            kernel='Markdown')
       # assert 'value is 102' in notebook.check_output(
       #     '''\
       #     %expand `java ` --in java
       #     value is `java var + 2`
       #     ''',
       #     kernel='Markdown')

    #def test_preview(self, notebook):
    #    '''Test support for %preview'''
    #    output = notebook.check_output(
    #        '''\
    #        %preview -n var
    #        var = seq(1, 1000)
    #       ''',
    #        kernel="R")
        # in a normal var output, 100 would be printed. The preview version would show
        # type and some of the items in the format of
        #   int [1:1000] 1 2 3 4 5 6 7 8 9 10 ...
    #    assert 'int' in output and '3' in output and '9' in output and '111' not in output
        #
        # return 'Unknown variable' for unknown variable
    #    assert 'Unknown variable' in notebook.check_output(
    #        '%preview -n unknown_var', kernel="R")
        #
        # return 'Unknown variable for expression
    #    assert 'Unknown variable' in notebook.check_output(
    #        '%preview -n var[1]', kernel="R")

    def test_sessioninfo(self, notebook):
        '''test support for %sessioninfo'''
        notebook.call('System.out.println("This is Java")', kernel="Java")
        assert 'Java' in notebook.check_output(
            '%sessioninfo', kernel="SoS")

    def teardown(self):
        time.sleep(5)
