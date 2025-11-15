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

    vex_keywords = (words(VEX_KEYWORDS, suffix=r'\b'), Keyword.Reserved)
    vex_types = (words(VEX_TYPES, suffix=r'\b'), Keyword.Type)
    vex_functions = (words(VEX_FUNCTIONS, suffix=r'\b'), Keyword.Type)
    # vex_preprocessor = (words(VEX_PREPROCESSOR, prefix=r'^#', suffix=r'.*?\n'), Comment.Preproc)

    tokens = {
        'root': [
            (r'\n', Whitespace),
            (r'\s+', Whitespace),
            (r'^#.*?\n', Comment.Preproc),

            (r'//.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment-multiline'),

            # Vex wrangles can inject expressions in backtick strings, macro-like
            (r'`', String, 'string-backtick'), # should be first, h-expression eval early
            
            # Keywords
            vex_keywords,
            vex_types,

            # Floats [todo, test 0.000_000_01]
            (r'[0-9]+\.[0-9]+([eE][-+]?[0-9]+)?', Number.Float),
            #(r'[0-9]+\.(?:[0-9][0-9][0-9]_)+[0-9]+', Number.Float),
            #(r'[0-9]+\.?[eE][-+]?[0-9]+', Number.Float),

            # Integers [todo, test 1_000_000]
            (r'0b[01]+', Number.Bin),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),
            #(r'[0-9]+(?:_[0-9][0-9][0-9])+', Number.Integer),

            # Identifier
            (r'[fuvpi234sd]?@[a-zA-Z_]\w*', Name.Builtin),
            (r'[a-zA-Z_]\w*', Name),
            
            # Strings
            (r'"', String, 'string-double'),
            (r"'", String, 'string-single'),

            # Operators, Punctuation
            (r'[+%=><|^!?/\-*&~:@]', Operator),
            (r'[{}()\[\],.;]', Punctuation)
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
        ],
        'comment-multiline': [
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^*]+', Comment.Multiline),
            (r'\*', Comment.Multiline),
        ]
    }

    def get_tokens_unprocessed(self, text, stack=('root',)):

        #for index, token, value in CLexer.get_tokens_unprocessed(self, text, stack):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            # if token is String:
            #     print(value)
            if token is Name:
                print(value)
                if value in VEX_FUNCTIONS:
                    token = Name.Function
            yield index, token, value

#if __name__ == '__main__':
#    print(VEX_KEYWORDS)