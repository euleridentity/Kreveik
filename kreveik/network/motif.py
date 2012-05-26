
#    Copyright 2012 Mehmet Ali ANIL
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#    http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import logging
import numpy as num
import itertools
import kreveik


def all_conn_motifs(nodes):
    """
    Returns a list of all connected motifs for a degree.
    
    This function takes every possible (fully connected) configuration of a graph with n nodes.
    And lists them as a list of all possible motifs. 
    
    Input Arguments:
    ---------------
    
    nodes
        The number of nodes of the motifs that will be generated.
    """
    logging.info("Returning all connected motifs with "+str(nodes)+" nodes")
    motiflist = []
    degree = nodes**2
    for number in xrange(2**degree):
        linear = num.array([int(item) for item in [False]*
                   (degree-len(list(bin(number)[2:])))+list(bin(number)[2:])],dtype=bool)
        motifadj = num.reshape(linear,(nodes,nodes))
        motif = kreveik.classes.Motif(motifadj)
        if motif.is_connected() and not(any([motif==motiffromlist[0] for
                                              motiffromlist in motiflist])):
                motiflist.append([motif,0])
    return motiflist

    
def motif_freqs (network,degree,**kwargs):
    """
    Returns a list of motifs for a given network
    
    This function takes every possible combinations of nodes counting degree, out of all
    nodes of the network provided, and counts them in a list of all motifs. 
    
    Args:
    ----
        network: the network which motif frequencies will be found.
        degree: the number of nodes of the motifs that will be searched in the network.
        motiflist: an optional argument in which if supplied, the search will be limited to
        motifs in that list.
        
    Returns:
    -------
    A numpy array of [Motif object , number of occurences], an N x 2 array. 
        
    """
    import itertools
    
    logging.info("Extracting "+str(degree)+" motifs of network "+str(network))
    all_combinations = itertools.combinations(range(len(network.adjacency)),degree)
    
    if 'motiflist' in kwargs:
        allmotifs = kwargs['motiflist'][:]
        motif_list = allmotifs[:]
        if len(motif_list[0]) == 1:
            # if only a list of motifs are presented, not a list and numbers.
            motif_list = num.array([[motif,0] for motif in motiflist])
    else:
        logging.info("Creating all possible motifs of node count "+str(degree)+".")
        motif_list = all_conn_motifs(degree)[:]
        
    logging.info("Extracting motifs from all possible "+str(degree)+" node combinations of the network.")
    
    for combination in all_combinations:
        logging.debug("Motif Permutation:"+str(list(combination)))
        
        this_motif_adj = num.zeros((degree,degree), dtype = bool)
        for (first_ctr,first_node) in enumerate(list(combination)):
            for (second_ctr,second_node) in enumerate(list(combination)):
                this_motif_adj[first_ctr][second_ctr] = network.adjacency[first_node][second_node]
        
        this_motif = kreveik.classes.Motif(this_motif_adj)
        logging.debug("Motif Adjacency:")
        logging.debug(list(combination))
        logging.debug(str(this_motif_adj))
        if this_motif.is_connected():
            truth = [this_motif == motif_vec[0] for motif_vec in motif_list]
            if (any(truth) == True):
                index = truth.index(True)
                motif_list[index][1] = motif_list[index][1]+1
            elif (all(truth) == False):
                logging.info("")
                motif_list.append([this_motif,1])
            else:
                logging.error("There has been a problem while extracting Motifs")
                break
        
    logging.info("Extraction done!")
    return motif_list
