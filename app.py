from plotting import *
import streamlit as st
import pandas as pd

st.write(
    """
# Exploring Wikidata's scientific knowledge about COVID-19

This is an exploration of the sort of scientific knowledge we can get and analyse from the largest free structured knowledge base:
[Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)! - It's also a learning experience in data analysis, SPARQL and streamlit.

First off, some things:

* The queries I used to get the data are a courtesy of [Egon Willighagen and contributors](https://github.com/egonw/SARS-CoV-2-Queries), 
thanks a lot to them!

* I tried to focus on information which you can easily acquire from Wikidata that may not be easily acquired elsewhere, so things such as case counts 
and distribution maps are out of the question, although **you can** get that data from wikidata too! Isn't that great?

* All the queries I used can be found in the subdirectory [queries/](https://github.com/jvfe/wikicovid-showcase/tree/master/queries) 
of this project's github repo.

## What genes/proteins do the coronaviruses interact with?

This data comes from annotated articles that attest these organisms interact with these molecules. Big players here, such as 
[ACE2 and TMPRSS2](https://en.wikipedia.org/wiki/Angiotensin-converting_enzyme_2#Coronavirus_entry_point), most people know, 
but some were a *surprise to me* and may be a surprise to you too.

"""
)

st.altair_chart(plot_literature_interactions(), use_container_width=True)

st.write(
    """
## Which drugs are being suggested as possible treatments for COVID-19?

This data comes from annotated clinical trials, they list the intervention being tested, and, as such, these can be quantified, which is what you see below.
HCQ leads the effort, at least quantitatively, [but do some research before saying it works](https://en.wikipedia.org/wiki/Hydroxychloroquine#COVID-19).

"""
)

min_ct = st.slider(
    label="Minimum number of clinical trials", min_value=1, max_value=20, value=10
)

st.altair_chart(plot_interventions(min_ct), use_container_width=True)

st.write(
    """
## Which biological pathways are coronaviruses in?

The pathways are from [Wikipathways](https://www.wikipathways.org/index.php/WikiPathways), 
another great open knowledge base, which happens to also be indexed inside of wikidata (Wiki inside of wiki!).
Hover over the points to see the number of molecules from this organism that are present in that pathway. 
Try clicking the points to see each pathway in wikipathways.
"""
)

st.altair_chart(plot_pathway_by_virus(), use_container_width=True)

st.write(
    """
## What types of vaccines candidates are being suggested for COVID-19?

As is the way data is structured in Wikidata, most of it is hierarchical, so things are subclasses of things which
are subclasses of other things. This allows us to easily find out what vaccines have the class "applicable to" equal to COVID-19, and, in
that sense, see what general category these vaccines are in.
"""
)

st.altair_chart(plot_vaccine_types(), use_container_width=True)

st.write(
    """
## Closing remarks

Wikidata is such a crazy concept that I still find it hard to believe it works! 
The amount of scientific knowledge that can be gathered from just this base is invaluable, 
I hope I was able to showcase at least some of it. 

And that's it! At least for now... See some interesting data that I've missed? Try to implement a nice visualization for it 
and send me a [pull request on github](https://github.com/jvfe/wikicovid-showcase/pulls)! Or, even better, fork my repo and do build your own analyses. 
The data you're thinking of isn't yet in Wikidata? [Maybe try adding it yourself!](https://www.wikidata.org/wiki/Wikidata:Tours) 
"""
)
