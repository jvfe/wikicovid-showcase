from collections import defaultdict
from functools import lru_cache
from itertools import product, chain
import pandas as pd
import requests


@lru_cache
def perform_query(query):
    """Performs a SPARQL query to the wikidata endpoint

    Args:
        query: A string containing a functional sparql query

    Returns:
        A json with the response content.
    """

    endpoint_url = "https://query.wikidata.org/sparql"

    try:
        response = requests.get(
            endpoint_url,
            params={"query": query},
            headers={"Accept": "application/sparql-results+json"},
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(err)

    else:
        raw_results = response.json()

        return raw_results


def parse_query_results(query_result):
    """Parse wikidata query results into a nice dataframe
    
    Args:
        query_result: A json dict with the results from the query

    Returns:
        A pandas dataframe with a column for each component from field_list.
    """

    parsed_results = defaultdict(list)

    data = query_result["results"]["bindings"]

    keys = frozenset(chain.from_iterable(data))

    for json_key, item in product(data, keys):
        try:
            parsed_results[item].append(json_key[item]["value"])
        except:
            # If there is no data for a key, append a null string
            parsed_results[item].append("")

    results_df = pd.DataFrame.from_dict(parsed_results).replace(
        {"http://www.wikidata.org/entity/": ""}, regex=True
    )

    return results_df


def query_wikidata(query):

    query_res = perform_query(query)

    parsed_res = parse_query_results(query_res)

    return parsed_res


def wikidata_from_file(query_file):
    """Runs a wikidata query from a file"""
    with open(query_file, "r") as q:
        query_string = q.read()

    results = query_wikidata(query_string)

    return results
