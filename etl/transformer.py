#!/usr/bin/python3
# Transforms files in /extracted/ and stores them in /transformed/

from pathlib import Path
from saxonche import PySaxonProcessor

# set = "dtb_trouwen"
set = "dtb_dopen"
amount = 0 # if 0, than all records are handled

xsltproc = PySaxonProcessor(license=False).new_xslt30_processor()
executable = xsltproc.compile_stylesheet(stylesheet_file="../a2a-to-pico/xsl/a2a-to-pico.xsl")

ext_path = Path(set + "/extracted")
for src_file in ext_path.glob("**/*.xml"):
    out_file = Path(set + "/transformed").joinpath(*src_file.parts[2:])
    out_file = out_file.with_suffix('.rdf')
    out_file.parent.mkdir(parents=True, exist_ok=True)
    executable.transform_to_file(source_file=str(src_file), output_file=str(out_file))

    print("written: " + str(out_file))
    amount = amount - 1
    if amount == 0: break 

print('done')