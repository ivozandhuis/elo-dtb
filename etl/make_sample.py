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

        # run all sparql-CONSTRUCT queries from directory ../additions/rq/improvements/dtb_dopen
        # and add the result to graph 'g'
        rq_dir = Path("../additions/rq/improvements/dtb_dopen")
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

        # run all sparql-CONSTRUCT queries from directory ../additions/rq/improvements/dtb_trouwen
        # and add the result to graph 'g'
        rq_dir = Path("../additions/rq/improvements/dtb_trouwen")
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