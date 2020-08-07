from utils import wikidata_from_file
import altair as alt
import pandas as pd


def plot_interventions(min_mentions):

    interv_query = wikidata_from_file("queries/clinicaltrialsByIntervention.rq")

    interv_query["trials"] = interv_query["trials"].astype(int)
    interv_query["Percent"] = interv_query["trials"] / sum(interv_query["trials"])
    interv_query = interv_query[interv_query["trials"] >= min_mentions]

    plot = (
        alt.Chart(interv_query)
        .mark_bar()
        .encode(
            x=alt.X("Percent:Q", axis=alt.Axis(format=".0%")),
            y=alt.Y("interventionLabel:N", sort="x"),
        )
    )

    return plot


def plot_vaccine_types():

    vacc = wikidata_from_file("queries/vaccines.rq")

    vacc = vacc[vacc["typeLabel"] != "vaccine candidate"]
    vacc_percs = (vacc["typeLabel"].value_counts() / vacc.shape[0]).reset_index()

    # What types of vaccines are being studied for COVID-19?
    plot = (
        alt.Chart(vacc_percs)
        .mark_bar()
        .encode(
            x=alt.X("typeLabel:Q", axis=alt.Axis(format=".0%")),
            y=alt.Y("index:N", sort="x"),
        )
    )

    return plot


def plot_literature_interactions():

    lit_inter = wikidata_from_file("queries/literatureInteractions.rq")

    lit_inter["count"] = lit_inter["count"].astype(int)

    # Find a better way to do this - Perhaps another query?
    lit_transf = lit_inter.replace(
        {
            "Angiotensin I converting enzyme 2": "ACE2",
            "Furin, paired basic amino acid cleaving enzyme": "FURIN",
            "Transmembrane serine protease 2": "TMPRSS2",
            "Interferon induced transmembrane protein ": "IFITM",
            "BCL2 associated X, apoptosis regulator": "BAX",
            "Alanyl aminopeptidase, membrane": "AAP",
            "Alanyl aminopeptidase, membrane": "AAP",
            "Peptidylprolyl isomerase A": "PPIA",
            "Dipeptidyl peptidase 4": "DPP4",
            "severe acute respiratory syndrome-related coronavirus": "SARS-related CoV",
        },
        regex=True,
    )

    lit_grouped = lit_transf.groupby(["geneLabel", "virusLabel"]).sum().reset_index()

    plot = (
        alt.Chart(lit_grouped)
        .mark_circle()
        .encode(
            x=alt.X("geneLabel:O", title="Gene or protein"),
            y=alt.Y("virusLabel:O", title=None),
            size=alt.Size("count:Q", title="# of articles"),
            color=alt.Color("virusLabel", legend=None),
        )
    )

    return plot


def plot_pathway_by_virus():

    pathways = wikidata_from_file("queries/covidpathways.rq")

    pathways_transf = (
        pathways.groupby(["virusLabel", "pathwayLabel", "wikiPathID"])
        .count()
        .reset_index()
        .drop(["componentLabel", "virus", "pathway"], axis=1)
        .replace(
            {
                "severe acute respiratory syndrome-related coronavirus": "SARS-related CoV"
            },
            regex=True,
        )
    )

    pathways_transf["url"] = (
        "https://www.wikipathways.org/index.php/Pathway:"
        + pathways_transf["wikiPathID"]
    )

    plot = (
        alt.Chart(pathways_transf)
        .mark_circle()
        .encode(
            # x=alt.X("virusLabel:N", title="# of components"),
            y=alt.Y("wikiPathID:N", title=None),
            color=alt.Color("virusLabel:N", legend=None),
            size=alt.Size(
                "component:Q", legend=None, scale=alt.Scale(range=[100, 300])
            ),
            href="url:N",
            tooltip=[
                alt.Tooltip("component:Q", title="# of components"),
                alt.Tooltip("pathwayLabel:N", title="Pathway"),
            ],
            column=alt.Column("virusLabel:N", title=None, spacing=55),
        )
    )

    return plot
