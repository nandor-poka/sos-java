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


    def test_preview(self, notebook):
        '''Test support for %preview'''
        output = notebook.check_output(
            '''\
            %preview -n var
            int var = 102;
           ''',
            kernel="Java")
        assert '> var: Integer'in output and '102' in output 

    def test_sessioninfo(self, notebook):
        '''test support for %sessioninfo'''
        notebook.call('System.out.println("This is Java")', kernel="Java")
        assert 'Java' in notebook.check_output(
            '%sessioninfo', kernel="SoS")
