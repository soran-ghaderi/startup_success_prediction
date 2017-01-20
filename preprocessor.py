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
    Create two dictionaries: ID-Startup and Startup-ID
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


def making_investor_startup_dicts(data: dict) -> tuple[dict, dict]:
    """
    Create two dictionaries: ID-Startup, Startup-ID, Investor_ID and ID_Investor
    :param data: Dictionary containing companies data
    :return: Four dictionaries: 1. ID-Startup 2. Startup-ID 3. Investor_ID 4. ID_Investor
    """
    startup_id, investor_id = 0, 0
    startup_id_dict = {}
    id_startup_dict = {}
    investor_id_dict = {}
    id_investor_dict = {}
    # print('making dicts...')
    for startup_name in data['company_name']:
        if startup_name not in startup_id_dict:
            startup_id_dict.update({startup_name: startup_id})
            id_startup_dict.update({startup_id: startup_name})
            startup_id = startup_id + 1
    for investor_name in data['investor_name']:
        if investor_name not in investor_id_dict:
            investor_id_dict.update({investor_name: investor_id})
            id_investor_dict.update({investor_id: investor_name})
            investor_id = investor_id + 1
    return startup_id_dict, id_startup_dict, investor_id_dict, id_investor_dict


def calcW_and_write(data):
    """
    Calculate and make primary graph edges
    :param data:
    :return:
    """
    # data = load_data()
    investor_startup_graph = make_graph(data)
    print(investor_startup_graph.edges)
    out = open('./dataset/Links.csv', 'w')
    out2 = open('./dataset/labels.csv', 'w')
    startup_id_dict, id_startup_dict, investor_id_dict, id_investor_dict = making_investor_startup_dicts(data)
    startup_id_dict_len, investor_id_dict_len = startup_id_dict.__len__(), investor_id_dict.__len__()

    id_counter, cc = 0, 0
    for i in range(startup_id_dict_len):
        for j in (range(i + 1, startup_id_dict_len)):
            print(id_startup_dict[i], '--', id_startup_dict[j])
            w = nx.common_neighbors(investor_startup_graph, id_startup_dict[i], id_startup_dict[j])
            print(w)
            if w != 0:
                out.write(str(id_counter))
                out.write(',')
                out.write(str(id_startup_dict[i]))
                out.write(',')
                out.write(str(i))
                out.write(',')
                out.write(str(id_startup_dict[j]))
                out.write(',')
                out.write(str(j))
                out.write(',')
                out.write(str(w))
                out.write("\n")
                id_counter = id_counter + 1
        # if cc%100 ==0 :
        # print(cc)

        cc = cc + 1
    for i in range(startup_id_dict_len):
        out2.write(str(i))
        out2.write(',')
        # out2.write(str(id_startup_dict[i]))
        out2.write("\n")
