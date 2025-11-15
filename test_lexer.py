from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import load_lexer_from_file

lexer = load_lexer_from_file("vex.py", lexername="VexLexer")

with open("test.vfl", "r") as f:
    code = f.read()

formatter = HtmlFormatter(style='monokai', full=True, linenos=True)
#formatter = HtmlFormatter(style='default', full=True, linenos=True)
highlighted_code = highlight(code, lexer, formatter)

with open("test.html", "w") as f:
  f.write(highlighted_code)

# css_styles = formatter.get_style_defs('.highlight')
# with open("pygments_style.css", "w") as f:
#     f.write(css_styles)