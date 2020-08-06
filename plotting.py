from bokeh.io import show
from bokeh.models import Range1d, Plot, Circle, HoverTool, MultiLine
from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.plotting import from_networkx
from utils import wikidata_from_file, parse_query_results
import networkx as nx
import pandas as pd


def plot_network(network, tooltip, layout=nx.kamada_kawai_layout):
    """Makes a nice network plot with Bokeh
    Mostly stuff I pieced together from the bokeh tutorials.
    Args:
        network: A networkx Graph or DiGraph object.
        tooltip: A list of tuples that will define the tooltip. Follows this template:
            
            [("Node", "@index"), ("Attr", "@attr")]
            
            Where index corresponds the name of the node and attr is an attribute of the node.
            
        layout: A networkx layout, for example kamada_kawai or spectral.
    """

    plot = Plot(x_range=Range1d(-2, 2), y_range=Range1d(-2, 2))

    # Create a Bokeh graph from the NetworkX input
    graph = from_networkx(network, layout, scale=1.8, center=(0, 0))
    plot.renderers.append(graph)

    # Add some new columns to the node renderer data source
    graph.node_renderer.glyph.update(size=20, fill_color="orange")

    # When we hover over nodes, highlight nodes and adjacent edges
    graph.node_renderer.hover_glyph = Circle(size=20, fill_color="#abdda4")
    graph.edge_renderer.hover_glyph = MultiLine(line_color="#abdda4", line_width=4)
    graph.inspection_policy = NodesAndLinkedEdges()

    # Also add tooltip when hovering
    hover_obj = HoverTool()
    hover_obj.tooltips = tooltip
    plot.add_tools(hover_obj)

    show(plot)


def create_symptom_network():
    """Create a network from the symptom query and plot it"""

    qres = wikidata_from_file("queries/symptoms.rq")

    df = parse_query_results(
        qres, "symptomLabel", "subclassofLabel", "symptom", "subclassof"
    )

    node_attrs = (
        pd.DataFrame(
            {
                "node": df["symptomLabel"].append(df["subclassofLabel"]),
                "qid": df["symptom"].append(df["subclassof"]),
            }
        )
        .drop_duplicates(subset=["node"])
        .set_index("node")
    )

    edgelist = df.drop(columns=["symptom", "subclassof"])

    symptom_graph = nx.from_pandas_edgelist(
        edgelist,
        source="symptomLabel",
        target="subclassofLabel",
        create_using=nx.OrderedDiGraph,
    )

    nx.set_node_attributes(symptom_graph, node_attrs.to_dict(orient="index"))

    return symptom_graph
