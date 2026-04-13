import gettext

# first var

# translation = gettext.translation("words", "po", fallback=True)
# _ = translation.gettext

# while True:
#     try:
#         line = input()
#         n = len(line.split())
#         print(_("Entered {n} word(s)").format(n=n))
#     except EOFError:
#         break

# sec var

import locale

locale = locale.setlocale(locale.LC_ALL, locale.getlocale())
translation = gettext.translation("wordcount", "po", fallback=True)
_, ngettext = translation.gettext, translation.ngettext

words = input().split()
n = len(words)
print(ngettext("Entered {} word", "Entered {} words", n).format(n))