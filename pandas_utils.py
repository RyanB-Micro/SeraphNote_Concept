
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



def save_project(nodes_list, filename="SeraphNote_Save_New.pk1"):
    # Create save directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Gather all data to be saved
    project_data = {
        'nodes': nodes_to_dataframe(nodes_list)
    }

    # Create and save pickle file
    pd.to_pickle(project_data, filename)
    print(f"Project _{filename}_ Saved")


def load_project(filename="SeraphNote_Save_New.pk1"):

    data_in = pd.read_pickle(filename)

    node_data = data_in['nodes']

    nodes_list = dataframe_to_nodes(node_data)

    return nodes_list
