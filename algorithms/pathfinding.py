"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""

from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable


def bfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.1: Breadth First Search

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()

    # ALGO GOES HERE
    if origin == goal:
        visited_order.append(origin)
        path.append(origin)
        return (path, visited_order)

    queue = PriorityQueue()

    counter = 0
    queue.insert(counter, origin)
    counter += 1

    visited_nodes = Map()
    visited_nodes.insert_kv(origin, True)

    parent_nodes = Map()
    parent_nodes.insert_kv(origin, None)

    bfs_complete = False

    while not queue.is_empty():
        cur_node = queue.remove_min()
        visited_order.append(cur_node)

        if cur_node == goal:
            bfs_complete = True
            break

        neighbors = graph.get_neighbours(cur_node)

        for neighbor in neighbors:
            neighbor_id = neighbor.get_id()  # index
            if visited_nodes.find(neighbor_id) is None:
                queue.insert(counter, neighbor_id)
                counter += 1
                visited_nodes.insert_kv(neighbor_id, True)
                parent_nodes.insert_kv(neighbor_id, cur_node)

    if bfs_complete:
        while goal is not None:
            path.append(goal)
            goal = parent_nodes.find(goal)
        # reverse not O(1) :<
        size = path.get_size()
        for i in range(size // 2):
            path[i], path[size - i - 1] = path[size - i - 1], path[i]

    return (path, visited_order)


def dijkstra_traversal(graph: Graph, origin: int) -> DynamicArray:
    """
    Task 2.2: Dijkstra Traversal

    @param: graph
      The *weighted* graph to process (POSW graphs)
    @param: origin
      The ID of the node from which to start traversal.

    @returns: DynamicArray containing Entry types.
      The Entry key is a node identifier, Entry value is the cost of the
      shortest path to this node from the origin.

    NOTE: Dijkstra does not work (by default) on LatticeGraph types.
    This is because there is no inherent weight on an edge of these
    graphs. It should of course work where edge weights are uniform.
    """
    valid_locations = DynamicArray()  # This holds your answers

    # ALGO GOES HERE
    distances = Map()

    visited = Map()

    # init distances to inf + origin to 0
    # could possibly skip
    for node in graph._nodes:
        node_id = node.get_id()
        distances.insert_kv(node_id, float("inf"))
    distances.insert_kv(origin, 0)

    queue = PriorityQueue()
    queue.insert(0, origin)

    while not queue.is_empty():
        curr_node = queue.remove_min()

        if visited.find(curr_node) is not None:
            continue

        visited.insert_kv(curr_node, True)

        dist_curr_node = distances.find(curr_node)
        neighbors = graph.get_neighbours(curr_node)

        for neighbor in neighbors:
            neighbor_node, weight = neighbor

            neighbor_node = neighbor_node.get_id()
            if visited.find(neighbor_node) is not None:
                continue

            dist_neighbor_node = distances.find(neighbor_node)
            new_dist = dist_curr_node + weight

            if new_dist < dist_neighbor_node:
                distances.insert_kv(neighbor_node, new_dist)
                queue.insert(new_dist, neighbor_node)

    for node in graph._nodes:
        node_id = node.get_id()
        dist = distances.find(node_id)
        if dist == float("inf"):
            continue
        entry = Entry(node_id, dist)
        valid_locations.append(entry)

    return valid_locations


def dfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.3: Depth First Search **** COMP7505 ONLY ****
    COMP3506 students can do this for funsies.

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.

    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()

    # ALGO GOES HERE

    # Return the path and the visited nodes list
    return (path, visited_order)
