# Het uitrekenen aanvullende statements die volgen uit de ontologie 
# (bv. als A sdo:parent B dan moet ook B sdo:children A worden aangemaakt)
# heet "materialiseren". Dat lijkt makkelijk, maar is het niet. 
# De hele graaf moet in het geheugen, dus ik heb dit nog niet echt durven doen.

from rdflib import Graph
from owlrl import DeductiveClosure, OWLRL_Semantics

onto = Graph()
onto.parse("ontology.ttl", format="turtle")

data = Graph()
data.parse("data.ttl", format="turtle")

g = data + onto

DeductiveClosure(OWLRL_Semantics).expand(g)  # materializes in place

g.serialize("materialized.ttl", format="turtle")