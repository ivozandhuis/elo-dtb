#!/usr/bin/python3

from pathlib import Path
from rdflib import Graph
import gzip

amount = 0 # if 0, than all records are handled. For testing purpose

ext_path = Path("transformed")
for src_file in ext_path.glob("**/*.rdf"):
    out_file = Path('serialized') / src_file.name
    out_file = out_file.with_suffix('.nt.gz')
    out_file.parent.mkdir(parents=True, exist_ok=True)

    g = Graph()
    g.parse(src_file, format="xml")
    data = g.serialize(format="nt").encode()

    with gzip.open(out_file, 'wb') as f:
        f.write(data)

    print("written: " + str(out_file))
    amount = amount - 1
    if amount == 0: break 

print('done')