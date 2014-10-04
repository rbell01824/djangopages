#!/usr/bin/env python
# coding=utf-8

""" Some description here

10/2/14 - Initial creation

"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '10/2/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ['rbell01824']
__license__ = 'All rights reserved'
__version__ = '0.1'
__maintainer__ = 'rbell01824'
__email__ = 'rbell01824@gmail.com'

from django.test import TestCase

from widgets.texthtml import text, markdown, loremipsum, dup


class TestText(TestCase):

    def test_simple_case(self):
        rtn = text('some text')
        self.assertEqual(rtn, 'some text')

    def test_list(self):
        rtn = text(('string 1', ' string 2'))
        self.assertEqual(rtn, 'string 1 string 2')
        rtn = text(['string 1', ' string 2'])
        self.assertEqual(rtn, 'string 1 string 2')

    def test_para(self):
        rtn = text('some string', para=True)
        self.assertEqual(rtn, '<p class="" style="">some string</p>')

    def test_para_with_classes_and_style(self):
        rtn = text('some string', para=True, classes='class_1 class_2', style='style_1')
        self.assertEqual(rtn, '<p class="class_1 class_2" style="style_1">some string</p>')

    def test_classes_and_style(self):
        rtn = text('some string', classes='class_1 class_2', style='style_1')
        self.assertEqual(rtn, '<span class="class_1 class_2" style="style_1">some string</span>')

    def test_para_iterable(self):
        rtn = text(['para 1', 'para 2'], para=True, classes='class_1', style='style_1')
        self.assertEqual(rtn, '<p class="class_1" style="style_1">para 1</p>'
                              '<p class="class_1" style="style_1">para 2</p>')


class TestMarkdown(TestCase):

    def test_simple_case(self):
        rtn = markdown('some text')
        self.assertEqual(rtn, '<p>some text</p>')

    def test_list(self):
        rtn = markdown(['para 1', 'para 2'])
        self.assertEqual(rtn, '<p>para 1</p><p>para 2</p>')


class TestLoremipsum(TestCase):

    def test_simple_case(self):
        rtn = loremipsum(2)
        self.assertTrue(rtn.startswith('<p class="" style="">'))
        self.assertTrue(rtn.endswith('</p>'))
        self.assertEqual(rtn.count('.'), 2)

    def test_list(self):
        rtn = loremipsum([2, 1])
        self.assertTrue(rtn.startswith('<p class="" style="">'))
        self.assertTrue(rtn.endswith('</p>'))
        self.assertEqual(rtn.count('<p class="" style="">'), 2)
        self.assertEqual(rtn.count('</p>'), 2)
        self.assertEqual(rtn.count('.'), 3)

    def test_para_false(self):
        rtn = loremipsum(2, para=False)
        self.assertFalse(rtn.startswith('<p class="" style="">'))
        self.assertFalse(rtn.endswith('</p>'))
        self.assertEqual(rtn.count('.'), 2)

    def test_para_with_classes_and_style(self):
        rtn = loremipsum(2, classes='class_1', style='style_1')
        self.assertTrue(rtn.startswith('<p class="class_1" style="style_1">'))
        self.assertTrue(rtn.endswith('</p>'))
        self.assertEqual(rtn.count('.'), 2)

    def test_classes_and_style(self):
        rtn = loremipsum(2, para=False, classes='class_1', style='style_1')
        self.assertTrue(rtn.startswith('<span class="class_1" style="style_1">'))
        self.assertTrue(rtn.endswith('</span>'))
        self.assertEqual(rtn.count('.'), 2)


class TestDup(TestCase):

    def test_simple_case(self):
        rtn = dup('string', 2)
        self.assertEqual(rtn, 'stringstring')

    def test_list(self):
        rtn = dup(['a', 'b'], 2)
        self.assertEqual(rtn, 'aabb')

    def test_classes_style(self):
        rtn = dup('a', 3, classes='class_1', style='style_1')
        self.assertEqual(rtn, '<span class="class_1" style="style_1">aaa</span>')
