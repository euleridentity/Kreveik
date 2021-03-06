"""
Definition of network object.
"""

import numpy as num
import matplotlib.pyplot as plt
import copy
import itertools 
import logging
from kreveik.classes import *
import kreveik.probes as probes
from kreveik import network


class TopologicalNetwork(ProbeableObj):
    """
    This object is a stripped down network, designated to be a core 
    object for all network-like objects, like sub-graphs and motifs.
    """
    def __init__ (self, adjacency_matrix):
        ProbeableObj.__init__(self)
        self.adjacency = num.array(adjacency_matrix, dtype=bool)
        self.code = str(len(self.adjacency)) + "-" + str(reduce(lambda x, y : 2 * x + y,
                                                              self.adjacency.flatten() * 1))
        self.n_nodes = len(self.adjacency)
    
    def text_plot(self):
        for i in range(len(self.adjacency)):
            for j in range(len(self.adjacency)): 
                if self.adjacency[i][j] == True:
                    print str(j) + "--->" + str(i)     

    def indegree(self):
        return self.adjacency.sum(axis=0)
    
    def outdegree(self):
        return self.adjacency.sum(axis=1)
    
    def plot(self):
        """Opens a window, draws the graph into the window.
           Requires Tk, and of course a windowing system.
        """
        import Tkinter as tk
        import math
        window = tk.Tk()
        canvas_size = 400
        drawing = tk.Canvas(window, height=canvas_size, width=canvas_size, background="white")
        n_nodes = self.n_nodes
        radius = 150
        node_radius = 10
        
        drawing.create_text(200, 10, text="Network:" + str(id(self)))

        list_of_coordinates = [(radius * math.sin(2 * math.pi * n / n_nodes) + canvas_size / 2, radius * math.cos(2 * math.pi * n / n_nodes) + canvas_size / 2) for n in range(n_nodes)]
        
        for linksto, node in enumerate(self.adjacency):
            for linksfrom, link in enumerate(node):
                
                if linksto == linksfrom and link == True:
                    angle = math.atan2(list_of_coordinates[linksto][1] - 200,
                                      list_of_coordinates[linksto][0] - 200)
                    
                    drawing.create_line(list_of_coordinates[linksto][0] + node_radius * math.cos(angle),
                                        list_of_coordinates[linksto][1] + node_radius * math.sin(angle),
                                        list_of_coordinates[linksto][0] + node_radius * 2 * (math.cos(angle + 20)),
                                        list_of_coordinates[linksto][1] + node_radius * 2 * math.sin(angle + 20),
                                        list_of_coordinates[linksto][0] + node_radius * 4 * (math.cos(angle)),
                                        list_of_coordinates[linksto][1] + node_radius * 4 * math.sin(angle),
                                        list_of_coordinates[linksto][0] + node_radius * 2 * math.cos(angle - 20),
                                        list_of_coordinates[linksto][1] + node_radius * 2 * (math.sin(angle - 20)),
                                        list_of_coordinates[linksto][0] + node_radius * math.cos(angle),
                                        list_of_coordinates[linksto][1] + node_radius * math.sin(angle),
                                        smooth=True, joinstyle="round", fill="black", width=2, arrow="last"
                                        )
                
                elif link == True: 
                    angle = math.atan2(list_of_coordinates[linksto][1] - list_of_coordinates[linksfrom][1],
                                   list_of_coordinates[linksto][0] - list_of_coordinates[linksfrom][0])
                
                    drawing.create_line(list_of_coordinates[linksfrom][0] + node_radius * math.cos(angle),
                                        list_of_coordinates[linksfrom][1] + node_radius * math.sin(angle),
                                        list_of_coordinates[linksto][0] - node_radius * math.cos(angle),
                                        list_of_coordinates[linksto][1] - node_radius * math.sin(angle),
                                        fill="black", width=2, arrow="last")
        
        for node_ctr, (x, y) in enumerate(list_of_coordinates):

            if type(self) != Network:
                node_color = "white"
                text_color = "black"
            elif self.state == num.array([[]]):
                node_color = "white"
                text_color = "black"
            else:
                if self.state[-1][node_ctr] == True: 
                    node_color = "black"
                    text_color = "white"
                else:                
                    node_color = "white"
                    text_color = "black"
                    
            drawing.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, width=2, fill=node_color)
            drawing.create_text(x, y, text=str(node_ctr), fill=text_color, font="Arial")
            

        
        drawing.pack()
        window.mainloop()
        
    def save_plot(self, filename):
        """
        Saves the image as filename.ps in the working directory
        Requires Tk, and of course a windowing system.
        """
        import Tkinter as tk
        import math

        window = tk.Tk()
        canvas_size = 400
        drawing = tk.Canvas(window, height=canvas_size, width=canvas_size, background="white")
        n_nodes = self.n_nodes
        radius = 150
        node_radius = 10
        
        drawing.create_text(200, 10, text="Network:" + str(id(self)))
        drawing.pack()
        
        list_of_coordinates = [(radius * math.sin(2 * math.pi * n / n_nodes) + canvas_size / 2, radius * math.cos(2 * math.pi * n / n_nodes) + canvas_size / 2) for n in range(n_nodes)]
        
        for linksto, node in enumerate(self.adjacency):
            for linksfrom, link in enumerate(node):
                
                if linksto == linksfrom and link == True:
                    angle = math.atan2(list_of_coordinates[linksto][1] - 200,
                                      list_of_coordinates[linksto][0] - 200)
                    
                    drawing.create_line(list_of_coordinates[linksto][0] + node_radius * math.cos(angle),
                                        list_of_coordinates[linksto][1] + node_radius * math.sin(angle),
                                        list_of_coordinates[linksto][0] + node_radius * 2 * (math.cos(angle + 20)),
                                        list_of_coordinates[linksto][1] + node_radius * 2 * math.sin(angle + 20),
                                        list_of_coordinates[linksto][0] + node_radius * 4 * (math.cos(angle)),
                                        list_of_coordinates[linksto][1] + node_radius * 4 * math.sin(angle),
                                        list_of_coordinates[linksto][0] + node_radius * 2 * math.cos(angle - 20),
                                        list_of_coordinates[linksto][1] + node_radius * 2 * (math.sin(angle - 20)),
                                        list_of_coordinates[linksto][0] + node_radius * math.cos(angle),
                                        list_of_coordinates[linksto][1] + node_radius * math.sin(angle),
                                        smooth=True, joinstyle="round", fill="black", width=2, arrow="last"
                                        )
                
                elif link == True: 
                    angle = math.atan2(list_of_coordinates[linksto][1] - list_of_coordinates[linksfrom][1],
                                   list_of_coordinates[linksto][0] - list_of_coordinates[linksfrom][0])
                
                    drawing.create_line(list_of_coordinates[linksfrom][0] + node_radius * math.cos(angle),
                                        list_of_coordinates[linksfrom][1] + node_radius * math.sin(angle),
                                        list_of_coordinates[linksto][0] - node_radius * math.cos(angle),
                                        list_of_coordinates[linksto][1] - node_radius * math.sin(angle),
                                        fill="black", width=2, arrow="last")
        
        for node_ctr, (x, y) in enumerate(list_of_coordinates):

            if type(self) != Network:
                node_color = "white"
                text_color = "black"
            elif self.state == num.array([[]]):
                node_color = "white"
                text_color = "black"
            else:
                if self.state[-1][node_ctr] == True: 
                    node_color = "black"
                    text_color = "white"
                else:                
                    node_color = "white"
                    text_color = "black"
                    
            drawing.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, width=2, fill=node_color)
            drawing.create_text(x, y, text=str(node_ctr), fill=text_color, font="Arial")
            

        drawing.update()
        drawing.pack()
        drawing.postscript(file=filename + ".ps")
        window.destroy()                        # This destroys the window that is 
                                                # generated for the postscript extraction
                                                # We actually need a Tk setting which disables 
                                                # rendering
                                                # TODO (mehmet.ali.anil)
        
        #window.mainloop

    def laplacian(self):  
        """
        Returns the graph laplacian of the network
        """  
        symmetric = self.adjacency + self.adjacency.T - num.diag(self.adjacency.diagonal())
        degrees = num.diag(symmetric.sum(axis=0))
        laplacian = degrees - symmetric
        return laplacian
    
        
    def directed_laplacian(self):
        """
        Returns the laplacian of the network. It differs from laplacian function by using
        the original adjacency matrix, not the symmetricised version of it. 
        """
        original = self.adjacency - num.diag(self.adjacency.diagonal())
        degrees = num.diag(original.sum(axis=0) + original.sum(axis=1))
        laplacian = degrees - original
        return laplacian
        
    def indegree_laplacian(self):
        """
        Returns the laplacian composed of in-degrees of the nodes
        """
        original = self.adjacency - num.diag(self.adjacency.diagonal())
        degrees = num.diag(original.sum(axis=1))
        laplacian = degrees - original
        return laplacian  
    
    def outdegree_laplacian(self):
        """
        Returns the laplacian composed of out-degrees of the nodes
        """
        original = self.adjacency - num.diag(self.adjacency.diagonal())
        degrees = num.diag(original.sum(axis=0))
        laplacian = degrees - original
        return laplacian  
      
    def laplacian_eigvals(self):
        """
        Returns an ordered array of eigenvalues of the laplacian.
        """
        ordered_list = []
        values = []
        eigenvalues = num.linalg.eigvals(self.laplacian())   
        for i in range(len(self.adjacency)):
            values.append(eigenvalues[i])
        for i in range(len(self.adjacency)):
            ordered_list.append(min(values))
            values.remove(min(values))
        return num.array(ordered_list)
        
    def spectral_distance(self, other):
        """
        Computes spectral distance between networks.
        """
        difference = self.laplacian_eigvals() - other.laplacian_eigvals()
        distance = difference * difference
        spec_distance = distance.sum()
        return spec_distance
    
    def diameter(self):
        """
        Computes diameter of a network which means the maximum value of 
        the minimum number of edges between every pair of nodes.
        
        Note: diameter cannot be bigger than the number of nodes for 
        connected networks. This problem is eliminated by returning 
        number of nodes plus 1 for disconnected networks.
        """
        symmetric = self.adjacency + self.adjacency.T - num.diag(self.adjacency.diagonal())
        adj = symmetric * 1
        new_adjacency = adj
        summed_adjacency = adj
        result = 0
        for j in range(len(self.adjacency) + 1):
            result = result + 1
            if num.alltrue(summed_adjacency):                    
                break
            else:
                new_adjacency = num.dot(new_adjacency, adj)            
                summed_adjacency = summed_adjacency + new_adjacency
        return result

    def is_connected(self):
        """
        Returns True if the graph is connected, False if not.
        uses the algorithm explained in 
        http://keithbriggs.info/documents/graph-eigenvalues.pdf
        """
        symmetric = self.adjacency + self.adjacency.T - num.diag(
                                 self.adjacency.diagonal())
        if (0 in symmetric.sum(axis=0) or 0 in symmetric.sum(axis=1)):
            return False
        degrees = num.diagflat(symmetric.sum(axis=0))
        laplacian = degrees - symmetric
        determinant = num.linalg.det(laplacian + num.ones((len(laplacian), len(laplacian))))
        return not(num.allclose(determinant, 0.0))
    
    def remove_self_connection(self):
        """
        Removes self connections of the nodes in the network.
        """
        diagonal = num.diag(num.diag(self.adjacency))
        new_adjacency = self.adjacency - diagonal
        self.adjacency = new_adjacency
            
    def copy(self):
        """
        Returns a copy of the Topological Network object. 
        """
        return copy.deepcopy(self)
    
    def save(self, filename):
        """
        Saves the Network as an object to a file specified.
        """
        import pickle
        try:
            filehandler = open(filename + ".net", 'w')
            pickle.dump(self, filehandler) 
        except pickle.PickleError:
            logging.error("The object failed to be pickled.")

            

