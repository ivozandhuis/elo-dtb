#!/usr/bin/python3
"""
Generate phonetic normalization triples for family names.

For each family name found via the SPARQL query, this script computes:
  1. A normalized spelling form (Dutch 16th/17th-century spelling variants
     folded to a canonical form: y->ij, ph->f, th->t, c->k, x->ks, z->s,
     doubled consonants collapsed, etc.)
"""

import gzip
import csv
import io
import re
import requests
from pathlib import Path

from rdflib import Graph, URIRef, BNode, Literal

QLEVER_ENDPOINT = "http://localhost:7654"

def to_term(value):
    """Convert a CSV cell from a CONSTRUCT query result into the right
    rdflib term type. URIs arrive already wrapped in '<' '>'."""
    value = value.strip()
    if value.startswith('<http') and value.endswith('>'):
        return URIRef(value[1:-1])
    if value.startswith('http://') or value.startswith('https://'):
        return URIRef(value)
    if value.startswith('_:'):
        return BNode(value[2:])
    return Literal(value)


# ---------------------------------------------------------------------------
# Normalization of historical Dutch spelling variants
# ---------------------------------------------------------------------------
# Order matters: multi-character patterns must be applied before single
# character ones, to avoid double-substitution.
NORMALIZATION_RULES = [
    (r'ch',  'g'),        
    (r'ph',  'f'),         
    (r'dt',  't'),         
    (r'gh',  'g'),
    (r'th',  't'),
    (r'ck',  'k'),
    (r'cq',  'k'),
    (r'qu',  'kw'),
    (r'ae',  'a'),
    (r'ue',  'u'),
    (r'ou',  'oe'),
    (r'ij',  'y'),
    (r'uy',  'ui'),
    (r'ey',  'ei'),
    (r'ay',  'ai'),
    (r'oy',  'oi'),
    (r'x',   'ks'),
    (r'z',   's'),
    (r'c(?=[eiy])', 's'),
    (r'c',   'k'),         # remaining c -> k
]


def normalize_name(name: str) -> str:
    """Fold common 16th/17th/18th-century Dutch spelling variants to a
    canonical form, to improve phonetic matching across archival
    spelling variation."""
    n = name.strip().lower()

    # Strip punctuation marks that sometimes appear in archival
    # transcriptions (quotes, apostrophes, backticks/acute accents,
    # sentence punctuation, hyphens, and parentheses) before any
    # phonetic processing.
    n = re.sub(r'["\'`´,.?!\-\(\)]', '', n)
 
    # Remove all whitespace (regular space, tab, non-breaking space, and
    # other Unicode space characters — \s is Unicode-aware in Python 3
    # str patterns and already covers all of these).
    n = re.sub(r'\s+', '', n)

    for pattern, replacement in NORMALIZATION_RULES:
        n = re.sub(pattern, replacement, n)

    # Word-final -n after a silent/schwa 'e' is not pronounced in Dutch
    # (e.g. "Bakkeren" -> "Bakkere", "Jansen" -> "Janse"). Drop it.
    n = re.sub(r'en$', 'e', n)

    # collapse doubled letters (aa -> a, ss -> s, etc.)
    n = re.sub(r'(.)\1+', r'\1', n)

    return n


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
out_file = Path('normalizations/familyname_phonetics_homemade.nt.gz')
out_file.parent.mkdir(parents=True, exist_ok=True)

# SPARQL request *.rq on qlever endpoint http://localhost:7654
src_file = Path("rq/normalizations/select_familynames.rq")
query = src_file.read_text(encoding='utf-8')

response = requests.get(
    QLEVER_ENDPOINT,
    params={"query": query},
    headers={"Accept": "text/csv"},
)
response.raise_for_status()

# read values of the csv and transform them to triples
reader = csv.reader(io.StringIO(response.text))
next(reader, None)  # skip header row (?s,?p,?o)

p_normalized     = to_term("<https://example.org/iz/vocabulary/normalized_Familyname>")

g = Graph()
row_count = 0
skipped_count = 0

for row in reader:
    if len(row) != 2:
        print(f'Warning: skipping weird row ({row})')
        skipped_count += 1
        continue

    uri, familyname = row[0], row[1]

    if not familyname.strip():
        print(f'Warning: empty familyname, skipping ({uri})')
        skipped_count += 1
        continue

    s = to_term(uri)
    normalized = normalize_name(familyname)

    g.add((s, p_normalized, Literal(normalized)))

    row_count += 1

data = g.serialize(format='nt', encoding='utf-8')

with gzip.open(out_file, 'wb') as f:
    f.write(data)

print(f"processed: {row_count} observations, skipped: {skipped_count}")
print("written: " + str(out_file))
print('done')