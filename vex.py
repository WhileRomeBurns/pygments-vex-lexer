"""
    Vex Lexer
"""

import os
import re

from pygments.lexer import RegexLexer, include, bygroups, inherit, words, \
    default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Whitespace

#from pygments.lexers.c_cpp import CLexer, CppLexer
#from pygments.lexers import _mql_builtins

try:
    __file__
except NameError:
    __file__ = 'vex.py'

_ROOT = os.path.abspath(os.path.dirname(__file__))
_ROOT = os.path.join(_ROOT, 'syntax')

with open(os.path.join(_ROOT, "VexKeywords.txt")) as f:
    VEX_KEYWORDS = f.read().split()
with open(os.path.join(_ROOT, "VexFunctions.txt")) as f:
    VEX_FUNCTIONS = f.read().split()
with open(os.path.join(_ROOT, "VexTypes.txt")) as f:
    VEX_TYPES = f.read().split()
with open(os.path.join(_ROOT, "VexPredefined.txt")) as f:
    VEX_PREDEFINED = f.read().split()
with open(os.path.join(_ROOT, "VexPreprocessor.txt")) as f:
    VEX_PREPROCESSOR = f.read().split()

class VexLexer(RegexLexer):
#class VexLexer(CLexer):
    """
    For Side Effects Vex source.
    """
    name = 'VexLexer'
    filenames = ['*.vfl', '*.vex']
    aliases = ['vfl', 'vex']
    mimetypes = ['text/vex']
    url = ''
    version_added = '1.0'

    tokens = {
        'root': [
            (r'`', String, 'string-backtick'), # should be first, h-expression eval early
            (r'"', String, 'string-double'),
            (r"'", String, 'string-single'),
        ],
        'string-backtick': [
            (r'`', String, '#pop'),
            (r'[^`]+?', String),
            #(r'[^`]+?', String),
        ],
        'string-double': [
            (r'"', String, '#pop'),
            (r'[^"]+?', String),
        ],
        'string-single': [
            (r"'", String, '#pop'),
            (r"[^']+?", String),
        ]
        # 'root': [
        #     #(r"`([^`])*`", String.Backtick),
        #     (r"`[^`]*`", String.Backtick),
        #     #(r'`.*?`', String),
        #     inherit,
        # ],
        # 'string': [
        #     (r"`", String, '#push'),
        #     (r"`", String, '#pop')
        #     #(r'`.*?`', String),
        # ],
        # 'string': [
        #     (r"`", String.Other, '#push'),
        #     (r"`", String.Other, '#pop')
        # ],
    }
    # tokens = {
    #     'comment': [
    #         (r"'", Comment.Multiline, '#push'),
    #         (r"'", Comment.Multiline, '#pop')
    #     ]
    # }

    # function_qualifiers = {'__device__', '__global__', '__host__',
    #                        '__noinline__', '__forceinline__'}
    # variable_qualifiers = {'__device__', '__constant__', '__shared__',
    #                        '__restrict__'}
    #variables = {'gridDim', 'blockIdx', 'blockDim', 'threadIdx', 'warpSize'}
    # functions = {'normalize', 'fit', 'fit01',
    #              'ch', 'chramp', 'pciterate',
    #              'pcopen'}
    # execution_confs = {'<<<', '>>>'}

    def get_tokens_unprocessed(self, text, stack=('root',)):

        #for index, token, value in CLexer.get_tokens_unprocessed(self, text, stack):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            # if token is String:
            #     print(value)
            if token is Name:
                #if value in self.variable_qualifiers:
                #    token = Keyword.Type
                if value in VEX_TYPES:
                    token = Keyword.Type
                #elif value in self.variables:
                #    token = Name.Builtin
                #elif value in self.execution_confs:
                #    token = Keyword.Pseudo
                #elif value in self.function_qualifiers:
                #    token = Keyword.Reserved
                elif value in VEX_FUNCTIONS:
                    token = Name.Function
            yield index, token, value

#if __name__ == '__main__':
#    print(VEX_KEYWORDS)