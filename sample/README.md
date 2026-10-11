# Test sample

This directory contains a sample of the data
- just to have a quick glance of what the data looks like
- as a small test set. A matching procedure should match these three records:
   - marriage record (1649) [fe0bf28c-e481-bdaa-48aa-fd2619b70c35](https://www.openarchieven.nl/elo:fe0bf28c-e481-bdaa-48aa-fd2619b70c35)
   - baptismal record (1651) [1c1c97e7-f9a7-40ea-c147-226c6817c9a1](https://www.openarchieven.nl/elo:1c1c97e7-f9a7-40ea-c147-226c6817c9a1)
   - baptismal record (1655) [7adcc50e-082b-04b4-8a91-17ea03827bee](https://www.openarchieven.nl/elo:7adcc50e-082b-04b4-8a91-17ea03827bee)

Links to the files: 
- [marriage (1649)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/fe0bf28c-e481-bdaa-48aa-fd2619b70c35.ttl)
- [baptism (1651)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/1c1c97e7-f9a7-40ea-c147-226c6817c9a1.ttl)
- [baptism (1655)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/7adcc50e-082b-04b4-8a91-17ea03827bee.ttl)

Notice that Lydia Thonis, 'moei' of the bride in the marriage (1649), and the witness Lydia Teunis at the baptism (1651) should be flagged as (potential) match.

# data
For now the data contains
- the original data as transformed by a2a-to-pico
- the improvements constructed with SPARQL constructs

Normalizations are not included (yet).

# sampling procedure
I picked the aformentioned example and therefore chose to sample every source-record from elo_dopen with a filename ending with "bee" and "9a1" and every source-record from elo_trouwen with a filename ending with "c35". If the GUIDs are assigned as should be, the selection of the rest of the records is completely random. 

That way the chance that other matches should arise is very small, so I expect in the matching procedure only the above example to pop up.