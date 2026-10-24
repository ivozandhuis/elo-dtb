#!/usr/bin/python3

from pathlib import Path
from rdflib import Graph


# set = "dtb_trouwen"
# set = "dtb_dopen"
set = "dtb_begraven"


dopen_sample   = ["e/e/b", "1/a/9"]
trouwen_sample = ["5/3/c"]
begraven_sample = ["2/f/5"]

if set == "dtb_dopen": sample = dopen_sample
if set == "dtb_trouwen": sample = trouwen_sample
if set == "dtb_begraven": sample = begraven_sample

# --
print("get examples from " + set)
for subdir in sample:

    ext_path = Path(set + "/transformed/" + subdir)
    for src_file in ext_path.glob("**/*.rdf"):
        out_file = Path(set + "/sampled") / src_file.name
        out_file = out_file.with_suffix('.ttl')
        out_file.parent.mkdir(parents=True, exist_ok=True)

        g = Graph()
        g.parse(src_file, format="xml")

        # run all sparql-CONSTRUCT queries from directory ../additions/rq/improvements/{set}
        # and add the result to graph 'g'
        rq_dir = Path("../additions/rq/improvements/" + set)
        for rq_file in sorted(rq_dir.glob("*.rq")):
            # read SPARQL CONSTRUCT query
            query = rq_file.read_text(encoding="utf-8")

            # remove all lines containing qlever specific properties with the prefix "ql:"
            query = "\n".join(
                line for line in query.splitlines() if "ql:" not in line
            )

            # execute query
            result = g.query(query)

            # add result
            constructed = list(result)
            for triple in constructed:
                g.add(triple)

            print(f"  {rq_file.name}: added {len(constructed)} triples")

        g.serialize(destination=out_file)

        print("written: " + str(out_file))

print('done')