'''
Created on Mar 8, 2011

@author: Mehmet Ali Anil
'''
import numpy as num
import genereg
import networkx as nx
import matplotlib.pyplot as plt
import pickle



__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = "GPL"
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"
        

if __name__ == '__main__':
    net = [None]*500
    petri2 = genereg.family()
    
    for numbertag,network in enumerate(net): 
        net[numbertag] = genereg.generate_random(4)
        petri2.add_to_family(net[numbertag])
    
    scores = []
    kout=[]

    petri2.populate_equilibria_in_family()
    
for i in range(1,5):
    meanscore = petri1.equilibria.mean()
    petri1.genetic_iteration(18)
    scores.append(petri1.equilibria.tolist())
    all_degrees = [net.nx.in_degree().values() for net in petri1.network_list]
    kout.append(all_degrees)
