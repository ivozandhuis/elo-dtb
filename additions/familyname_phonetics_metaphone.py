#!/usr/bin/python3
"""
Generate phonetic normalization triples for family names.

For each family name found via the SPARQL query, this script computes:
  1. A normalized spelling form (Dutch 16th/17th-century spelling variants
     folded to a canonical form: y->ij, ph->f, th->t, c->k, x->ks, z->s,
     doubled consonants collapsed, etc.)
  2. Double Metaphone codes (primary + optional secondary), computed on
     the normalized form.
"""

import gzip
import csv
import io
import re
import requests
from pathlib import Path

from rdflib import Graph, URIRef, BNode, Literal
from metaphone import doublemetaphone

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
# Main pipeline
# ---------------------------------------------------------------------------
out_file = Path('normalizations/familyname_phonetics_metaphone.nt.gz')
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

p_double_primary = to_term("<https://example.org/iz/vocabulary/doubleMetaphone_Familyname>")
p_double_secondary = to_term("<https://example.org/iz/vocabulary/doubleMetaphonePronounced_Familyname>")

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

    # --- Double Metaphone, computed on normalized form ---
    primary, secondary = doublemetaphone(normalized)
    if primary:
        g.add((s, p_double_primary, Literal(primary)))
        if secondary:
            g.add((s, p_double_secondary, Literal(secondary)))
    else:
        print(f'Warning: could not compute double metaphone for "{familyname}" ({uri})')

    row_count += 1

data = g.serialize(format='nt', encoding='utf-8')

with gzip.open(out_file, 'wb') as f:
    f.write(data)

print(f"processed: {row_count} observations, skipped: {skipped_count}")
print("written: " + str(out_file))
print('done')