# Instance-level check: sample persons against Wikidata

Follow-up to the [vocabulary crosswalk](crosswalk.md): instead of comparing *terms*, this checks whether any actual person in [sample/](../sample/) — the 72-record PiCo sample of 17th-century Leiden DTB (baptism/marriage/burial) data — has a corresponding Wikidata item.

## What we did

1. Extracted every distinct `sdo:name` value from the person observations in `sample/*.ttl` — **979 distinct names**.
2. First pass: matched each name exactly against Wikidata human (`wdt:P31 wd:Q5`) labels, with no further restriction.
3. Second pass: same label match, but restricted to humans with a recorded place of birth or death of Leiden (`wd:Q43631`) and a birth or death year between 1600 and 1900.
4. Ran both passes via the Wikidata Query Service (`query.wikidata.org/sparql`), batched into chunks of ~20–35 names per query (URLs over ~1800 characters were rejected), covering all 979 names in both passes.

## Results

**First pass (no restriction): noisy, no real matches.** A handful of names returned Wikidata hits, but all were false positives of two kinds:
- **Bare given names** ("Barbara", "Cornelia", "Jacob", "Hendrick", "Françoise") matching dozens of unrelated people worldwide who happen to share that common name — a French singer, Roman empresses, 20th-century athletes.
- **Coincidental full-name collisions** — a distinctive two-part name matching a real but unrelated person: "Charlotte Segers" (a living academic), "Hendrik Visser" (a WWII "Righteous Among the Nations"), "Gerrit Schoonhoven" (a South African actor, 1958–2020), "Cornelis de Groot" (a different Dutch captain of the guard). One case, "François Schas" (Q110557588, "c.1698–1761"), looked period-plausible, but turned out to be a bulk import from the *Genealogics* database rather than independent Wikidata notability — and it carries no place of birth/death at all.

**Second pass (born or died in Leiden, 1600–1900): zero matches.** Across all 979 names, not one Wikidata item satisfied the restriction. Every false positive from the first pass dropped out — including "François Schas", confirming it was never actually tied to Leiden in the first place; the date plausibility was coincidental.

## Conclusion

This is about as clean a negative result as this kind of check can produce. It isn't that the matches are weak or ambiguous — once a real tie to Leiden and a plausible date are required, there are *no* candidates left at all. This confirms, on the actual sample data (not just the family-treez side investigation), that individual-level linking between this dataset and Wikidata isn't viable: the people in these records are ordinary parish-register entries with no public notability, and Wikidata simply doesn't contain them. Any future linking work on this project should stay at the vocabulary/term level (see [crosswalk.md](crosswalk.md)) or target place names and other shared reference entities, not individual persons.
