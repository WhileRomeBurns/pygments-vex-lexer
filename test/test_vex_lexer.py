import os
import sys

from pygments import highlight
from pygments.formatters import HtmlFormatter

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import PygmentsVexLexer


lexer = PygmentsVexLexer.VexLexer()
formatter = HtmlFormatter(style='default', full=True, linenos=True)
#formatter = HtmlFormatter(style='monokai', full=True, linenos=True)

with open("./test/test.vfl", "r") as f:
    code = f.read()

with open("./test/test.html", "w") as f:
    f.write( highlight(code, lexer, formatter))