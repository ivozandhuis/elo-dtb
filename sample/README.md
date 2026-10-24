# Test sample

This directory contains a sample of the data
- just to have a quick glance of what the data looks like
- as a small test set. A matching procedure should match these three records:
   - marriage record (1649) [fe0bf28c-e481-bdaa-48aa-fd2619b70c35](https://www.openarchieven.nl/elo:fe0bf28c-e481-bdaa-48aa-fd2619b70c35)
   - baptismal record (1651) [1c1c97e7-f9a7-40ea-c147-226c6817c9a1](https://www.openarchieven.nl/elo:1c1c97e7-f9a7-40ea-c147-226c6817c9a1)
   - baptismal record (1655) [7adcc50e-082b-04b4-8a91-17ea03827bee](https://www.openarchieven.nl/elo:7adcc50e-082b-04b4-8a91-17ea03827bee)
   - burial record (1707) [aa78fdb2-66d7-29da-dbcc-6db7661fa5f2](https://www.openarchieven.nl/elo:aa78fdb2-66d7-29da-dbcc-6db7661fa5f2)



Links to the files: 
- [marriage (1649)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/fe0bf28c-e481-bdaa-48aa-fd2619b70c35.ttl)
- [baptism (1651)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/1c1c97e7-f9a7-40ea-c147-226c6817c9a1.ttl)
- [baptism (1655)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/7adcc50e-082b-04b4-8a91-17ea03827bee.ttl)
- [burial (1707)](https://github.com/ivozandhuis/elo-dtb/blob/main/sample/aa78fdb2-66d7-29da-dbcc-6db7661fa5f2.ttl)

Notice that Lydia Thonis, 'moei' of the bride in the marriage (1649), and the witness Lydia Teunis at the baptism (1651) should be flagged as (potential) match.

Notice that the data about the burial of Frans Cloek is very thin. In the real world this is *not* the groom and father mentioned in earlier files, because the widow of Frans Pieters remarried in 1656. (Maybe we want to add [this marriage record](https://www.openarchieven.nl/elo:133850a5-15e2-e703-9e6e-3d538d60a606) to the testsample to test for false positives?)

# data
For now the data contains
- the original data as transformed by a2a-to-pico
- the improvements constructed with SPARQL constructs

Normalizations are not included (yet).

# sampling procedure
I picked the aformentioned example and therefore chose to sample every source-record from elo_dopen with a filename ending with "bee" and "9a1", every source-record from elo_trouwen with a filename ending with "c35", every-source record ending with "5f2". If the GUIDs are assigned as should be, the selection of the rest of the records is completely random. 

That way the chance that other matches should arise is very small, so I expect in the matching procedure only the above example to pop up.