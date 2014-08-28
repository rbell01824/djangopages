#!/usr/bin/env python
# coding=utf-8

""" Support user defined classes built from strings.

8/28/14 - Initial creation

"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '8/28/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ['rbell01824']
__license__ = 'All rights reserved'
__version__ = '0.1'
__maintainer__ = 'rbell01824'
__email__ = 'rbell01824@gmail.com'

import sys


# class Singleton(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
#
#
# class X(object):
#     __metaclass__ = Singleton
#
#     def __init__(self, code):
#         DPageUserPages.xglobal(code)
#         return


# noinspection PyClassHasNoInit
class DUserPage(object):
    """ DjangoPages User Pages

    .. sourcecode:: python
        DUserPage(source_code)

    Used to compile source_code.  If compile is error free, the code is exec(ed) and any objects created
    saved as attributes of DUserPage and DUserPage.errors set to None.  Otherwise,
    DUserPage.errors is set to error text hopefully useful for finding the error in the source_code.

    :param code: DPage and other class code
    :type code: str or unicode
    :return: None, sets DUserPage.objs to objects created.  Sets DUserPage.errors to error text.
    """

    @classmethod
    def __init__(cls, code):
        """
        :param code: DPage and other class code
        :type code: str or unicode
        :return: None, sets DUserPage.objs to objects created.  Sets DUserPage.errors to error text.
        """
        cls.objs, cls.errors = cls.xglobal(code)
        return

    @classmethod
    def compile(cls, code):
        """ Compile code string and return compile object and error string

        :param code: code string to compile
        :type code: str or unicode
        :return: tuple of compile_obj, error_string.  If compile_obj is None, there were errors; otherwise compile was
                successful
        :rtype: tuple
        """
        # noinspection PyBroadException
        try:                                # compile
            compile_obj = compile(code, "<string>", 'exec')
            # exec(code)
            error_msg = None
        except:                             # had compile error
            compile_obj = None
            exception = sys.exc_info()[0]
            error_msg = "compile error: {}\n".format(exception)
            error_args = sys.exc_info()[1]
            error_msg += 'error line {}\n'.format(error_args.lineno, error_args.msg)
            lines = code.split('\n')
            l1 = min(error_args.lineno-4, 0)
            l2 = min(error_args.lineno+4, len(lines))
            line_number = l1 + 1
            for l in lines[l1:l2]:
                error_marker = '' if line_number != error_args.lineno else ' <----- {}'.format(error_args.args[0])
                error_msg += '{}: {}{}\n'.format(line_number, l, error_marker)
                line_number += 1
        return compile_obj, error_msg

    @classmethod
    def xexec(cls, code):
        """ Compile code and return dict of compiled objects and error string.

        :param code: code
        :type code: str or unicode
        :return: tuple of dict_of_compiled_objects, error_string
        :rtype: tuple
        """
        compile_obj, errors = cls.compile(code)
        if not compile_obj:
            return compile_obj, errors
        global_dict = dict()
        local_dict = dict()
        exec(compile_obj, global_dict, local_dict)
        return local_dict, errors

    @classmethod
    def xglobal(cls, code):
        """ Compile code and return dict of compiled objects and error string.

        :param code: code
        :type code: str or unicode
        :return: tuple of dict_of_compiled_objects, error_string
        :rtype: tuple
        """
        objs_dict, errors = cls.xexec(code)
        if not objs_dict:
            return objs_dict, errors
        for key, value in objs_dict.items():
            setattr(cls, key, value)
        return objs_dict, errors
DUP = DUserPage
