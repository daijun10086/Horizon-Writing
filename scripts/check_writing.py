#!/usr/bin/env python3
"""Flag patterns in a draft that the horizon-writing skill discourages.

Usage:
    python3 check_writing.py draft.md [more files ...]
    python3 check_writing.py - < draft.md          # read from stdin
    python3 check_writing.py --only words draft.md

Checks (all on by default):
    words      discouraged words and phrases from references/word-list.txt
    acronyms   abbreviations used before they are defined, such as "TLB"
               without "translation lookaside buffer (TLB)" at or before it
    sentences  sentences longer than --max-words words (default 35)
    dashes     em dashes, which AI prose overuses
    contrast   "it's not X, it's Y" and "not just X, but Y" framing

Each finding asks you to reread the sentence. It is not an order to change it:
a listed word is fine when it is the most precise word in its literal sense.
Code blocks, inline code, URLs, HTML comments, and LaTeX citations and math
are skipped.

Exit status: 0 when nothing is found, 1 when something is found, 2 on errors.
Needs only the Python 3 standard library.
"""

import argparse
import bisect
import os
import re
import sys

CHECKS = ("words", "acronyms", "sentences", "dashes", "contrast")

DEFAULT_LIST = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "references", "word-list.txt"
)

# Abbreviations that almost every reader in computing already knows.
# Add your own with --allow.
COMMON_ACRONYMS = set("""
AI API APIs CPU CPUs GPU GPUs TPU RAM ROM OS CS ECE EE US USA UK EU PDF PDFs
HTML CSS JSON XML YAML CSV TSV URL URLs URI HTTP HTTPS TCP UDP IP DNS SSH SSL
TLS SQL IO USB PC PCs ID IDs OK PhD IEEE ACM USENIX NSF DARPA NIH TODO FIXME
README LICENSE MIT GPL BSD CLI GUI UI UX IDE SDK LLM LLMs ML PR PRs CI VM VMs
GB MB KB TB PB AM PM FAQ ASCII UTF NASA AWS PNG JPG JPEG SVG MD CEO CTO
""".split())

ROMAN = re.compile(r"^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$")


# ---------------------------------------------------------------- word list

class Entry:
    def __init__(self, forms, exceptions, group):
        self.forms = forms
        self.group = group
        self.label = forms[0]
        alternatives = set()
        for form in forms:
            alternatives.update(expand_form(form))
        body = "|".join(
            phrase_regex(a) for a in sorted(alternatives, key=len, reverse=True)
        )
        # Word boundaries on both sides, and do not match "won" in "won't".
        self.regex = re.compile(r"(?<![\w])(?:" + body + r")(?![\w])(?!['\u2019]t\b)",
                                re.IGNORECASE)
        self.exceptions = [
            re.compile(r"(?<![\w])" + phrase_regex(e) + r"(?![\w])", re.IGNORECASE)
            for e in exceptions
        ]


class Group:
    def __init__(self, name):
        self.name = name
        self.why = ""
        self.instead = ""


def expand_form(form):
    """Return the form plus its regular inflections (bet -> bets, betting, ...)."""
    form = form.strip().lower()
    if " " in form or not form.isalpha():
        return {form}
    out = {form}
    for suffix in ("s", "es", "ed", "d", "ing", "ly"):
        out.add(form + suffix)
    if form.endswith("e"):
        out.update({form[:-1] + "ing", form[:-1] + "ed"})
    if len(form) > 2 and form.endswith("y") and form[-2] not in "aeiou":
        out.update({form[:-1] + "ies", form[:-1] + "ied", form[:-1] + "ily"})
    # Short consonant-vowel-consonant words double the last letter: bet -> betting.
    if (len(form) >= 3 and form[-1] not in "aeiouwxy" and form[-2] in "aeiou"
            and form[-3] not in "aeiou"):
        out.update({form + form[-1] + "ing", form + form[-1] + "ed"})
    return out


def phrase_regex(phrase):
    """Escape a phrase and let any run of whitespace separate its words."""
    words = phrase.strip().split()
    return r"\s+".join(re.escape(w).replace("'", "['\u2019]") for w in words)


def load_word_list(path):
    groups, entries = {}, []
    current = Group("ungrouped")
    groups[current.name] = current
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                comment = line.lstrip("#").strip()
                key, _, value = comment.partition(":")
                key = key.strip().lower()
                if key == "group" and value.strip():
                    current = groups.setdefault(value.strip(), Group(value.strip()))
                elif key == "why":
                    current.why = value.strip()
                elif key == "instead":
                    current.instead = value.strip()
                continue
            forms_part, _, rest = line.partition("|")
            forms = [f.strip() for f in forms_part.split(",") if f.strip()]
            exceptions = []
            rest = rest.strip()
            if rest.lower().startswith("except:"):
                exceptions = [e.strip() for e in rest[len("except:"):].split(",")
                              if e.strip()]
            if forms:
                entries.append(Entry(forms, exceptions, current))
    return groups, entries


# ---------------------------------------------------------------- masking

