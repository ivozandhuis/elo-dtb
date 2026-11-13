#!/usr/bin/python3

from pathlib import Path
from rdflib import Graph
from saxonche import PySaxonProcessor


xsltproc = PySaxonProcessor(license=False).new_xslt30_processor()
executable = xsltproc.compile_stylesheet(stylesheet_file="../a2a-to-pico/xsl/a2a-to-pico.xsl")

sets = ["dtb_dopen", "dtb_trouwen", "dtb_begraven"]

# list of subdirectories in the data-tree selected to contain the files in the sample
dopen_sample   = ["e/e/b", "1/a/9", "0/d/2"]
trouwen_sample = ["5/3/c", "6/0/6", "3/8/f", "5/2/0"]
begraven_sample = ["2/f/5"]

# --
for set in sets:

    if set == "dtb_dopen": sample = dopen_sample
    if set == "dtb_trouwen": sample = trouwen_sample
    if set == "dtb_begraven": sample = begraven_sample

    print("start examples from " + set)
    for subdir in sample:

        print("start transformation from " + subdir)

        ext_path = Path("../etl/" + set + "/extracted/"  + subdir)
        for src_file in ext_path.glob("**/*.xml"):
            out_file = Path("../etl/" + set + "/transformed").joinpath(*src_file.parts[2:])
            out_file = out_file.with_suffix('.rdf')
            out_file.parent.mkdir(parents=True, exist_ok=True)
            executable.transform_to_file(source_file=str(src_file), output_file=str(out_file))

            print("written: " + str(out_file))

        print("end transformation from " + subdir)

        print("start sampling from " + subdir)

        ext_path = Path("../etl/" + set + "/transformed/" + subdir)
        for src_file in ext_path.glob("**/*.rdf"):
            out_file = Path(set) / src_file.name
            out_file = out_file.with_suffix('.ttl')
            out_file.parent.mkdir(parents=True, exist_ok=True)

            g = Graph()
            g.parse(src_file, format="xml")

            # run specific improvement queries and add the result to graph 'g'
            rq_dir = Path("../improvements/rq/" + set)
            for rq_file in rq_dir.glob("**/*construct*.rq"):
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

            # run general improvement queries and add the result to graph 'g'
            rq_dir = Path("../improvements/rq")
            for rq_file in rq_dir.glob("**/*construct*.rq"):
                query = rq_file.read_text(encoding="utf-8")
                query = "\n".join(
                    line for line in query.splitlines() if "ql:" not in line
                )

                result = g.query(query)
                constructed = list(result)
                for triple in constructed:
                    g.add(triple)

                print(f"  {rq_file.name}: added {len(constructed)} triples")

            # run all normalizations queries and add the result to graph 'g'
            rq_dir = Path("../normalizations/rq")
            for rq_file in rq_dir.glob("**/*construct*.rq"):
                query = rq_file.read_text(encoding="utf-8")
                query = "\n".join(
                    line for line in query.splitlines() if "ql:" not in line
                )

                result = g.query(query)
                constructed = list(result)
                for triple in constructed:
                    g.add(triple)

                print(f"  {rq_file.name}: added {len(constructed)} triples")

            g.serialize(destination=out_file)

            print("written: " + str(out_file))

        print("end sampling from " + subdir)

    print("end examples from " + set)

print("ready")
