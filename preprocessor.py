import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def load_and_sample_data():
    """
    Import data from the dataset
    :return: Dictionary samples
    """
    print('loading data...')
    data = pd.read_csv('./dataset/Link.csv')
    df_percent = data.sample(frac=0.001)
    return df_percent

def make_graph(data: dict) -> dict:
    """
    Constructing a bipartite graph for calcW_and_write() method
    to calculate the common investors startups have
    :param data: Dictionary object containing data
    :return:
    """
    print('Building the graph...')
    company_investor_graph = nx.Graph()
    company_investor_graph.add_nodes_from(data['company_name'], bipartite=0)
    company_investor_graph.add_nodes_from(data['investor_name'], bipartite=1)
    company_investor_graph.add_weighted_edges_from(
        [(row['company_name'], row['investor_name'], 1) for idx, row in data.iterrows()],
        weight='weight'
    )
    return company_investor_graph

def make_graph_weighted(data: dict) -> dict:
    """
    Constructing a weighted graph
    :param data: Dictionary samples
    :return: Waited graph
    """
    company_investor_weighted_graph = nx.Graph()
    # B.add_nodes_from(data['company_name'], bipartite=0)
    # B.add_nodes_from(data['investor_name'], bipartite=1)
    company_investor_weighted_graph.add_weighted_edges_from(
        [(row['Source'], row['Target'], row['Weight']) for idx, row in data.iterrows()],
        weight='weight')
    return company_investor_weighted_graph

def making_dicts(data):
    """

    :param data:
    :return:
    """
    company_id, x2 = 0, 0
    company_id_dict = {}
    id_company_dict = {}

    # print('making dicts...')
    # # print(data)
    for company_name in data['name']:
        if company_name not in company_id_dict:
            company_id_dict.update({company_name: company_id})
            id_company_dict.update({company_id: company_name})
            company_id = company_id + 1
    return company_id_dict,id_company_dict
