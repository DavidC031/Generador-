import os
import json
import shutil,bz2,getopt
import networkx as nx
from collections import defaultdict


def parse_args():
    """
    Parsea los argumentos de entrada

    Args:
        None

    Returns:
        dict: Diccionario con los argumentos de entrada
    """

    args = {}
    options, _ = getopt.getopt(sys.argv[1:], "d:fi:ff:h:", ["dir=", "fi=", "ff=", "hashtags="])
    for opt, arg in options:
        if opt in ("-d", "--dir"):
            args["dir"] = arg
        elif opt in ("-fi", "--fi"):
            args["fecha_inicial"] = arg
        elif opt in ("-ff", "--ff"):
            args["fecha_final"] = arg
        elif opt in ("-h", "--hashtags"):
            args["hashtags"] = arg
    return args


def get_tweets(directorio):
    """
    Obtiene los tweets de un directorio

    Args:
        directorio: Directorio donde se encuentran los tweets

    Returns:
        list: Lista con los tweets
    """

    tweets = []
    for archivo in os.listdir(directorio):
        with bz2.open(os.path.join(directorio, archivo), "r") as f:
            tweets.extend(json.load(f))
    return tweets


def get_retweets(tweets):
    """
    Obtiene los retweets de una lista de tweets

    Args:
        tweets: Lista con los tweets

    Returns:
        list: Lista con las aristas del grafo de retweets
    """

    retweets = []
    for tweet in tweets:
        if tweet["retweeted_status"]:
            retweets.append((tweet["id"], tweet["retweeted_status"]["user"]["id"]))
    return retweets


def get_menciones(tweets):
    """
    Obtiene las menciones de una lista de tweets

    Args:
        tweets: Lista con los tweets

    Returns:
        list: Lista con las aristas del grafo de menciones
    """

    menciones = []
    for tweet in tweets:
        for user in tweet["entities"]["user_mentions"]:
            menciones.append((tweet["user"]["id"], user["id"]))
    return menciones


def get_corretweets(tweets):
    """
    Obtiene los corretweets de una lista de tweets

    Args:
        tweets: Lista con los tweets

    Returns:
        list: Lista con las aristas del grafo de corretweets
    """

    corretweets = []
    for tweet in tweets:
        if tweet["retweeted_status"]:
            for user in tweet["retweeted_status"]["retweeted_by"]:
                corretweets.append((tweet["user"]["id"], user["id"]))
    return corretweets


def create_graph(edges, directed=False):
    """
    Crea un grafo a partir de una lista de aristas

    Args:
        edges: Lista con las aristas
        directed: Si el grafo es dirigido

    Returns:
        nx.Graph: Grafo
    """

    graph = nx.Graph()
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


def save_graph(graph, filename):
    """
    Guarda un grafo en un archivo

    Args:
        graph: Grafo
        filename: Nombre del archivo

    Returns:
        None
    """

    nx.write_gexf(graph, filename)


def save_json(data, filename):
    """
    Guarda un diccionario en un archivo JSON

    Args:
        data: Diccionario
        filename: Nombre del archivo

    Returns:
        None
    """

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
