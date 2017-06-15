#!/usr/bin/env python3

"""
This program fetches MITH's current project data from the research
explorer and builds a graph of people and the projects they've worked on.
It then projects the graph so that people are connected via their shared 
membership in a project and saves the relationships as js/people.js

You will need to have networkx installed for it to work.
"""

import csv
import sys
import json
import networkx

from urllib.request import urlopen
from networkx.algorithms.bipartite.projection import weighted_projected_graph

def to_json(g):
    """
    Turns a networkx graph into JSON data that D3 expects.
    """

    j = {"nodes": [], "links": []}

    for node_id in g.nodes():
        j["nodes"].append({"id": node_id})

    for source, target in g.edges():
        j["links"].append({
            "source": source,
            "target": target
        })

    return j

url = "http://mith.umd.edu/wp-content/mu-plugins/mith-research-explorer-data/projects.json"

people = set()
g = networkx.Graph()

for project in json.load(urlopen(url)):
    for member in project['member']:
        people.add(member['name'])
        g.add_edge(member['name'], project['title'])

g = weighted_projected_graph(g, people) 

for node in g.nodes():
    if g.degree(node) == 0:
        g.remove_node(node)

js = "var people = " + json.dumps(to_json(g), indent=2) + ";\n"
open("js/people.js", "w").write(js)
