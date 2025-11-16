from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import load_lexer_from_file

lexer = load_lexer_from_file("VexLexer.py", lexername="VexLexer")
formatter = HtmlFormatter(style='default', full=True, linenos=True)
#formatter = HtmlFormatter(style='monokai', full=True, linenos=True)

with open("test.vfl", "r") as f:
    code = f.read()
with open("voplib.h", "r") as f:
    code2 = f.read()

with open("test.html", "w") as f:
    f.write( highlight(code, lexer, formatter))
with open("voplib.html", "w") as f:
    f.write( highlight(code2, lexer, formatter))
