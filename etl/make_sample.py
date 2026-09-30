#!/usr/bin/python3

from pathlib import Path
from rdflib import Graph

dopen_sample   = ["e/e/b", "1/a/9"]
trouwen_sample = ["5/3/c"]

# --
print("get examples from dopen")
for subdir in dopen_sample:

    ext_path = Path("dtb_dopen/transformed/" + subdir)
    for src_file in ext_path.glob("**/*.rdf"):
        out_file = Path("dtb_dopen/sampled") / src_file.name
        out_file = out_file.with_suffix('.ttl')
        out_file.parent.mkdir(parents=True, exist_ok=True)

        g = Graph()
        g.parse(src_file, format="xml")
        g.serialize(destination=out_file)

        print("written: " + str(out_file))

# --
print("get examples from trouwen")
for subdir in trouwen_sample:

    ext_path = Path("dtb_trouwen/transformed/" + subdir)
    for src_file in ext_path.glob("**/*.rdf"):
        out_file = Path("dtb_trouwen/sampled") / src_file.name
        out_file = out_file.with_suffix('.ttl')
        out_file.parent.mkdir(parents=True, exist_ok=True)

        g = Graph()
        g.parse(src_file, format="xml")
        g.serialize(destination=out_file)

        print("written: " + str(out_file))


print('done')