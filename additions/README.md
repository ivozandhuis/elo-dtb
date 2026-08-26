# Create additions

This code expects an available qlever endpoint with data from the etl. See directory ```qlever```.

## Improvements
SPARQL queries that make data explicit that is captured on unlogical (incorrect?) places in the original data
todo: places.

## Normalizations

### Standardized familynames
Python script ```familynames_phonetics.py``` calculates various phonetic standardizations. Results in extra statements that can be added to the endpoint.

### Standardized givennames
Download Bloothoofts givennames standardizations from (https://linkeddata.cultureelerfgoed.nl/rce/CLARIAH-Given-Names/)[https://linkeddata.cultureelerfgoed.nl/rce/CLARIAH-Given-Names/] and reindex the data in qlever. This enables SPARQL queries to find standardized givennames. Todo: create CONSTRUCT queries to link standardized names to the personobservations.

### Standardized patronymix
Todo. Maybe compare sdo:Male names from Bloothooft + ("s" or "z" or "sz" or "sdr" or ...)?
Remember Isaaks => Isaax.

### Standardized placenames
Todo. Remember the A2A field for place contains lots of streetnames ('Breestraat') and placenames ('Haarlem') in the same field ... 

### Standardized professions
Todo. HISCO of course.

## Inference
Todo: statements logically derived eg. 
```a sdo:parent/sdo:children b AND a!=b <=> a sdo:sibling b``` 

Needs data from the improvements that add the relations to the data that is not explicit in the original data.


