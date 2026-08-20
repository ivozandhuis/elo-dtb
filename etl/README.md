# Data Extract and Transform

1. extract data from OAI-PMH endpoint of elo
    _NB change variable 'set' to name of the OAI-PMH setname to extract a particular dataset
    eg. dtb_trouwen, dtb_dopen, poorterboeken. Remember to add the set-name to the .gitignore file to prevent uploading the data three times to github ..._
2. transform data with a2a-to-pico
3. serialize into n-triples and compress