def mask(text):
    """Blank out code, URLs, comments, and LaTeX references and math.

    Masked characters become spaces (newlines stay), so offsets and line
    numbers in the masked text match the original.
    """
    chars = list(text)

    def blank(start, end):
        for i in range(start, end):
            if chars[i] != "\n":
                chars[i] = " "

    patterns = [
        r"^---\n.*?\n---\n",                       # YAML front matter
        r"^(```|~~~).*?^\1[^\n]*$",                # fenced code blocks
        r"<!--.*?-->",                             # HTML comments
        r"`[^`\n]+`",                              # inline code
        r"https?://\S+",                           # URLs
        r"(?<!\\)%[^\n]*",                         # LaTeX comments
        r"\\(?:cite[tp]?|ref|eqref|autoref|cref|Cref|label|url|href|input|include"
        r"|begin|end|usepackage|documentclass)\*?(?:\[[^\]]*\])*\{[^}]*\}",
        r"\$\$.*?\$\$",                            # display math
        r"(?<!\\)\$[^$\n]+\$",                     # inline math
    ]
    for pattern in patterns:
        flags = re.MULTILINE | re.DOTALL
        if pattern.startswith("(?<!\\\\)%") and not looks_like_latex(text):
            continue
        for match in re.finditer(pattern, text, flags):
            blank(match.start(), match.end())
    return "".join(chars)


def looks_like_latex(text):
    return bool(re.search(r"\\(documentclass|section|begin|cite|textbf|emph)\b", text))


# ---------------------------------------------------------------- checks

class Finding:
    def __init__(self, offset, kind, message, group=None):
        self.offset = offset
        self.kind = kind
        self.message = message
        self.group = group


def check_words(masked, entries):
    candidates = []
    for entry in entries:
        skip = []
        for exc in entry.exceptions:
            skip.extend((m.start(), m.end()) for m in exc.finditer(masked))
        for match in entry.regex.finditer(masked):
            if any(s <= match.start() and match.end() <= e for s, e in skip):
                continue
            candidates.append((match.start(), match.end(), entry))
    # Keep the longest match where matches overlap ("trade-off" over "trade").
    candidates.sort(key=lambda c: (c[0], -(c[1] - c[0])))
    findings, last_end = [], -1
    for start, end, entry in candidates:
        if start < last_end:
            continue
        last_end = end
        word = " ".join(masked[start:end].split())
        findings.append(Finding(start, "word", '"%s"' % word, entry.group))
    return findings


ACRONYM = re.compile(r"(?<![\w-])([A-Z][A-Z0-9&]*[A-Z][A-Z0-9]*)(s?)(?![\w-])")


def check_acronyms(masked, allowed):
    findings, seen = [], set()
    for match in ACRONYM.finditer(masked):
        acronym = match.group(1)
        if acronym in seen or acronym in allowed or acronym + match.group(2) in allowed:
            continue
        if ROMAN.match(acronym) or len(acronym) > 10:
            continue
        line_start = masked.rfind("\n", 0, match.start()) + 1
        line_end = masked.find("\n", match.end())
        line = masked[line_start:line_end if line_end != -1 else len(masked)]
        letters = [c for c in line if c.isalpha()]
        if letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
            continue  # an all-caps heading, not an abbreviation in prose
        seen.add(acronym)
        esc = re.escape(acronym)
        defined_before = re.search(r"\(\s*" + esc + r"s?\s*[),;]",
                                   masked[:line_end if line_end != -1 else len(masked)])
        defined_here = re.match(r"s?\s*\(", masked[match.end() - len(match.group(2)):])
        if defined_before or defined_here:
            continue
        findings.append(Finding(
            match.start(), "acronym",
            '"%s" is used without a definition at or before this point' % acronym))
    return findings


SENTENCE_END = re.compile(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\u2019-]*")


def check_sentences(masked, max_words):
    findings = []
    # Paragraphs are separated by blank lines; list items and table rows,
    # headings, and block quotes each count as their own paragraph.
    block_start = 0
    blocks = []
    for match in re.finditer(r"\n\s*\n|\n(?=\s*(?:[-*+]|\d+[.)]|#|\||>)\s)", masked):
        blocks.append((block_start, match.start()))
        block_start = match.end()
    blocks.append((block_start, len(masked)))
    for start, end in blocks:
        block = masked[start:end]
        if block.lstrip().startswith("|"):
            continue
        pos = 0
        for piece in SENTENCE_END.split(block) + [None]:
            if piece is None:
                break
            count = len(WORD.findall(piece))
            if count > max_words:
                offset = start + block.find(piece, pos)
                findings.append(Finding(
                    offset + len(piece) - len(piece.lstrip()), "long sentence",
                    "%d words; see whether it is two sentences" % count))
            pos = block.find(piece, pos) + len(piece)
    return findings


def check_dashes(masked):
    return [Finding(m.start(), "em dash",
                    "consider a period, comma, colon, or parentheses")
            for m in re.finditer(r"\u2014|(?<=\w) -- (?=\w)", masked)]


