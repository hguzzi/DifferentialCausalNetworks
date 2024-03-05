import sys
def main():
    #install gcastle 
    #pip install gcastle==1.0.3

    #checks args
    if len(args) != 6:
        print("Error: failed check args")
        return
    
    #df_name = name of file csv preprocessed for the tissue in analysis, 
    #graph1 = name to save male causal graph
    #graph2 = name to save female causal graph
    #sim_graph = name to save the symmetric difference between female and male causal graph
    #graph12 = name to save the difference between male and female causal graph
    #graph21 = name to save the difference between female and male causal graph
    df_name, graph1, graph2, sim_graph, graph12, graph21 = args

    import pandas as pd
    df = pd.read_csv(df_name)
    df = df.drop('Unnamed: 0', axis=1)
    
    #splitts the dataset in male data and female data
    df1 = df.copy()
    df1 = df1[df1['SEX'] == 1]
    df1 = df1.drop('SEX', axis=1)

    df2 = df.copy()
    df2 = df2[df2['SEX'] == 2]
    df2 = df2.drop('SEX', axis=1)

    import networkx as nx
    from networkx.readwrite import graphml
    import matplotlib.pyplot as plt
    import os
    os.environ['CASTLE_BACKEND'] = 'pytorch'
    import numpy as np
    import networkx as nx
    from castle.algorithms import PC

    #applies PC algorithm for causal discovery to
    #both datasets for males and females
    nodes1 = [col for col in df1.columns]
    pc1 = PC()
    pc1.learn(df1, columns = nodes1)
    #pc1.causal_matrix
    graph1 = nx.from_numpy_array(pc1.causal_matrix, create_using=nx.DiGraph)
    mapping1 = {node: label for node, label in zip(graph1.nodes(), pc1.causal_matrix.columns)}
    graph1 = nx.relabel_nodes(graph1, mapping1)
    graphml.write_graphml(graph1, graph1)

    nodes2 = [col for col in df2.columns]
    pc2 = PC()
    pc2.learn(df2, columns = nodes2)
    #pc2.causal_matrix
    graph2 = nx.from_numpy_array(pc2.causal_matrix, create_using=nx.DiGraph)
    mapping2 = {node: label for node, label in zip(graph2.nodes(), pc2.causal_matrix.columns)}
    graph2 = nx.relabel_nodes(graph2, mapping2)
    graphml.write_graphml(graph2, graph2)


    #computes and saves differential causal networks
    R = nx.symmetric_difference(graph1, graph2)
    graphml.write_graphml(R, sim_graph)

    R1 = nx.difference(graph1, graph2)
    graphml.write_graphml(R1, graph12)

    R2 = nx.difference(graph2, graph1)
    graphml.write_graphml(R2, graph21)

    # Paarametri
    print("Parametri passati:", args)

if __name__ == "__main__":
    main()
