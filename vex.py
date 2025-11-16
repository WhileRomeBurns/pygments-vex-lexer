"""
    Vex Lexer
"""
import os
import re

from pygments.lexer import RegexLexer, bygroups, inherit, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Whitespace

try:
    __file__
except NameError:
    __file__ = 'vex.py'

_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'syntax')

with open(os.path.join(_ROOT, "VexKeywords.txt")) as f:
    VEX_KEYWORDS = f.read().split()
with open(os.path.join(_ROOT, "VexFunctions.txt")) as f:
    VEX_FUNCTIONS = f.read().split()
with open(os.path.join(_ROOT, "VexTypes.txt")) as f:
    VEX_TYPES = f.read().split()
with open(os.path.join(_ROOT, "VexPredefined.txt")) as f:
    VEX_PREDEFINED = f.read().split()
with open(os.path.join(_ROOT, "VexConstants.txt")) as f:
    VEX_CONSTANTS = f.read().split()
with open(os.path.join(_ROOT, "VexContexts.txt")) as f:
    VEX_CONTEXTS = f.read().split()

class VexLexer(RegexLexer):
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
    vex_functions = (words(VEX_FUNCTIONS, suffix=r'\b(\s)*?(\()'), bygroups(Name.Function, Whitespace, Punctuation))
    vex_predefined = (words(VEX_PREDEFINED, suffix=r'\b'), Name.Builtin)
    vex_constants = (words(VEX_CONSTANTS, suffix=r'\b'), Name.Constant)
    vex_contexts = (words(VEX_CONTEXTS, suffix=r'\b'), Keyword.Namespace)

    tokens = {
        'root': [
            (r'\n', Whitespace),
            (r'\s+', Whitespace),
            (r'^#.*?\n', Comment.Preproc),

            (r'//.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment-multiline'),

            # Backtick Expression Strings
            (r'`', String, 'string-backtick'),
            
            # Keywords
            vex_keywords,
            vex_types,
            #vex_functions,
            vex_predefined,
            vex_constants,
            vex_contexts,

            # Floats
            (r'[0-9]+\.(?:[0-9][0-9][0-9]_)+[0-9]+', Number.Float),
            (r'[0-9]+\.(?:[eE][-+]?[0-9]+)?', Number.Float),
            (r'[0-9]+\.[0-9]+(?:[eE][-+]?[0-9]+)?', Number.Float),
            
            # Integers
            (r'0b[01]+', Number.Bin),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+(?:_[0-9][0-9][0-9])+', Number.Integer),
            (r'[0-9]+(?:[eE][-+]?[0-9]+)?', Number.Integer),

            # Identifier, match bindings like v[]@ and v@ first and then known types @
            (r'[fuvpi234sd]+(?:\[\])?@[a-zA-Z_]\w*', Name.Builtin),
            (r'@[a-zA-Z_]\w*', Name.Builtin),
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

        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name:
                if value in VEX_FUNCTIONS:
                    start = index + len(value)
                    if start < len(text):
                        match = re.match(r'\s*?\(', text[start:])
                        if match:
                            token = Name.Function
            yield index, token, value
