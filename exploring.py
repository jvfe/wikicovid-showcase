# %%
from utils import wikidata_from_file, parse_query_results
from plotting import create_symptom_network
import pandas as pd
import networkx as nx


# %%
create_symptom_network()

# %%
qres = wikidata_from_file("queries/covidpathways.rq")

df = parse_query_results(qres, "virusLabel", "componentLabel", "pathwayLabel")

# %%
