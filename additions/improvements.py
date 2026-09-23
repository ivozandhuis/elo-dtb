#!/usr/bin/python3

from pathlib import Path
from rdflib import Graph, URIRef, BNode, Literal
import gzip
import itertools
import csv
import io
import requests

QLEVER_ENDPOINT = "http://localhost:7654"

amount = 0  # if 0, than all records are handled. For testing purpose

# set = "dtb_trouwen"
set = "dtb_dopen"

def to_term(value):
    """Convert a CSV cell from a CONSTRUCT query result into the right
    rdflib term type. URIs arrive already wrapped in '<' '>'."""
    value = value.strip()
    if value.startswith('<') and value.endswith('>'):
        return URIRef(value[1:-1])
    if value.startswith('_:'):
        return BNode(value[2:])
    return Literal(value)


ext_path = Path("rq/improvements/" + set)
print(ext_path)
for src_file in ext_path.glob("**/*.rq"):
    out_file = Path('improvements/' + set) / src_file.name
    out_file = out_file.with_suffix('.nt.gz')
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # SPARQL request *.rq on qlever endpoint http://localhost:7654
    print('query: ' + str(src_file))
    query = src_file.read_text(encoding='utf-8')

    response = requests.get(
        QLEVER_ENDPOINT,
        params={"query": query},
        headers={"Accept": "text/csv"},
    )
    response.raise_for_status()

    # read values of the csv and transform them to triples
    reader = csv.reader(io.StringIO(response.text))
    # A CONSTRUCT result has no header row (a SELECT does), so only skip a real one.
    # In RDF a subject is always an IRI or a blank node, so a first cell that is
    # neither is a header; anything else is already a triple and must be kept.
    first = next(reader, None)
    if first is not None and first and (first[0].startswith('<') or first[0].startswith('_:')):
        reader = itertools.chain([first], reader)

    g = Graph()
    for row in reader:
        if len(row) < 3:
            print ('Warning: skipping weird row' + str(row))
            continue
        s, p, o = row[0], row[1], row[2]
        g.add((to_term(s), to_term(p), to_term(o)))

    data = g.serialize(format='nt', encoding='utf-8')

    with gzip.open(out_file, 'wb') as f:
        f.write(data)

    print("written: " + str(out_file))

    amount = amount - 1
    if amount == 0: break 

print('done')
