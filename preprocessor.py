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
    company_investor_graph.add_nodes_from(data['startup_name'], bipartite=0)
    company_investor_graph.add_nodes_from(data['investor_name'], bipartite=1)
    company_investor_graph.add_weighted_edges_from(
        [(row['startup_name'], row['investor_name'], 1) for idx, row in data.iterrows()],
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
    # B.add_nodes_from(data['startup_name'], bipartite=0)
    # B.add_nodes_from(data['investor_name'], bipartite=1)
    company_investor_weighted_graph.add_weighted_edges_from(
        [(row['Source'], row['Target'], row['Weight']) for idx, row in data.iterrows()],
        weight='weight')
    return company_investor_weighted_graph


def making_startup_dicts(data: dict) -> tuple[dict, dict]:
    """
    Create two dictionaries: ID-Company and Company-ID
    :param data: Dictionary containing companies data
    :return: Two dictionaries: 1. ID-company 2. company-ID
    """
    startup_id = 0
    startup_id_dict = {}
    id_company_dict = {}

    # print('making dicts...')
    for startup_name in data['name']:
        if startup_name not in startup_id_dict:
            startup_id_dict.update({startup_name: startup_id})
            id_company_dict.update({startup_id: startup_name})
            startup_id = startup_id + 1
    return startup_id_dict, id_company_dict

def making_investor_startup_dicts(data):
    """
    Create two dictionaries: ID-Startup, Startup-ID, Investor_ID and ID_investor
    :param data:
    :return:
    """
    x, x2 = 0, 0
    company_dic = {}
    company_dic2 = {}
    investor_dic = {}
    investor_dic2 = {}
    # print('making dicts...')
    # # print(data)
    for i in data['company_name']:
        if i not in company_dic:
            company_dic.update({i: x})
            company_dic2.update({x: i})
            x = x + 1
    for i in data['investor_name']:
        if i not in investor_dic:
            investor_dic.update({i: x2})
            investor_dic2.update({x2: i})
            x2 = x2 + 1
    # print(company_dic2.__len__())
    return company_dic,company_dic2, investor_dic, investor_dic2
