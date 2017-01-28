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
    # graph.add_nodes_from(data['startup_name'], bipartite=0)
    # graph.add_nodes_from(data['investor_name'], bipartite=1)
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


def calc_weight_and_write(data):
    """
    Calculate and make primary graph edges
    :param data:
    :return:
    """
    investor_startup_graph = make_graph(data)
    print(investor_startup_graph.edges)
    output_link = open('./dataset/Links.csv', 'weight')
    output_label = open('./dataset/labels.csv', 'weight')
    startup_id_dict, id_startup_dict, investor_id_dict, id_investor_dict = making_investor_startup_dicts(data)
    startup_id_dict_len, investor_id_dict_len = startup_id_dict.__len__(), investor_id_dict.__len__()

    edge_id = 0
    for i in range(startup_id_dict_len):
        for j in (range(i + 1, startup_id_dict_len)):
            print(id_startup_dict[i], '--', id_startup_dict[j])
            weight = nx.common_neighbors(investor_startup_graph, id_startup_dict[i], id_startup_dict[j])
            print(weight)
            if weight != 0:
                output_link.write(str(edge_id))
                output_link.write(',')
                output_link.write(str(id_startup_dict[i]))
                output_link.write(',')
                output_link.write(str(i))
                output_link.write(',')
                output_link.write(str(id_startup_dict[j]))
                output_link.write(',')
                output_link.write(str(j))
                output_link.write(',')
                output_link.write(str(weight))
                output_link.write("\n")
                edge_id = edge_id + 1
        # if i%100 ==0 :
        # print(i)

    for i in range(startup_id_dict_len):
        output_label.write(str(i))
        output_label.write(',')
        output_label.write(str(id_startup_dict[i]))
        output_label.write("\n")

def metrics(graph,data):
    """
    Calculate metrics for the startups' graph.
    Metrics calculated are:
        1. Closeness
        2. Degree
        3. Betweenness
        4. PageRank
    :param graph: A NetworkX graph of Startups and companies
    :param data:
    :return:
    """
    # print('calculating metrics...')
    # print(120*'+','Closeness ...')
    closeness = nx.closeness_centrality(graph, u=None, distance=None)
    # Eig = nx.eigenvector_centrality(graph)
    # print(120 * '+', 'Degree ...')
    deg = nx.degree_centrality(graph)
    # print(120 * '+', 'Betweenness ...')
    bet = nx.betweenness_centrality(graph, k=None, normalized=False, weight=None, endpoints=False)
    # print(120 * '+', 'Page rank ...')
    pagerank = nx.pagerank(graph)
    return closeness,deg, bet, pagerank
