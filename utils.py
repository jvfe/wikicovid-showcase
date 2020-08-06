from collections import defaultdict
import pandas as pd
import requests


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
        print(err)

    else:
        raw_results = response.json()

        return raw_results


def parse_query_results(query_result, field_list):
    """Parse wikidata query results into a nice dataframe
    
    Args:
        query_result: A json dict with the results from the query
        field_list: A list of the fields from the response you want in your final dataframe.

    Returns:
        A pandas dataframe with a column for each component from field_list.
    """

    parsed_results = defaultdict(list)

    for q_r in query_result["results"]["bindings"]:
        for item in field_list:
            parsed_results[item].append(q_r[item]["value"])

    results_df = pd.DataFrame.from_dict(parsed_results).replace(
        {"http://www.wikidata.org/entity/": ""}, regex=True
    )

    return results_df


def wikidata_from_file(query_file, field_list):
    """Runs a wikidata query from a file"""
    with open(query_file, "r") as q:
        query_string = q.read()

    query_res = perform_query(query_string)

    parsed_res = parse_query_results(query_res, field_list)

    return parsed_res
