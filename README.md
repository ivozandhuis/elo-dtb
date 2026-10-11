# Data project PersonObservations from 17th/18th century Leiden (NL)
The Erfgoed Leiden en Omstreken (ELO) archival service provides indexes on the Doop- Trouw- en Begraafboeken (DTB) from the 17th/18th century. It contains a lot of interesting and useful data for our project to try and match the persons described in these sources. In this repo we collect code used to create data according to the [pico format](https://personsincontext.org/model).

## Sample
Check the sample/ directory for a first glance of what the resulting data looks like.

## Steps
### ETL
Code to obtain the data from the [ELO OAI-PMH endpoint in A2A](https://webservices.memorix.nl/a2a/20a181d4-c896-489f-9d16-20a3b7306b15?verb=Identify) and make Linked Data according to PiCo with [a2a-to-pico](https://github.com/ivozandhuis/a2a-to-pico).

### Qlever
Get a [qlever](https://en.wikipedia.org/wiki/QLever) endpoint running with this data. I originally pushed the resulting data in the data-directory to github, but that grew to big ...

### Additions
Improve and normalize the original data by creating extra statements mainly with SPARQL CONSTRUCT queries, using the qlever endpoint.

### Qlever
Read the improvements into the endpoint.

## PiCo-Wikidata
Vocabulary-level crosswalk between the PiCo model and Wikidata, done for the hack-a-lod (NDE) challenge. See [pico-wikidata/](pico-wikidata/).
