#!/usr/bin/env python
# coding=utf-8

""" userpages support routines

8/27/14 - Initial creation

"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '8/27/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ['rbell01824']
__license__ = 'All rights reserved'
__version__ = '0.1'
__maintainer__ = 'rbell01824'
__email__ = 'rbell01824@gmail.com'

#######################################################################################################################
#
# prototype code for how to exec string and save into a namespace as an object
#
#######################################################################################################################
#
# import sys
# import __builtin__
# import my_globals
#
# cls1 = 'class CLS1(object):\n' \
#        '    def __init__(self):\n' \
#        '        self.v1 = 1\n' \
#        '    def f1(self, v2):\n' \
#        '        return self.v1 + v2\n'
# cls2 = """class CLS2(object):
#     def __init__(self):
#         self.v1 = 1
#     def f1(self, v2):
#         return self.v1 + v2"""
# cls3 = """
# class CLS3(object):
#     def __init__(self):
#         self.v1 = 1
#     def f1(self, v2):
#         return self.v1 + v2"""
# cls4 = """
# class CLS4(object):
#     def __init__(self):
#         self.v1 = 1
#     def f1(self, v2):
#         return self.v1 + v2"""
#
#
# class STR_Test(object):
#     def __init__(self):
#         self.v1 = '1'
#         return
#     def f1(self, v2):
#         return self.v1 + v2
#
# class global_injector:
#     '''Inject into the *real global namespace*, i.e. "builtins" namespace or "__builtin__" for python2.
#     Assigning to variables declared global in a function, injects them only into the module's global namespace.
#     >>> Global= sys.modules['__builtin__'].__dict__
#     >>> #would need
#     >>> Global['aname'] = 'avalue'
#     >>> #With
#     >>> Global = global_injector()
#     >>> #one can do
#     >>> Global.bname = 'bvalue'
#     >>> #reading from it is simply
#     >>> bname
#     bvalue
#
#     '''
#     def __init__(self):
#         try:
#             self.__dict__['builtin'] = sys.modules['__builtin__'].__dict__
#         except KeyError:
#             self.__dict__['builtin'] = sys.modules['builtins'].__dict__
#     def __setattr__(self,name,value):
#         self.builtin[name] = value
# Global = global_injector()
#
#
# def main():
#     # c_local = {}
#     # c_global = {}
#     # print cls1
#     exec 'class HI: pass'
#     print locals()['HI']
#     exec('class HO(object): pass')
#     print locals()['HO']
#     he = 'class HE(object):\n' \
#          '    def __init__(self):\n' \
#          '        self.v1 = 1\n' \
#          '    def f1(self, v2):\n' \
#          '        return self.v1 + v2\n'
#     exec(he)
#     print locals()['HE']
#     exec(cls1)
#     print locals()['CLS1']
#     exec(cls2)
#     print locals()['CLS2']
#     exec(cls3)
#     print locals()['CLS3']
#     exec(cls4)
#     print locals()['CLS4']
#     Global.CLS4 = locals()['CLS4']
#     __builtin__.CLS4a = locals()['CLS4']
#     my_globals.CLS4 = locals()['CLS4']
#     print CLS4, CLS4a, my_globals.CLS4
#     hehehe = my_globals.CLS4()
#     print hehehe.f1(3), 'should be 4'
#     return
#
# if __name__ == "__main__":
#     main()

#######################################################################################################################
#
# Prototype code for how to compile and get error messages for class as a string
#
#######################################################################################################################
#
# import sys
# import StringIO
#
# # create file-like string to capture output
# codeOut = StringIO.StringIO()
# codeErr = StringIO.StringIO()
#
# code = """
# def f(x):
#     x = x + 1
#         print 'error'
#     return x
#
# print 'This is my output.'
# """
#
# # capture output and errors
# sys.stdout = codeOut
# sys.stderr = codeErr
#
# try:
#     cd = compile(code, "<string>", 'exec')
#     exec(code)
#     print f(4)
# except:
#     print "compile error:", sys.exc_info()[0]
#     e = sys.exc_info()[1]
#     ln = e.args[1][1]
#     print 'error line {}'.format(ln, e.args[0])
#     lines = code.split('\n')
#     l1 = min(e.lineno-4, 0)
#     l2 = min(e.lineno+4, len(lines))
#     lo = l1+1
#     for l in lines[l1:l2]:
#         print lo, ':', l, '' if ln!=lo else ' <----- {}'.format(e.args[0])
#         lo += 1
#     pass
#
# # restore stdout and stderr
# sys.stdout = sys.__stdout__
# sys.stderr = sys.__stderr__
#
# s = codeErr.getvalue()
# print "error:\n%s\n" % s
#
# s = codeOut.getvalue()
#
# print "output:\n%s" % s
#
# codeOut.close()
# codeErr.close()