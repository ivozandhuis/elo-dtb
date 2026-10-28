# Test sample

This directory contains a sample of the data
- just to have a quick glance of what the data looks like
- as a small test set. A matching procedure should match these records:
   1. [marriage record (1649)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/fe0bf28c-e481-bdaa-48aa-fd2619b70c35.ttl) op [openarchieven](https://www.openarchieven.nl/elo:fe0bf28c-e481-bdaa-48aa-fd2619b70c35)
   1. [baptismal record (1651)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/1c1c97e7-f9a7-40ea-c147-226c6817c9a1.ttl) op [openarchieven](https://www.openarchieven.nl/elo:1c1c97e7-f9a7-40ea-c147-226c6817c9a1)
   1. [baptismal record (1655)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/7adcc50e-082b-04b4-8a91-17ea03827bee.ttl) op [openarchieven](https://www.openarchieven.nl/elo:7adcc50e-082b-04b4-8a91-17ea03827bee)
   1. [marriage record (1656)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/133850a5-15e2-e703-9e6e-3d538d60a606.ttl) op [openarchieven](https://www.openarchieven.nl/elo:133850a5-15e2-e703-9e6e-3d538d60a606)
   1. [marriage record (1678)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/bd9518d5-1d0e-aa7a-3321-904aec5ecf83.ttl) op [openarchieven](https://www.openarchieven.nl/elo:bd9518d5-1d0e-aa7a-3321-904aec5ecf83)
   1. [marriage record (1687)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/2ef4776a-5184-a9ef-ec0b-03becba36025.ttl) op [openarchieven](https://www.openarchieven.nl/elo:2ef4776a-5184-a9ef-ec0b-03becba36025)
   1. [baptismal record (1693)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/d5eca0c3-248a-729c-9e9d-b9a62a9152d0.ttl) op [openarchieven](https://www.openarchieven.nl/elo:d5eca0c3-248a-729c-9e9d-b9a62a9152d0)
   1. [burial record (1707)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/aa78fdb2-66d7-29da-dbcc-6db7661fa5f2.ttl) op [openarchieven](https://www.openarchieven.nl/elo:aa78fdb2-66d7-29da-dbcc-6db7661fa5f2)

Notice that Lydia Thonis, 'moei' of the bride in the marriage (1649), the witness Lydia Teunis at the baptism (1651), the witness Lydia Tonis, moei of the bride, at the marriage (1656) should be flagged as (potential) match.

At the first marriage of Frans Fransz (1678) his 'schoonvader' is mentioned as witness. Should be his grandfather. (Remember that Frans Fransz' mother was called Jacomijntje Isaaks de Graaf). The Cecilia Gasthuys is typically a place for (old) people that can not take care of themselves.

In the second marriage of Frans Fransz (1687) the father (source states father, but should be: STEPfather. Apparently that is considered roughly the same) Casper Steven (second husband of the grooms mother) and Casper Steedink (spelling in the marriage of Frans Fransz) are the same.

Notice that the data about the burial (1707) of Frans Cloek, spinner, is very thin. It should be Frans Fransz instead of Frans Pietersz, because the widow of Frans Pietersz remarried in 1656.

# data
For now the data contains
- the original data as transformed by a2a-to-pico
- the improvements constructed with SPARQL constructs

Normalizations are not included (yet).

# sampling procedure
I picked the aformentioned example records and therefore chose to sample every source-record from elo_dopen with a filename ending with "bee" and "9a1", every source-record from elo_trouwen with a filename ending with "c35", every-source record ending with "5f2". If the GUIDs are assigned as should be, the selection of the rest of the records is completely random. 

That way the chance that other matches should arise is very small, so I expect in the matching procedure only the above example to pop up.