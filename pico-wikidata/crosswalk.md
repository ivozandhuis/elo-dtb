# PiCo &harr; Wikidata term crosswalk

Rough, term-by-term pass over every class and property defined in [pico.ttl](https://github.com/CBG-Centrum-voor-familiegeschiedenis/PiCo/blob/main/pico.ttl) (the PiCo RDF model), matched against the closest Wikidata property/item. Every Wikidata P/Q-id below was looked up against the live Wikidata API on 2026-10-11, not recalled from memory — "no equivalent" means a search turned up nothing plausible, not that I didn't look.

This is a **vocabulary-level** crosswalk (which Wikidata term, if any, corresponds to a given PiCo term), not an **instance-level** one — it says nothing about whether any specific Leiden person in your data actually has a Wikidata item.

## How to read "fit"

Three broad outcomes recur throughout the table:

- **Good** — same concept, same granularity; mainly a syntax/range difference (string vs. Wikidata item, etc.).
- **Partial** — the concept exists on Wikidata but is modeled differently (folded into a qualifier, split by gender, merged with a neighbouring concept, generic mechanism only).
- **None** — no plausible counterpart; usually because the concept belongs to PiCo's *source-observation* layer (what a record literally says, by whom, how reliably), which Wikidata's single-global-fact model has no place for.

That third category is the real headline: PiCo's `PersonObservation` vs. `PersonReconstruction` split — keeping "what this specific record says" distinct from "what we believe happened" — has **no Wikidata counterpart at all**. Wikidata stores one merged fact per property (with per-*statement* references), never a competing set of source-attested values. Several rows below (`hasAge`, `deceased`, `hadPrimarySource`, `wasDerivedFrom`, the whole `prov:Activity`/`prov:Agent` pair) are symptoms of that one structural gap, not independent gaps of their own.

---

## Classes

| PiCo term | Wikidata term | Fit |
|---|---|---|
| `picom:Person` | [Q5](https://www.wikidata.org/wiki/Q5) (human) | Partial — `picom:Person` is an abstract container, not meant to be instantiated directly; Wikidata has no such abstraction, every item is already a resolved individual. |
| `picom:PersonObservation` | *none* | None — see "how to read fit" above. Wikidata has no resource representing "person X as recorded on source Y"; only per-statement references exist, and those don't carry their own name/age/occupation-as-written. |
| `picom:PersonReconstruction` | [Q5](https://www.wikidata.org/wiki/Q5) (human) | Partial — a Wikidata person item already *is* the single de-duplicated identity, so it structurally plays this role, but it never declares itself "a reconstruction" or lists which observations it was derived from. |
| `prov:Activity` | *none* | None — Wikidata's own edit history plays a loosely similar role but isn't exposed as queryable item data. [P887](https://www.wikidata.org/wiki/Property:P887) "based on heuristic" flags an automated inference on one statement, which is a different thing. |
| `prov:Agent` | *none* | None — same gap as `prov:Activity`; a reference's "stated in" target ([P248](https://www.wikidata.org/wiki/Property:P248)) is the closest analogue and isn't really comparable. |
| `sdo:ArchiveComponent` (Source) | *none* | None — individual archival records (a specific birth/marriage act) are essentially never modeled as Wikidata items; sourcing is done per-statement ("stated in" / reference URL), not as a describable resource with its own name/date/holding archive. |
| `sdo:ImageObject` (Scan) | *none* (cf. [P18](https://www.wikidata.org/wiki/Property:P18) image) | Partial — Wikidata links media straight to a Commons file via P18; there's no reified "scan" resource carrying its own url/thumbnailUrl/position/embedUrl metadata the way PiCo models it. |
| `pnv:PersonName` | *none* | None — Wikidata has no bundled "one name occurrence" resource; it uses the item's own label/aliases for the literal name, plus flat properties pointing at separate name-concept items (see below), not grouped together. |
| `picom:LifeEvent` | *none* (cf. [P793](https://www.wikidata.org/wiki/Property:P793) significant event) | Partial — vital events are inlined as direct dated properties on the person (birth, death) or as qualifiers on `spouse` (marriage); there's no generic event-node for things like baptism or migration the way `picom:LifeEvent` provides. P793 is for independently notable events, not routine vital events. |

## Core person attributes

| PiCo term | Wikidata term | Fit |
|---|---|---|
| `sdo:name` | *none* (item's own label) | Partial — the role is played by the item's label/alias, not a settable property; no counterpart at all for naming a Source. |
| `sdo:givenName` / `pnv:givenName` | [P735](https://www.wikidata.org/wiki/Property:P735) given name | Good, with a range difference: P735 points to a Wikidata item representing the name itself, not a plain string. PiCo also duplicates this concept across `sdo:` and `pnv:`; Wikidata has it once. |
| `sdo:familyName` | [P734](https://www.wikidata.org/wiki/Property:P734) family name | Good, same range caveat as given name. |
| `pnv:baseSurname` | *none* | None — Wikidata doesn't separate a "sortable" surname from the full family name. |
| `pnv:patronym` | [P5056](https://www.wikidata.org/wiki/Property:P5056) patronym or matronym | Good — clean, direct match; one of the best-aligned terms in this whole list. |
| `pnv:surnamePrefix` | *none* | None — Dutch "tussenvoegsel" has no separate Wikidata statement; it's just part of the family-name item. |
| `pnv:initials` | *none* | None found. |
| `pnv:literalName` | *none* (item's own label) | Partial — same as `sdo:name`: played by the label, not a value-property, so not really a crosswalkable term. |
| `sdo:birthDate` | [P569](https://www.wikidata.org/wiki/Property:P569) date of birth | Good, with a caveat: PiCo allows a verbatim-string value alongside the ISO date; Wikidata requires one normalized date (with precision/calendar qualifiers), no "as written on the source" slot. |
| `sdo:deathDate` | [P570](https://www.wikidata.org/wiki/Property:P570) date of death | Good, same string-vs-normalized caveat. |
| `sdo:birthPlace` | [P19](https://www.wikidata.org/wiki/Property:P19) place of birth | Good conceptually, but P19 requires the place to already be a Wikidata item — exactly the reconciliation step PiCo's own scope note anticipates ("preferably a link to geonames or wikidata") but doesn't require. |
| `sdo:deathPlace` | [P20](https://www.wikidata.org/wiki/Property:P20) place of death | Good, same reconciliation caveat. |
| `sdo:gender` | [P21](https://www.wikidata.org/wiki/Property:P21) sex or gender | Partial — conceptually aligned, but PiCo's own SHACL shape constrains this to exactly `sdo:Male`/`sdo:Female`, while Wikidata's P21 range is deliberately broader (intersex, non-binary, transgender identities, etc.) — a values-model mismatch, not just naming. |
| `picom:hasAge` | *none* | None — this is specifically "the age as stated in this source," distinct from any computed age. Wikidata only ever stores P569/P570 as single global facts and has no slot for a source-attested age that might disagree with them. |
| `picom:deceased` | *none* | None — Wikidata infers "presumed alive" the same way PiCo's scope note warns against: by the mere absence of a death date. There's no boolean flag for "known dead, date unknown" vs. "no evidence found either way." |
| `sdo:hasOccupation` | [P106](https://www.wikidata.org/wiki/Property:P106) occupation | Good, range difference: P106 points to an occupation-concept item, PiCo allows free text or URI. |
| `picom:hasReligion` | [P140](https://www.wikidata.org/wiki/Property:P140) religion or worldview | Good match. |
| `sdo:address` | [P6375](https://www.wikidata.org/wiki/Property:P6375) street address (string) / [P669](https://www.wikidata.org/wiki/Property:P669) located on street | Partial — reasonable for a modern postal address; historical "Wijk B no. 35"-style numbering (no named street) doesn't map cleanly onto either. |
| `sdo:contentLocation` | *none* (cf. [P180](https://www.wikidata.org/wiki/Property:P180) depicts) | Weak — P180 covers "this image depicts place X," not the general "geographic coverage of this record" PiCo's scope note describes. |
| `sdo:dateCreated` | [P571](https://www.wikidata.org/wiki/Property:P571) inception / [P577](https://www.wikidata.org/wiki/Property:P577) publication date | Good, pick based on whether the Source is treated as a created artifact or a published document. |
| `sdo:position` | [P1545](https://www.wikidata.org/wiki/Property:P1545) series ordinal | Good generic match for ordering multiple scans. |
| `sdo:url` / `sdo:contentUrl` / `sdo:thumbnailUrl` / `sdo:embedUrl` | *none* (cf. [P973](https://www.wikidata.org/wiki/Property:P973) described at URL) | None/weak — Wikidata strongly prefers hosting media on Commons via P18 (which carries its own thumbnail/rendition logic) over externally-hosted URLs; P973 is generic and carries none of PiCo's scan-specific semantics (position, embed viewer, thumbnail vs. full image). |
| `sdo:holdingArchive` | [P485](https://www.wikidata.org/wiki/Property:P485) archives at | Partial — same concept, but P485 is conventionally used on the *person/creator's* item ("this person's papers are held at X"), not on the individual record the way PiCo attaches it. |
| `sdo:additionalType` (source type) | *none* (cf. [P31](https://www.wikidata.org/wiki/Property:P31) instance of) | None — Wikidata types things via the open `P31` item graph; PiCo's closed `picot_sourcetypes` thesaurus (via `qb:CodedProperty`) has no structural counterpart. |
| `picom:eventDate` / `picom:eventPlace` / `picom:eventType` | *none* generically (cf. [P580](https://www.wikidata.org/wiki/Property:P580)/[P582](https://www.wikidata.org/wiki/Property:P582) for marriage) | Partial — see `picom:LifeEvent` above; only the marriage case has a real Wikidata counterpart (qualifiers on `spouse`), nothing generic for baptism, migration, etc. |

## Direct kinship

| PiCo term | Wikidata term | Fit |
|---|---|---|
| `sdo:parent` | [P22](https://www.wikidata.org/wiki/Property:P22) father / [P25](https://www.wikidata.org/wiki/Property:P25) mother | Partial — structural mismatch: PiCo offers one gender-neutral property (matching its own stated design choice to keep kinship separate from gender inference), Wikidata has no generic "parent" property at all and requires picking the gendered one. |
| `sdo:children` | [P40](https://www.wikidata.org/wiki/Property:P40) child | Good, with a note: Wikidata explicitly excludes stepchildren from P40 (routes them to the generic `relative` mechanism instead), where PiCo gives stepchildren their own dedicated property (see below). |
| `sdo:sibling` | [P3373](https://www.wikidata.org/wiki/Property:P3373) sibling | Good — and P3373 explicitly includes half-siblings in the one property, where PiCo splits plain siblings from `hasHalf-sibling` as two separate properties. |
| `sdo:spouse` | [P26](https://www.wikidata.org/wiki/Property:P26) spouse | **Best match in this list.** P26 already supports `start time` ([P580](https://www.wikidata.org/wiki/Property:P580)) / `end time` ([P582](https://www.wikidata.org/wiki/Property:P582)) qualifiers, which is exactly PiCo's own `rdf:value` + `sdo:startDate`/`endDate` pattern for a person married more than once. |
| `picom:hasPreviousPartner` | *none* | None — redundant with `spouse` qualified by an end date; Wikidata would just add another (now-ended) P26 statement rather than a separate property. |
| `picom:isWidOf` | *none* | None — same as above; no explicit "widow/widower of" semantic on Wikidata, it's implicit in a P26 statement with an end date. |

## Step / foster / god / extended kinship

| PiCo term | Wikidata term | Fit |
|---|---|---|
| `picom:hasStepparent` | [P3448](https://www.wikidata.org/wiki/Property:P3448) stepparent | Good, direct match. |
| `picom:hasStepchild` | *none* (inverse of P3448 only) | Partial — Wikidata has no separate "stepchild" property; you'd query the inverse of P3448 rather than assert it. PiCo gives both directions their own dedicated, explicitly inverse-linked property. |
| `picom:hasGodparent` | [P1290](https://www.wikidata.org/wiki/Property:P1290) godparent | Good, direct match. |
| `picom:hasGodchild` | *none* (inverse of P1290 only) | Partial — same asymmetry as stepchild/stepparent. |
| `picom:hasHalf-sibling` | *none* (folded into [P3373](https://www.wikidata.org/wiki/Property:P3373)) | None as a separate term — Wikidata's one `sibling` property already covers this. |
| `picom:hasFosterChild` / `hasFosterParent` | *none* confirmed (cf. [P1038](https://www.wikidata.org/wiki/Property:P1038)+[P1039](https://www.wikidata.org/wiki/Property:P1039)) | Weak — only reachable, if at all, through the generic "relative" + "kinship to subject" qualifier mechanism, and I could not confirm a matching kinship-type item exists for foster relations. |
| `picom:hasGrandparent` / `hasGrandchild` / `hasGreat-grandparent` / `hasGreat-grandchild` / `hasAncestor` / `hasDescendant` | *none* stored (derived via chained P22/P25/P40) | None as asserted facts — Wikidata convention is to compute multi-generation relations by chaining the direct properties in a query, not to store them redundantly. PiCo instead materializes them as first-class properties specifically to avoid multi-hop joins — a real architectural difference in how "derivable but convenient" facts are treated. |
| `picom:hasCousin` / `hasUncle_Aunt` / `hasNephew_Niece` (+ their `-in-law` variants) | *none* dedicated (cf. [P1038](https://www.wikidata.org/wiki/Property:P1038) relative, qualified with [P1039](https://www.wikidata.org/wiki/Property:P1039) kinship to subject) | Weak/indirect — only reachable via the generic relative mechanism, and only if a matching kinship-type item exists for each (confirmed for niece and daughter-in-law as worked examples on P1039's own documentation; not individually checked for the rest). |
| `picom:hasParent-in-law` / `hasChild-in-law` / `hasSibling-in-law` / `hasGrandparent-in-law` / `hasGrandchild-in-law` / `hasStepparent-in-law` / `hasStepchild-in-law` | *none* dedicated (cf. [P1038](https://www.wikidata.org/wiki/Property:P1038)+[P1039](https://www.wikidata.org/wiki/Property:P1039)) | Weak/indirect — same generic mechanism; P1039's own documentation singles out in-law relationships as its intended use case, so this path is more plausible than the cousin/uncle/nephew row above, but still unconfirmed term-by-term. |
| `picom:hasStepsibling` | *none* confirmed | Weak — same generic-mechanism-only story; couldn't confirm a matching kinship-type item exists. |
| `picom:hasLegitimizedChild` / `isLegitimizedChildOf` | *none* | None — specific Dutch/civil-law legal concept ("wettiging") with no apparent Wikidata analogue, even through the generic relative mechanism. |

## Provenance & source linking

| PiCo term | Wikidata term | Fit |
|---|---|---|
| `prov:hadPrimarySource` | *none* (cf. [P248](https://www.wikidata.org/wiki/Property:P248) stated in) | Partial — Wikidata's nearest idea attaches a reference to one *statement*, not to a whole resource the way `hadPrimarySource` links an entire PersonObservation to its Source. |
| `prov:wasDerivedFrom` | *none* | None — Wikidata doesn't track "which prior source-records fed into this item" as item-level data. |
| `prov:wasGeneratedBy` | *none* | None — follows from `prov:Activity` having no counterpart. |
| `prov:wasRevisionOf` | *none* (cf. the wiki's own edit history) | None in RDF-queryable form. |
| `prov:startedAtTime` / `prov:endedAtTime` | *none* for this purpose (cf. [P580](https://www.wikidata.org/wiki/Property:P580)/[P582](https://www.wikidata.org/wiki/Property:P582)) | None — P580/P582 exist on Wikidata but for a different purpose (a *statement's* validity period, e.g. a job held from–to), not for timing the activity that produced a reconstruction. Worth flagging so the similarly-named concepts aren't conflated. |
| `prov:wasAssociatedWith` | *none* | None — follows from `prov:Agent` having no counterpart. |
| `sdo:associatedMedia` | *none* (cf. [P18](https://www.wikidata.org/wiki/Property:P18) image) | Weak — P18 points straight to a Commons file; no reified "this Source has an associated Scan resource" step. |
| `sdo:embedUrl` | *none* | None found. |
| `sdo:additionalName` | *none* (cf. [P1477](https://www.wikidata.org/wiki/Property:P1477) birth name, for the common genealogical case) | Weak — P1477 covers "name at birth if different," the single most common reason PiCo would use `additionalName`, but `sdo:additionalName` points to a whole `pnv:PersonName` resource, not a bare string. |

## Coded/thesaurus properties

| PiCo term | Wikidata term | Fit |
|---|---|---|
| `picom:hasRole` | *none* (cf. [P3831](https://www.wikidata.org/wiki/Property:P3831) object of statement has role) | None structurally — P3831 is a qualifier on an arbitrary statement, not a dedicated closed thesaurus of document-interaction roles (declarant, witness, bride/groom...) the way `picot_roles` works. |
| `picom:eventType` | *none* closed (cf. [P793](https://www.wikidata.org/wiki/Property:P793) significant event) | None structurally — P793's range is the open item graph, not a closed, versioned thesaurus like `picot_eventtypes`. |

---

## Takeaways

1. **The strongest matches are all in the "classic" civil-registration core**: birth/death date & place, gender, occupation, religion, and — especially — spouse (where Wikidata's qualifier pattern for `P26` is a near-exact structural match for PiCo's own qualified `sdo:spouse`). If you only crosswalk five terms, these are the five.
2. **Wikidata splits by gender where PiCo doesn't** (`parent` &rarr; father/mother), and **merges where PiCo splits** (`sibling` already covers half-siblings; PiCo keeps them separate). Neither direction is a bug, just a different modeling choice to account for in any CONSTRUCT query.
3. **The extended/in-law/step/foster/god kinship properties** — more than a third of all PiCo terms — mostly fall back to Wikidata's one generic `relative` (P1038) + `kinship to subject` (P1039) qualifier, and even that's only confirmed for a handful of specific relations. This whole branch of PiCo's vocabulary is, realistically, not crosswalkable term-by-term.
4. **Everything in the Classes section tied to `PersonObservation`, `Activity`, and `Agent` has no Wikidata counterpart at all** — this is the Observation/Reconstruction split surfacing again, and it's structural, not a gap that a better search query would close.
