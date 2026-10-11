#!/usr/bin/env python3
"""Local copyright guard for BQ learning content (reference implementation).

One rule everywhere (facts, cards, questions, feedback): no run of 8 or more
consecutive words may be shared with the handbook text. The only exceptions are short
quotations of out-of-copyright or statutory text (a poem title or opening, the oath),
which are flagged `quote`.

The guard needs the handbook text, which must NEVER be committed, so run it on your
own machine:

    python3 -I copyright_guard.py --handbook /path/to/handbook.txt --csv syllabus.csv

    python3 -I copyright_guard.py --handbook /path/to/handbook.txt --text cards.txt

How words are compared (the same as the project's syllabus checker):
  * lower case, the letters a-z, digits and apostrophes only (so punctuation, capitals
    and line breaks do not matter);
  * a run is 8 or more words in a row that also occur in a row in the handbook.

How `quote` is read:
  * --csv: a row whose `flags` column (semicolon separated) contains `quote` is allowed
    to share a run, but not a run longer than --max-quote-run words (default 12);
  * --text: a line that contains the marker [quote] is treated the same way.

Exit code 0 = clean, 1 = offenders found. Standard library only.
"""
import argparse
import csv
import re
import sys

RUN = 8


def words(text):
    return re.findall(r"[a-z0-9']+", text.lower().replace("’", "'"))


def load_handbook(path):
    hb = words(open(path, encoding="utf-8", errors="replace").read())
    return {tuple(hb[i:i + RUN]) for i in range(len(hb) - RUN + 1)}


def shared_runs(text, shingles, run=RUN):
    """Return a list of (length, text) for every run of `run` or more words shared with the handbook."""
    w = words(text)
    hits = [i for i in range(len(w) - run + 1) if tuple(w[i:i + run]) in shingles]
    runs, group = [], []
    for i in hits:
        if group and i == group[-1] + 1:
            group.append(i)
        else:
            if group:
                runs.append(group)
            group = [i]
    if group:
        runs.append(group)
    return [(g[-1] - g[0] + run, " ".join(w[g[0]:g[-1] + run])) for g in runs]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--handbook", required=True, help="plain-text handbook (kept outside the repo)")
    ap.add_argument("--csv", help="CSV file to check")
    ap.add_argument("--column", default="fact", help="CSV column holding the text (default: fact)")
    ap.add_argument("--id-column", default="id", help="CSV column holding the row id (default: id)")
    ap.add_argument("--flags-column", default="flags", help="CSV column holding the flags (default: flags)")
    ap.add_argument("--text", help="plain-text file to check, one item per line")
    ap.add_argument("--max-quote-run", type=int, default=12,
                    help="longest run a `quote` item may share with the handbook (default: 12 words)")
    args = ap.parse_args()
    if not args.csv and not args.text:
        ap.error("give --csv or --text")

    shingles = load_handbook(args.handbook)
    items = []  # (id, text, is_quote)
    if args.csv:
        with open(args.csv, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                flags = [x.strip() for x in row.get(args.flags_column, "").split(";")]
                items.append((row.get(args.id_column, "?"), row[args.column], "quote" in flags))
    if args.text:
        with open(args.text, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if line.strip():
                    items.append(("line %d" % n, line.replace("[quote]", " "), "[quote]" in line))

    bad = quotes = 0
    for item_id, text, is_quote in items:
        runs = shared_runs(text, shingles)
        if not runs:
            continue
        if is_quote:
            quotes += 1
            too_long = [r for r in runs if r[0] > args.max_quote_run]
            if too_long:
                bad += 1
                print("%s: quote shares %d words (limit %d): %s" % (item_id, too_long[0][0], args.max_quote_run, too_long[0][1]))
            continue
        bad += 1
        print("%s: shares %d words: %s" % (item_id, runs[0][0], " // ".join(r[1] for r in runs)))
    print("%d item(s) checked, %d offender(s), %d allowed quotation(s)" % (len(items), bad, quotes))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