class Motif(TopologicalNetwork):
    """
    Motif is a 
    """
    def __init__(self, adjacency_matrix):
        TopologicalNetwork.__init__(self, adjacency_matrix)
        self.degree = len(adjacency_matrix)
    
    def __eq__(self, other):
        permutation_list = itertools.permutations(range(self.degree), self.degree)
        for permutation in permutation_list:
            
            if num.sum(self.indegree()) != num.sum(other.indegree()):
                return False

            newarray = num.zeros((len(self.adjacency), len(self.adjacency)), dtype=bool)
            #newarray[[node_init,node_end]] = newarray[[node_end,node_init]]
            #newarray[:,[node_init,node_end]] = newarray[:,[node_end,node_init]]
            for rowctr, row in enumerate(self.adjacency):
                for colctr, col in enumerate(row):
                    if col == True:
                        newarray[permutation[rowctr]][permutation[colctr]] = True
        
            if num.all(newarray == other.adjacency):
                return True
            
        return False    
        
 

class Network(TopologicalNetwork, Element):
    '''
    Network Class
    
    Input Arguments
        adjacency_matrix
        mask
        state_vec  
    '''
    def __init__ (self, adjacency_matrix, mask, function, state_vec=None):
        Element.__init__(self)
        TopologicalNetwork.__init__(self, adjacency_matrix)
        self.n_nodes = num.size(adjacency_matrix, 0)
        self.mask = mask
        if state_vec == None:
            state_vec = (num.random.random((1, self.n_nodes)) < 0.5)
        self.state = num.array(state_vec)
        self.function = function
    
    def __str__(self):
        return str(id(self))
        
    def info(self):
        '''
        Prints out an identification of the Network.
        Prints:
            Id
            Mothers
            Children
            Orbits
            Score
            Adjacency matrix
            sTate
            masK
        '''
        print "This network is : " + str(id(self)) + "."
        print "Nodes: " + str(self.n_nodes)
        print "Score: " + str(self.score)
        print "Its children are: "
        for child in self.children:
            print "   " + str(child)
        print "It has the following adjacency matrix: "
        print self.adjacency
        print "The following are the masks for each node: "
        for (num, node) in enumerate(self.mask):
            print str(num) + " th node : " + str(node)
        print "The following are the states with respect to time "
        for (t, state) in enumerate(self.state):
            print "t= " + str(t) + " : " + str(node)
        print "The scorer is : "
        print self.scorer
        
    def __getitem__(self, index):
        """
        nth item of a network object is the state that it is in, in the nth 
        iteration
        """
        if index > len(self.state):
            raise IndexError
        return self.state[index]
    
    def __contains__(self, state):
        """
        Returns a boolean according to whether a network includes the state  
        """
        item = num.array(state * True)
        return item in self.state
            
    def __call__ (self, state):
        """
        When a  network is called as a function, it sets the initial condition 
        as the given vector, finds the equilibrium of that state.
        """
        self.set_state(state)
        self.search_equilibrium(2 ** self.n_nodes, state, orbit_extraction=False, def_advance=1)
        
        
    def advance(self, times, start_from=None, *args):
        '''
        Advances the state in the phase space a given number of times.
        If a starter state is given, the initial condition is taken as the given state.
        If not, the last state is used instead.
        Input Arguments
            times -> the number of iterations to be taken.
            starter_state -> the initial state to be used
        '''
        
        if start_from != None:
            self.set_state(start_from)
            
        newstate = self.function(self, self.state[-1], times)
        self.state = num.append(self.state, newstate, axis=0)
            
        self.populate_probes(probes.advance)    

        
    def set_state(self, state):
        """
        Flushes the state of the system, and sets the new state as the given one 
        """
        
        if type(state) == int:
            state = [int(strings) == True for strings in list(num.binary_repr(
                                                (state), width=self.n_nodes))]
        state_bool = [i == True for i in state]
        state = [list(state_bool)]
        self.state = num.array(state)
        
    def set_mask(self, mask):
        """
        Sets the given mask as the new mask function.
        """
        self.mask = mask
        
    def plot_state(self, last=20):
        '''
        Plots the last 20 states as a black and white strips vertically.
        The vertical axis is time, whereas each strip is a single state.
        Input Arguments
            last -> the number of states that will be plotted 
        '''
        # Take the state vector, convert the list of arrays into a 2d array, then show it as an image
        # Black and white. 
        
