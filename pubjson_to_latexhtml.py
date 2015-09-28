#!/usr/bin/env python
"""
Usage:
    pubjson_to_latexhtml.py <doc.json>

Read a json file of publications in the following form:

[
    {
        "title": "string"
        "named_authors": "string"
        "extra_authors": "yes/no string",
        "minerva_collaboration": "yes/no string",
        "how_published": "Journal ref",
        "year": integer
    }
]

and produce a latex `.tex` file and a `.html` file.
"""

import json
import sys
import re


def write_latex(pubs):

    with open("pubs.tex", "w") as outf:
        print("\\section{Publications}\n", file=outf)
        print("\\begin{enumerate}\n", file=outf)

        for pub in pubs:
            latex_print(pub, outf)

        print("\\end{enumerate}\n", file=outf)


def latex_print(pub, outf=None):

    print("\item", file=outf)

    if "title" in pub:
        print("{\\bf ``", pub["title"], "''}", sep="", file=outf)

    # the "author's block" should have only one newline at the end
    if "named_authors" in pub:
        print("\\\\{}", end="", file=outf)
        named_list = pub["named_authors"].split(",")
        for name in named_list:
            print(re.sub(". ", ".~", name), end=" ", file=outf)

    if "extra_authors" in pub:
        print("{\\it et al.}", end=" ", file=outf)

    if "collaboration" in pub:
        print("[", pub["collaboration"], "].", sep="", file=outf)
    else:
        print("", file=outf)

    # the "journal block" should have only one newline at the end
    if "how_published" in pub:
        print(pub["how_published"], end=" ", file=outf)

    if "year" in pub:
        print("(", pub["year"], ")", sep="", file=outf)

    # final newline for the entry
    print("", file=outf)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("This script requires a filename argument.\n")
        print(__doc__)
        sys.exit(2)

    if '-h' in sys.argv or '--help' in sys.argv:
        print(__doc__)
        sys.exit(1)

    json_file = sys.argv[1]

    with open(json_file) as data_file:
        pubs = json.load(data_file)

    write_latex(pubs)
