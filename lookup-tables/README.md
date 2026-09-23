# Look up tables

Soms is het handig om data te normalizeren op basis van een lookup table. 

## Bloothooft's voornamen
Deze lijst standaardiseert de spelling van voornamen.
Zie: https://linkeddata.cultureelerfgoed.nl/rce/dutch-given-names

PS de URIs in deze dataset resolven niet, maar dat mag de pret niet drukken.

## Mijn eigen lijst van adressen van Leiden
In de data is soms bij data entry aangegeven dat een straat/steeg etc. in Leiden was, door er de plaatsnaam 'Leiden' voor of achter te typen. Deze konden worden uitgefilterd met deze query:

```
PREFIX sdo: <https://schema.org/>
PREFIX picom: <https://personsincontext.org/model#>

SELECT DISTINCT ?street 
WHERE {
    ?po a picom:PersonObservation ;
        sdo:address ?residence .
    FILTER(CONTAINS(?residence, ", Leiden") || CONTAINS(?residence, "Leiden, "))
    BIND(
      IF(CONTAINS(?residence, ", Leiden"),
         REPLACE(STR(?residence), ", Leiden", ""),
         REPLACE(STR(?residence), "Leiden, ", ""))
      AS ?street
    )
}
```

Dit is de basis voor een lookup-table voor Leidse adressen. In de CSV file is een kolom toegevoegd met een gestandaardiseerde spelling, zoveel mogelijk naar de spelwijze zoals deze nu gangbaar is. Work-in-progress.

## Ricks lijst met Liedse adressen
In de toponiemenlijst van Rick zitten ook straatnamen. Hier heb ik nog niet naar gekeken.