#        plt.imshow(self.state[-last:],cmap=plt.cm.binary,interpolation='nearest')     
        plt.show()


    def plot_equilibria(self):
        """Creates a plot of the equilibria for all possible initial conditions
        in the phase space. Every point in the phase space corresponds to the 
        length of the orbit that initial condition is attracted to.
        """
        rowsandcols = 2 ** (len(self.adjacency) / 2)
        if self.n_nodes % 2 == 0:
            im_matrix = self.equilibria.reshape((rowsandcols, rowsandcols))
        
        if self.n_nodes % 2 == 1:
            im_matrix = self.equilibria.reshape((rowsandcols, rowsandcols * 2))
    
#        plt.imshow(im_matrix,cmap=plt.cm.gray,interpolation='nearest')
        
        plt.grid()
        plt.colorbar()
        plt.show()
             
           
    def search_equilibrium(self, chaos_limit, starter_state, orbit_extraction=False, trajectory_extraction=False, def_advance=1):
        '''
        Searches for an equilibrium point, or a limit cycle. 
        Returns the state vector, or the state vector list, if the equilibrium is a limit cycle.
        If no equilibrium is found, returns False.
        Input Arguments:
            starter_state -> the initial state vector that the state will evolve on.
            chaos_limit -> the degree that an orbit will be considered as chaotic.
                The calculation will stop when this point is reached.
            orbit_extraction -> True when every individual orbit is recorded with its degree.
        '''

        self.set_state(starter_state)
        starter_state = self.state[-1]
        
        for ctr in xrange(chaos_limit):

            self.advance(def_advance)
            
                
            row = num.all(self.state[-1] == self.state, axis=1) 
            where = num.where(row == True)
            
            if len(where[0]) > 1:
                frst_where = where[0][0]
                scnd_where = where[0][1]
                
                orbit_length = scnd_where - frst_where
                
                orbit = None
                trajectory = None
                location = reduce(lambda x, y : 2 * x + y, starter_state)
                
                if orbit_extraction:
                    orbit = self.state[frst_where:scnd_where]
                if trajectory_extraction:
                    trajectory = self.state[:frst_where + 1]
                self.populate_probes(probes.search_equilibrium)
                trajectory_length = frst_where + 1
                return (orbit_length, orbit, trajectory_length, trajectory)
            

        
            
    def populate_equilibria(self, orbit_extraction=False, trajectory_extraction=False, averaging=False, mean_trajectory_length=0):
        '''
        Creates all possible initial conditions by listing all possible 2^n boolean states.
        Then runs populate_equilibrium for each of them.
            populate_equilibrium returns orbits and-or degrees of the orbits.
        Gives scores to each of the networks, depending on the degree of the orbit each initial condition
        rests on.
        Input Arguments:
            normalize -> normalizes the scores to the value given.
        '''
        
        if not(hasattr(self, "equilibria")):
            self.equilibria = num.zeros(2 ** self.n_nodes)
        if not(hasattr(self, "orbits")):
            if orbit_extraction:
                self.orbits = num.array([None] * 2 ** self.n_nodes)
        if not(hasattr(self, "orbits")):
            if trajectory_extraction:
                self.trajectories = num.array([None] * 2 ** self.n_nodes)
        if not(hasattr(self, "trajectory_lengths")):
            self.trajectory_lengths = num.zeros(2 ** self.n_nodes)
                
        self.equilibria = num.zeros(2 ** self.n_nodes)
        if orbit_extraction:
            self.orbits = num.array([None] * 2 ** self.n_nodes)
        if trajectory_extraction:
            self.trajectories = num.array([None] * 2 ** self.n_nodes)
        
        binspace = range(0, num.power(2, self.n_nodes))
        unit_advance = 1 + mean_trajectory_length
        for location, state in enumerate(binspace):
            if self.equilibria[location] != None:                
                result = self.search_equilibrium(2 ** self.n_nodes, state, orbit_extraction, def_advance=unit_advance)
                (orbit_length, orbit, trajectory_length, trajectory) = result
                if orbit_extraction:
                    self.orbits[location] = orbit
                if trajectory_extraction:
                    self.trajectories[location] = trajectory
                string_repr=[[str(self.state[j][i] * 1) for i in range(len(self.state[j]))] for j in range(len(self.state))]
                int_state_list = [int(''.join(string_repr[k]), 2) for k in range(len(string_repr))]
                for int_state in int_state_list:
                    self.equilibria[int_state] = orbit_length
                    self.trajectory_lengths[int_state] = trajectory_length
                unit_advance = trajectory_length + mean_trajectory_length
            
        self.populate_probes(probes.populate_equilibria)

def search_all_orbits(self):
    """
    Searches orbits for all initial conditions.
    Returns the list of orbits for each initial state.
    """
    
    import numpy as num
    
    binspace = range(0, num.power(2, self.n_nodes))
    orbits_of_initials = []
    for state in binspace:
        (orbit_length, orbit) = self.search_equilibrium(2 ** self.n_nodes, state, True)
        orbits_of_initials.append(orbit)
    return orbits_of_initials

#def initial_states_of_orbits(self):
#    """
#    TODO
#    """
#    orbit_list=[]
#    initial_states=num.zeros(num.power(2,self.n_nodes))
#    count=0
#    binspace = range(0,num.power(2,self.n_nodes))
#    all_orbits=self.search_all_orbits()
#    for i in range(len(all_orbits)):
#        if initial_states[i]==0:
#            for j in range(len(all_orbits)):
#                
#            count=count+1

