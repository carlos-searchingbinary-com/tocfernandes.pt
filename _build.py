#!/usr/bin/env python3
"""Generate en/ es/ fr/ from the Portuguese pages in the repo root.

The root pages are the source of truth. Run `python3 _build.py` after editing them;
it fails if any Portuguese text has no translation in _i18n.py.
"""
import re, sys, pathlib
from _i18n import T, KEEP, LEGAL_NOTE

ROOT = pathlib.Path(__file__).parent
SITE = "https://tocfernandes.pt/"
PAGES = ["index.html", "privacidade.html", "cookies.html", "termos.html"]
LANGS = ["pt", "en", "es", "fr"]
NAMES = {"pt": "Português", "en": "English", "es": "Español", "fr": "Français"}
HTML_LANG = {"pt": "pt-PT", "en": "en", "es": "es", "fr": "fr"}
CUR = ' aria-current="true"'
ATTRS = re.compile(r'\b(alt|aria-label)="([^"]*)"')


def url(page, lang, frm):
    """Relative link to `page` in `lang`, from a page that lives in language `frm`."""
    up = "" if frm == "pt" else "../"
    return (up + ("" if lang == "pt" else lang + "/") + ("" if page == "index.html" else page)) or "./"


def between(s, name, new):
    a, b = f"<!--{name}-->", f"<!--/{name}-->"
    assert s.count(a) == 1 and s.count(b) == 1, f"marker {name} missing"
    return s[: s.index(a) + len(a)] + new + s[s.index(b):]


def chrome(s, page, lang):
    """Language switcher and hreflang links, regenerated for every page (pt included)."""
    links = "".join(
        f'<a href="{url(page, l, lang)}" lang="{l}" hreflang="{l}" title="{NAMES[l]}"'
        f'{CUR if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    s = between(s, "langs", f'<nav class="langs" aria-label="Idioma / Language">{links}</nav>')
    p = "" if page == "index.html" else page
    alts = "".join(f'\n<link rel="alternate" hreflang="{l}" href="{SITE}{"" if l == "pt" else l + "/"}{p}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{p}">\n'
    return between(s, "hreflang", alts)


def translate(s, lang, missing):
    i = LANGS.index(lang) - 1

    def tr(text):
        core = text.strip()
        if not core or core in KEEP or not re.search(r"[A-Za-zÀ-ÿ]{2}", core):
            return text
        if core not in T:
            missing.add(core)
            return text
        return text.replace(core, T[core][i])

    out, skip = [], None
    for part in re.split(r"(<[^>]+>)", s):
        if part.startswith("<"):
            m = re.match(r"<(/?)(script|style)\b", part)
            if m:
                skip = None if m.group(1) else m.group(2)
            if part.startswith("<meta name=\"description\""):
                part = re.sub(r'content="([^"]*)"', lambda m: f'content="{tr(m.group(1))}"', part)
            elif not part.startswith(("<!--", "<link")):
                part = ATTRS.sub(lambda m: f'{m.group(1)}="{tr(m.group(2))}"', part)
            out.append(part)
        else:
            out.append(part if skip else tr(part))
    return "".join(out)


def main():
    missing = set()
    for page in PAGES:
        src = chrome((ROOT / page).read_text(), page, "pt")
        (ROOT / page).write_text(src)
        for lang in LANGS[1:]:
            s = chrome(src, page, lang)
            s = translate(s, lang, missing)
            s = s.replace('<html lang="pt-PT">', f'<html lang="{HTML_LANG[lang]}">')
            s = re.sub(r'(href|src)="assets/', r'\1="../assets/', s)
            s = s.replace("docs.github.com/pt/", f"docs.github.com/{lang}/")
            if page != "index.html":
                a = '<main class="wrap">\n'
                assert s.count(a) == 1
                s = s.replace(a, a + f'  <p class="note">{LEGAL_NOTE[lang]}</p>\n')
            (ROOT / lang).mkdir(exist_ok=True)
            (ROOT / lang / page).write_text(s)
    if missing:
        sys.exit("No translation in _i18n.py for:\n  " + "\n  ".join(sorted(missing)))
    unused = [k for k in T if not any(k in (ROOT / p).read_text() for p in PAGES)]
    if unused:
        sys.exit("Translations in _i18n.py no longer used by any page:\n  " + "\n  ".join(unused))
    print(f"built {len(PAGES)} pages x {len(LANGS) - 1} languages")


if __name__ == "__main__":
    main()
