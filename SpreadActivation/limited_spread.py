#Overall Goal: To run a network that spreads activation from one node to a
#limited number of others based on distance from that intial node. This was just a silly exercise
#to practice spreading activation around a network. 

#General Outline: Create the network, then designate one node as the initial start point.
#Partition the network based on proximity to that node. Spread activation to a desired number
#of nodes based on that proximity. 

import math
from random import *  
import create_graph_spread_activation
  
#Function to determine node distances from the "initially activated"
#node. It starts with a breadth first search: it colors the instructor as black,
#then moves to the nodes adjacent to the instructor. It colors 
#those gray and moves them to a cue. Once the layer is entirely gray, it begins
#at the beginning of the cue, and moves through the unvisited nodes connected to
#each node in the cue in the same way, until the entire network has been visited.
def describe_network(network, start_node):

    #Initiate the cue, let it hold the instructor node, since it is the starting point
    cue = [start_node]

    #Continue to search nodes as long as there are items in the cue.
    while len(cue) > 0:
        
        #Start at the front of the cue, color it black
        current_node = cue[0]
        current_node.color="black"
        
        #For all the nodes connected to the current node, check if it's been visited.
        #If it hasn't, then color it gray and move it to the cue.
        for link in current_node.links:
            if link.node1.color=="white":
                link.node1.color="gray"
                link.node1.pred = current_node
                link.node1.distance = current_node.distance + 1
                link.node1.pred = current_node
                cue.append(link.node1)
                current_node.children.append(link.node1)

            if link.node2.color =="white":
                link.node2.color="gray"
                link.node2.pred = current_node
                link.node2.distance = current_node.distance + 1
                link.node1.pred = current_node
                cue.append(link.node2)
                current_node.children.append(link.node2)
        
        #Remove the black completed node from the cue.        
        cue.remove(current_node)
        

#Function to activate the desired number of "students" based on proximity to the
#intially activated node, and then number of children.  
def spread_limit(desired_activation_number, activated_nodes, nodes):
    
    #Find the largest distance that any node is away from the initial activation node,
    #and make it available as a counter
    largest_dist = max(nodes, key = lambda node: node.distance).distance

    #For each value in that max distance, activate nodes at each level farther away
    #from the "activated node", until the desired number of activated nodes is reached.
    for dist in range(largest_dist):
        considered_dist = dist
    
        #Make an array of all the nodes with the specified distance
        considering = [node for node in nodes if considered_dist == node.distance]
        
        #If the number of nodes in the level is less than the desired activation
        #number, then activate the whole level
        if (len(considering)+len(activated_nodes)) < desired_activation_number:
            for node in considering:
                node.activated= True
                activated_nodes.append(node)
        
        #If activating the number of nodes in the level would activate more nodes
        #than desired, search all the nodes for the fewest node connections in the
        #next farthest level. Activate that node, then repeat until the desired
        #number of activated nodes is reached.
        else:
            
            #Find the number of nodes that still need to be activated
            available = desired_activation_number-len(activated_nodes)
    
            #While there are some available, consider nodes for activation.
            while available >= 0:
        
                #Start with the first node in considering list
                current_lowest_node = considering[0]
            
                #Compare the "current lowest's" number of "children" to every
                #other node in the considering list.
                for node in considering:
                    #If the comparison node has fewer "children" make it the
                    #new current_lowest_node
                    if len(node.children) < len(current_lowest_node.children):
                        current_lowest_node = node
                
                #Activate the current lowest node, add it to the activated list,
                #and remove it from consideration.
                current_lowest_node.activated = True
                activated_nodes.append(current_lowest_node)
                considering.remove(current_lowest_node)
                available -= 1    

###########################     
##### RUN THE NETWORK ####
##########################  

#Call the graph creation module and create the network.
network = create_graph_spread_activation.create_network()
nodes = network[0]
links = network[1]

#Initiate an empty activated_nodes list. This will be filled as nodes become
#activated
activated_nodes = []

#Initiate a variable to track whether the network has reached desired activation
#Change this if you want to a greater or smaller number of people
desired_activation_number = 20

#Choose the node that will be the gensis of the activation
start_node = choice(nodes)
start_node.activated = True
activated_nodes.append(start_node)

#Check if the network is smaller than the desired activation number. If not,
#continue the activation process. If so, activate everything and tell the user
#that the size of the network is insufficient. 
if desired_activation_number < len(nodes):
    #Run the function to determine node distances from the "activation node"
    describe_network(network, start_node)

    #Run the function to activate the desired number of nodes.
    spread_limit(desired_activation_number, activated_nodes, nodes)
else:
    for node in nodes:
        node.activated = True
        print "Your network is too small"

#Print the final activation outcome
for node in nodes:
    print node.identifier
    print node.activated
