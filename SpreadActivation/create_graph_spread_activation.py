#Overall Goal: To write a module that will create a graph with a random number
#of nodes between 100 and 1000.

#General Outline: Create a network that contains nodes and links between those
#nodes. Nodes will be linked to a random number of other nodes, but not themselves
from random import *


#Write this script so that it can be called as a module.
def create_network():   
    
    #Create a node object. Note, some of these attributes will not be used by every
    #script that calls it (e.g., color and distance).
    class node(object):
        def __init__(self, infected, color):
            self.identifier = "na"
            self.links = []
            self.activated = infected
            self.connected_to = []
            self.children = []
            self.color = color
            self.pred = None
            self.distance = 0
            
    #Create a link object. Give it attributes for each of the nodes that it
    #connects. 
    class link(object):
        def __init__(self, value, node1, node2):
            self.node1 = node1
            self.node2 = node2
       
    #Make the links. Links will be probabilistic, so not every node will be connected
    #to every other node.
    def make_links(idx1, idx2, node1, node2):
        #If the two selected nodes are not the same node and random
        #results in 0, make a link between them.
        #Note, this line will control how interconnected the network is.
        #Change it to change the network's connectivity.
        if (idx1 != idx2) and (randint(0,10) == 0):
            new_link = (link(0.00, node1, node2))
            links.append(new_link)
            node1.links.append(new_link)
            node2.links.append(new_link)
            node1.connected_to.append(node2)
            node2.connected_to.append(node1)
    
    #############################   
    #####CREATE THE NETWORK ####
    ############################
    
    #Start lists of the nodes and the links. These are empty for now.
    nodes = []
    links = []
    
    #Randomly select how many nodes you are going to have
    number_of_nodes = randint(100, 1000)
    
    #Make the number of nodes specified by the number_of_nodes variable.
    #Initialize them to not be infected, and to be colored "white".
    [nodes.append(node(False, "white")) for new_node in range(number_of_nodes)]
 
    #Give the nodes distinct id numbers.
    for idx, node in enumerate(nodes):                                          
        node.identifier=idx

    #Make the links for the network
    
    #Select 2 nodes from the network, and if they are not already connected,
    #give the chance to make a link between them.
    for idx1, node1 in enumerate(nodes):
        for idx2, node2 in enumerate(nodes):
            if node2 not in node1.connected_to:
                make_links(idx1, idx2, node1, node2)
    
    return nodes, links

#Call the module. 
if __name__ == '__main__':
    create_network()
