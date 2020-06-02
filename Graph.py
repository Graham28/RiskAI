"""
Graph ADT from university
"""

class Graph:
    #Implement an undirected unweighted graph.

    def __init__(self):
        """Initialise the empty graph."""
        self.graph = dict()

    # Inspectors
    # ----------

    def has_node(self, node):
        """Return True if the graph contains the node, otherwise False."""
        return node in self.graph

    def has_edge(self, node1, node2):
        """Check if there's an edge between the two nodes.
        Return False if the edge or either node don't exist, otherwise True.
        """
        return self.has_node(node1) and node2 in self.graph[node1]

    def neighbours(self, node):
        """Return the set of neighbours of node.
        Assume the graph has the node.
        """
        assert self.has_node(node)

        # copy the set of neighbours, to prevent clients modifying it directly
        result = set()
        for neighbour in self.graph[node]:
            result.add(neighbour)
        return result

    def nodes(self):
        """Return the set of all nodes in the graph."""
        result = list()
        for node in self.graph:
            result.append(node)
        return result

    def edges(self):
        """Return the set of all edges in the graph.
        An edge is a tuple (node1, node2).
        Only one of (node1, node2) and (node2, node1) is included in the set.
        """
        #result = set()
        result = list()
        for node1 in self.nodes():
            for node2 in self.nodes():
                if self.has_edge(node1, node2):
                    if (node2, node1) not in result:
                        #result.add((node1, node2))
                        result.append([node1,node2])
        return result

    def __eq__(self, other):
        """Implement == to check two graphs have the same nodes and edges."""
        nodes = self.nodes()
        if nodes != other.nodes():
            return False
        for node1 in nodes:
            for node2 in nodes:
                if self.has_edge(node1, node2) != other.has_edge(node1, node2):
                    return False
        return True

    # Breadth-first search
    # --------------------

    def bfs(self, start):
        """Do a breadth-first search of the graph, from the start node.
        Return a list of nodes in visited order, the first being start.
        Assume the start node exists.
        """
        assert self.has_node(start)

        # Initialise the list to be returned.
        visited = []
        # Keep the nodes yet to visit in another list, used as a queue.
        # Initially, only the start node is to be visited.
        to_visit = [start]
        # While there are nodes to be visited:
        while to_visit != []:
            # Visit the next node at the front of the queue.
            next_node = to_visit.pop(0)
            visited.append(next_node)
            # Look at its neighbours.
            for neighbour in self.neighbours(next_node):
                # Add node to the back of the queue if not already
                # visited or not already in the queue to be visited.
                if neighbour not in visited and neighbour not in to_visit:
                    to_visit.append(neighbour)
        return visited

    # Depth-first search
    # ------------------

    def dfs(self, start):
        """Do a depth-first search of the graph, from the start node.
        Return a list of nodes in visited order, the first being start.
        Assume the start node exists.
        """
        assert self.has_node(start)

        # Use the BFS algorithm, but keep nodes to visit in a stack.
        visited = []
        to_visit = [start]
        while to_visit != []:
            next_node = to_visit.pop()
            visited.append(next_node)
            for neighbour in self.neighbours(next_node):
                if neighbour not in visited and neighbour not in to_visit:
                    to_visit.append(neighbour)
        return visited


    # Modifiers
    # ---------

    def add_node(self, node):
        """Add the node to the graph.
        Do nothing if the graph already has the node.
        Assume the node is of an immutable type.
        """
        if not self.has_node(node):
            self.graph[node] = set()

    def add_edge(self, node1, node2):
        """Add to the graph an edge between the two nodes.
        Add any node that doesn't exist.
        Assume the two nodes are different and of an immutable type.
        """
        assert node1 != node2

        #self.add_node(node1)
        #self.add_node(node2)
        self.graph[node1].add(node2)
        self.graph[node2].add(node1)