CONTRAST = [
    re.compile(r"\b(?:it's|it is|this is|this isn't|that's|that is|they're|they are)"
               r"\s+not\s+(?:just\s+|only\s+|merely\s+|simply\s+)?[^.;!?\n]{1,80}?"
               r"[,;:\u2014\u2013]\s*(?:it's|it is|this is|that's|they're|but)\b",
               re.IGNORECASE),
    re.compile(r"\b(?:isn't|aren't|wasn't)\s+(?:just\s+|only\s+)?[^.;!?\n]{1,60}?"
               r"[,;:\u2014\u2013]\s*(?:it's|it is|they're|it was)\b", re.IGNORECASE),
    re.compile(r"\bnot\s+(?:just|only|merely|simply)\s+[^.;!?\n]{1,80}?,?\s+but\b",
               re.IGNORECASE),
]


def check_contrast(masked):
    findings, seen = [], set()
    for pattern in CONTRAST:
        for m in pattern.finditer(masked):
            if m.start() in seen:
                continue
            seen.add(m.start())
            findings.append(Finding(
                m.start(), "contrast framing",
                "\"not X, but Y\" framing; state what it is directly"))
    return findings


# ---------------------------------------------------------------- driver

def excerpt(text, offset, width=70):
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    line = text[line_start:line_end if line_end != -1 else len(text)]
    col = offset - line_start
    left = max(0, col - width // 2)
    snippet = line[left:left + width].strip()
    return ("..." if left > 0 else "") + snippet + ("..." if left + width < len(line) else "")


def run(name, text, args, entries):
    masked = mask(text)
    findings = []
    if "words" in args.checks:
        findings += check_words(masked, entries)
    if "acronyms" in args.checks:
        findings += check_acronyms(masked, COMMON_ACRONYMS | set(args.allow))
    if "sentences" in args.checks:
        findings += check_sentences(masked, args.max_words)
    if "dashes" in args.checks:
        findings += check_dashes(masked)
    if "contrast" in args.checks:
        findings += check_contrast(masked)
    findings.sort(key=lambda f: f.offset)

    line_starts = [0] + [m.end() for m in re.finditer("\n", text)]
    for f in findings:
        line = bisect.bisect_right(line_starts, f.offset)
        col = f.offset - line_starts[line - 1] + 1
        kind = f.kind if f.group is None else "word: " + f.group.name
        print("%s:%d:%d: [%s] %s" % (name, line, col, kind, f.message))
        print("    | " + excerpt(text, f.offset))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Flag discouraged words and AI-style patterns in a draft.")
    parser.add_argument("files", nargs="+", help="files to check, or - for stdin")
    parser.add_argument("--list", default=DEFAULT_LIST,
                        help="word list to use (default: references/word-list.txt)")
    parser.add_argument("--only", help="comma-separated checks to run: " + ",".join(CHECKS))
    parser.add_argument("--skip", help="comma-separated checks to skip")
    parser.add_argument("--max-words", type=int, default=35,
                        help="flag sentences longer than this (default 35)")
    parser.add_argument("--allow", default="",
                        help="comma-separated abbreviations the readers already know")
    args = parser.parse_args(argv)

    checks = set(CHECKS)
    if args.only:
        checks = {c.strip() for c in args.only.split(",")}
    if args.skip:
        checks -= {c.strip() for c in args.skip.split(",")}
    unknown = checks - set(CHECKS)
    if unknown:
        parser.error("unknown check(s): %s" % ", ".join(sorted(unknown)))
    args.checks = checks
    args.allow = [a.strip() for a in args.allow.split(",") if a.strip()]

    try:
        groups, entries = load_word_list(args.list)
    except OSError as err:
        print("cannot read word list: %s" % err, file=sys.stderr)
        return 2

    all_findings = []
    for name in args.files:
        try:
            if name == "-":
                text, label = sys.stdin.read(), "<stdin>"
            else:
                with open(name, encoding="utf-8") as handle:
                    text, label = handle.read(), name
        except (OSError, UnicodeDecodeError) as err:
            print("cannot read %s: %s" % (name, err), file=sys.stderr)
            return 2
        all_findings += run(label, text, args, entries)

    used_groups = []
    for f in all_findings:
        if f.group is not None and f.group not in used_groups:
            used_groups.append(f.group)
    if used_groups:
        print("\nWhy these words are discouraged:")
        for group in used_groups:
            print("  %s: %s" % (group.name, group.why))
            if group.instead:
                print("    Instead: %s" % group.instead)
    kinds = {}
    for f in all_findings:
        key = "word" if f.group is not None else f.kind
        kinds[key] = kinds.get(key, 0) + 1
    if all_findings:
        summary = ", ".join("%d %s" % (n, k) for k, n in sorted(kinds.items()))
        print("\n%d finding(s): %s." % (len(all_findings), summary))
        print("Reread each one. Keep a word if it is the precise, literal term; "
              "otherwise rewrite the sentence rather than swapping in a synonym.")
        return 1
    print("No findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
