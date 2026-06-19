
import pandas as pd
import pickle
import nodes
import os

pandas_version = pd.__version__


def nodes_to_dataframe(node_list):
    # Clear buffer for dataframe
    node_data = []

    # Loop through each node created
    for node in node_list:
        node_data.append(node.data_out())

    return pd.DataFrame(node_data)


def dataframe_to_nodes(node_dataframe):
    node_list = []
    for _,row in node_dataframe.iterrows():
        node = nodes.Node(row['x'], row['y'], row['colour'], row['text'])
        node.data_in(row)
        node_list.append(node)

    return node_list

def facts_to_dataframe(facts_list):
    # Clear buffer for dataframe
    facts_data = []

    # Loop through each node created
    for facts in facts_list:
        facts_data.append(facts.data_out())

    return pd.DataFrame(facts_data)


def dataframe_to_facts(facts_dataframe):
    facts_list = []
    for _,row in facts_dataframe.iterrows():
        facts = nodes.Fact(row['x'], row['y'], row['colour'], row['text'])
        facts.data_in(row)
        facts_list.append(facts)

    return facts_list


def bonds_to_dataframe(bonds_list):
    # Clear buffer for dataframe
    bonds_data = []

    # Loop through each node created
    for bonds in bonds_list:
        bonds_data.append(bonds.data_out())

    return pd.DataFrame(bonds_data)


def dataframe_to_bonds(bonds_dataframe):
    bonds_list = []
    for _,row in bonds_dataframe.iterrows():
        bonds = nodes.Bond(row['node_1'], row['node_2'], row['corner_1'], row['corner_2'])
        bonds.data_in(row)
        bonds_list.append(bonds)

    return bonds_list




def save_project(nodes_list, facts_list, bonds_list, filename="SeraphNote_Save_New.pk1"):
    # Create save directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Gather all data to be saved
    project_data = {
        'nodes': nodes_to_dataframe(nodes_list),
        'facts': facts_to_dataframe(facts_list),
        'bonds': bonds_to_dataframe(bonds_list)
    }

    # Create and save pickle file
    pd.to_pickle(project_data, filename)
    print(f"Project _{filename}_ Saved")


def refresh_bonds(bonds, nodes, facts):
    for bond in bonds:
        bond.refresh_connections(nodes, facts)


def load_project(filename="SeraphNote_Save_New.pk1"):

    data_in = pd.read_pickle(filename)

    node_data = data_in['nodes']
    fact_data = data_in['facts']
    bond_data = data_in['bonds']

    nodes_list = dataframe_to_nodes(node_data)
    fact_list = dataframe_to_facts(fact_data)
    bond_list = dataframe_to_bonds(bond_data)

    refresh_bonds(bond_list, nodes_list, fact_list)

    return nodes_list, fact_list, bond_list
