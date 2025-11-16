"""
    Pygments Lexer for Side Effects Software's Vex and Vex Wrangle source code.
    Function names were generated for Houdini 21 via the vcc compiler. See
    /syntax/syntax.py for details.
"""
__author__  = "Shawn Lipowski"
__email__   = "vfxcodeblog@gmail.com"
__date__    = "2025-11-16"
__version__ = "1.0.0"
__license__ = "MIT"


import os
import re

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Whitespace

try:
    __file__
except NameError:
    __file__ = 'PygmentsVexLexer.py' # for vscode dev


_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'syntax')

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
with open(os.path.join(_ROOT, "VexConstants.txt")) as f:
    VEX_CONSTANTS = f.read().split()
with open(os.path.join(_ROOT, "VexContexts.txt")) as f:
    VEX_CONTEXTS = f.read().split()


class VexLexer(RegexLexer):
    """
    Lexer for Side Effects Software's Vex and Vex Wrangle source.
    """
    name = 'Vex'
    filenames = ['*.vfl', '*.vex', '*.h']
    aliases = ['vfl', 'vex', 'vexwrangle']
    mimetypes = ['text/vex']
    url = 'https://www.sidefx.com/'
    version_added = '1.0.0'

    vex_keywords = (words(VEX_KEYWORDS, suffix=r'\b'), Keyword.Reserved)
    vex_types = (words(VEX_TYPES, suffix=r'\b'), Keyword.Type)
    vex_functions = (words(VEX_FUNCTIONS, suffix=r'\b(\s)*?(\()'), bygroups(Name.Function, Whitespace, Punctuation))
    vex_predefined = (words(VEX_PREDEFINED, suffix=r'\b'), Name.Variable.Magic)
    vex_preprocessor = (words(VEX_PREPROCESSOR, suffix=r'\b'), Comment.Preproc)
    vex_constants = (words(VEX_CONSTANTS, suffix=r'\b'), Name.Constant)
    vex_contexts = (words(VEX_CONTEXTS, suffix=r'\b'), Keyword.Namespace)

    tokens = {
        'root': [
            (r'\n', Whitespace),
            (r'\s+', Whitespace),

            # Comments
            (r'//.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment-multiline'),

            # Expression Strings (wrangle string replacement)
            (r'`', String, 'string-backtick'),
            
            # Keywords and Types
            vex_keywords,
            vex_types,
            vex_predefined,
            vex_constants,
            vex_contexts,
            vex_preprocessor,

            # Floats
            (r'[0-9]+\.f', Number.Float),
            (r'[0-9]+\.[0-9]+f', Number.Float),
            (r'[0-9]+\.(?:[0-9][0-9][0-9]_)+[0-9]+', Number.Float),
            (r'[0-9]+\.(?:[eE][-+]?[0-9]+)?', Number.Float),
            (r'[0-9]+\.[0-9]+(?:[eE][-+]?[0-9]+)?', Number.Float),

            # Integers
            (r'0b[01]+', Number.Bin),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+(?:_[0-9][0-9][0-9])+', Number.Integer),
            (r'[0-9]+(?:[eE][-+]?[0-9]+)?', Number.Integer),

            # Wrangle Binding Identifier
            (r'[fuvpi234sd]+(?:\[\])?@[a-zA-Z_]\w*', Name.Variable),
            (r'@[a-zA-Z_]\w*', Name.Variable),

            # Identifier
            (r'[a-zA-Z_]\w*', Name),
            
            # Strings
            (r'"', String, 'string-double'),
            (r"'", String, 'string-single'),

            # Operators, Punctuation
            (r'[+%=><|^!?/\-*&~:@\\]', Operator),
            (r'[{}()\[\],.;]', Punctuation)
        ],
        'string-backtick': [
            (r'`', String, '#pop'),
            (r'[^`]+?', String),
        ],
        'string-double': [
            (r'\\"', String), # escape
            (r'"', String, '#pop'),
            (r'[^"]+?', String),
        ],
        'string-single': [
            (r"\\'", String), # escape
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

        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name:
                if value in VEX_FUNCTIONS:
                    start = index + len(value)
                    if start < len(text):
                        if re.match(r'\s*?\(', text[start:]):
                            token = Name.Function
            yield index, token, value
