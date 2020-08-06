# %%
from utils import wikidata_from_file
import pandas as pd

# %%
interv_query = wikidata_from_file(
    "queries/clinicaltrialsByIntervention.rq", ["interventionLabel", "trials"]
)
vacc = wikidata_from_file("queries/vaccines.rq", ["type", "typeLabel"])

# %%
# Group pathways by component and virus, visualize those
# Plot those that have very obvious quantitative properties, e.g. vaccines quantities, interventions,
# literature-supported interactions, etc.
# Try visualizing the symptom network as a dendrogram (improbable) - Maybe ete3?
# Plot table of coronaviruses proteins
