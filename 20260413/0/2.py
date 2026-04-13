import gettext
import locale

locale = locale.setlocale(locale.LC_ALL, locale.getlocale())
translation = gettext.translation("wordcount", "po", fallback=True)
tolmatch = gettext.translation("wordcounter", fallback=True)
ngettext, ngette = translation.ngettext, tolmatch.ngettext

words = input().split()
n = len(words)
print(ngettext("Entered {} word", "Entered {} words", n).format(n))
print(ngette("Entereth {} worde", "Entereth {} words", n).format(n))