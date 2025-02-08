"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

 Each problem will be assessed on three sets of tests:

1. "It works":
       Basic inputs and outputs, including the ones peovided as examples, with generous time and memory restrictions.
       Large inputs will not be tested here.
       The most straightforward approach will likely fit into these restrictions.

2. "Exhaustive":
       Extensive testing on a wide range of inputs and outputs with tight time and memory restrictions.
       These tests won't accept brute force solutions, you'll have to apply some algorithms and optimisations.

 3. "Welcome to COMP3506":
       Extensive testing with the tightest possible time and memory restrictions
       leaving no room for redundant operations.
       Every possible corner case will be assessed here as well.

There will be hidden tests in each category that will be published only after the assignment deadline.

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""

from structures.entry import Entry, Compound, Offer
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
from structures.bit_vector import BitVector
from structures.graph import Node, Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable


def maybe_maybe_maybe(database: list[str], query: list[str]) -> list[str]:
    """
    Task 3.1: Maybe Maybe Maybe

    @database@ is an array of k-mers in our database.
    @query@ is an array of k-mers we want to search for.

    Return a list of query k-mers that are *likely* to appear in the database.

    Limitations:
        "It works":
            @database@ contains up to 1000 elements;
            @query@ contains up to 1000 elements.

        "Exhaustive":
            @database@ contains up to 100'000 elements;
            @query@ contains up to 100'000 elements.

        "Welcome to COMP3506":
            @database@ contains up to 1'000'000 elements;
            @query@ contains up to 500'000 elements.

    Each test will run over three false positive rates. These rates are:
        fp_rate = 10%
        fp_rate = 5%
        fp_rate = 1%.

    You must pass each test in the given time limit and be under the given
    fp_rate to get the associated mark for that test.
    """
    answer = []

    # DO THE THING

    # import time
    # start_time = time.time()

    # -----bloom filter------
    # kmers_bf = BloomFilter(len(database))
    # for kmer in database:
    #     kmers_bf.insert(kmer)

    # for kmer in query:
    #     if kmers_bf.contains(kmer):
    #         answer.append(kmer)

    # mid_time = time.time()
    # elapsed_time = mid_time - start_time
    # print(f"Time Bloom: {elapsed_time:.6f} seconds")

    # -----map-------
    kmers_map = Map(my_cap=len(database))
    for kmer in query:
        kmers_map.insert_kv(kmer, 1)

    for kmer in database:
        if kmers_map.find(kmer):
            answer.append(kmer)

    # end_time = time.time()
    # elapsed_time = end_time - mid_time
    # print(f"Time Map: {elapsed_time:.6f} seconds")

    return answer


def dora(
    graph: Graph,
    start: int,
    symbol_sequence: str,
) -> tuple[BitVector, list[Entry]]:
    """
    Task 3.2: Dora and the Chin Bicken

    @graph@ is the input graph G; G might be disconnected; each node contains
    a single symbol in the node's data field.
    @start@ is the integer identifier of the start vertex.
    @symbol_sequence@ is the input sequence of symbols, L, with length n.
    All symbols are guaranteed to be found in G.

    Return a BitVector encoding symbol_sequence via a minimum redundancy code.
    The BitVector should be read from index 0 upwards (so, the first symbol is
    encoded from index 0). You also need to return your codebook as a
    Python list of unique Entries. The Entry key should correspond to the
    symbol, and the value should be a string. More information below.

    Limitations:
        "It works":
            @graph@ has up to 1000 vertices and up to 1000 edges.
            the alphabet consists of up to 26 characters.
            @symbol_sequence@ has up to 1000 characters.

        "Exhaustive":
            @graph@ has up to 100'000 vertices and up to 100'000 edges.
            the alphabet consists of up to 1000 characters.
            @symbol_sequence@ has up to 100'000 characters.

        "Welcome to COMP3506":
            @graph@ has up to 1'000'000 vertices and up to 1'000'000 edges.
            the alphabet consists of up to 300'000 characters.
            @symbol_sequence@ has up to 1'000'000 characters.

    """
    coded_sequence = BitVector()

    """
    list of Entry objects, each entry has key=symbol, value=str. The str
    value is just an ASCII representation of the bits used to encode the
    given key. For example: x = Entry("c", "1101")
    """
    codebook = []
    symbol_char = ""

    # DO THE THING
    gene_freq = Map(my_cap=1753127)
    visited = Map(my_cap=1753127)

    # queue = PriorityQueue()
    # queue.insert_fifo(start)

    # while not queue.is_empty():
    #     cur_node = queue.remove_min()

    #     if visited.find(cur_node) is not None:
    #         continue

    #     visited.insert_kv(cur_node, True)
    #     symbol = graph.get_node(cur_node).get_data()

    #     if gene_freq.find(symbol) is None:
    #         gene_freq.insert_kv(symbol, 1)
    #         symbol_char = symbol_char + symbol
    #     else:
    #         gene_freq.insert_kv(symbol, gene_freq.find(symbol) + 1)

    #     neighbors = graph.get_neighbours(cur_node)
    #     for neighbor in neighbors:
    #         neighbor_id = neighbor.get_id()
    #         if visited.find(neighbor_id) is None:
    #             queue.insert_fifo(neighbor_id)

    queue = DoublyLinkedList()
    queue.insert_to_back(start)

    while not queue.get_size() == 0:
        cur_node = queue.remove_from_front()

        # if graph.get_node(cur_node).get_seen():
        #    continue

        # graph.get_node(cur_node).set_seen(True)
        if visited.find(cur_node) is not None:
            continue

        visited.insert_kv(cur_node, 1)
        symbol = graph.get_node(cur_node).get_data()

        if gene_freq.find(symbol) is None:
            gene_freq.insert_kv(symbol, 1)
            symbol_char = symbol_char + symbol
        else:
            gene_freq.insert_kv(symbol, gene_freq.find(symbol) + 1)

        neighbors = graph.get_neighbours(cur_node)
        for neighbor in neighbors:
            neighbor_id = neighbor.get_id()
            if visited.find(neighbor_id) is None:
            # if not graph.get_node(neighbor_id).get_seen():
                queue.insert_to_back(neighbor_id)

    # huffman coding
    huffman_tree = make_huffman_tree(gene_freq, symbol_char)

    # make codes
    huffman_codes_map = Map(my_cap=1753127)
    generate_huffman_codes(huffman_tree, "", huffman_codes_map, codebook)

    for symbol in symbol_sequence:
        code = huffman_codes_map.find(symbol)
        if code is not None:
            for bit in code:
                coded_sequence.append(int(bit))

    return (coded_sequence, codebook)


def generate_huffman_codes(node: Entry, current_code: str, huffman_codes: Map, codebook: list[Entry]) -> None:
    # if node.get_key() is not None and node.get_key() != "$":
    #     huffman_codes.insert_kv(node.get_key(), current_code)
    #     codebook.append(Entry(node.get_key(), current_code))
    #     return

    # if node.left is not None:
    #     generate_huffman_codes(node.left, current_code + "0", huffman_codes, codebook)
    # if node.right is not None:
    #     generate_huffman_codes(node.right, current_code + "1", huffman_codes, codebook)

    stack = [(node, "")]

    while stack:
        cur_node, cur_code = stack.pop()
        if cur_node.get_key() is not None and cur_node.get_key() != "$":
            huffman_codes.insert_kv(cur_node.get_key(), cur_code)
            codebook.append(Entry(cur_node.get_key(), cur_code))
        else:
            if cur_node.right is not None:
                stack.append((cur_node.right, cur_code + "1"))
            if cur_node.left is not None:
                stack.append((cur_node.left, cur_code + "0"))


def make_huffman_tree(gene_freq: Map, symbol_char: str) -> Entry:
    tree_q = PriorityQueue()
    for symbol in symbol_char:
        freq = gene_freq.find(symbol)
        tree_q.insert(freq, Entry(symbol, freq))

    # Potentially slow, might need to like merge build type thing
    while tree_q.get_size() > 1:
        left = tree_q.remove_min()
        right = tree_q.remove_min()

        combined_node = Entry("$", left.get_value() + right.get_value())
        combined_node.left = left
        combined_node.right = right

        tree_q.insert(combined_node.get_value(), combined_node)

    return tree_q.remove_min()

    # left = tree_q.remove_min()
    # right = tree_q.remove_min()
    # while tree_q.get_size() > 0:
    #     new_node = Entry("$", 0)
    #     new_node.left = left
    #     new_node.right = right
    #     right = new_node
    #     left = tree_q.remove_min()

    # new_node = Entry("$", 0)
    # new_node.left = left
    # new_node.right = right
    # right = new_node
    # left = tree_q.remove_min()

    # return right


def chain_reaction(compounds: list[Compound]) -> int:
    """
    Task 3.3: Chain Reaction

    @compounds@ is a list of Compound types, see structures/entry.py for the
    definition of a Compound. In short, a Compound has an integer x and y
    coordinate, a floating point radius, and a unique integer representing
    the compound identifier.

    Return the compound identifier of the compound that will yield the
    maximal number of compounds in the chain reaction if set off. If there
    are ties, return the one with the smallest identifier.

    Limitations:
        "It works":
            @compounds@ has up to 10 elements

        "Exhaustive":
            @compounds@ has up to 50 elements

        "Welcome to COMP3506":
            @compounds@ has up to 100 elements

    """
    maximal_compound = -1
    explosive_compound = -1
    # DO THE THING

    # ----Easy, duplicate looks-----
    # ----doesnt acctually look for reactions reaction----
    # for i in range(len(compounds)):
    #     count = 0
    #     for j in range(len(compounds)):
    #         if i != j and reaction_range(compounds[i], compounds[j]):
    #             count += 1
    #     if count > maximal_compound:
    #         maximal_compound = count
    #         explosive_compound = compounds[i].get_compound_id()
    #     elif count == maximal_compound and compounds[i].get_compound_id() < explosive_compound:
    #             explosive_compound = compounds[i].get_compound_id()

    # maximal_compound = -1
    # explosive_compound = -1

    trigger_count = Map()
    adjacency_list = Map()

    build_adjacency_list(compounds, adjacency_list)

    for i in range(len(compounds)):
        if trigger_count.find(i) is None:
            triggered_num = chain_bfs(i, adjacency_list, trigger_count)
        else:
            triggered_num = trigger_count.find(i)
        compound_id = compounds[i].get_compound_id()
        if triggered_num > maximal_compound:
            maximal_compound = triggered_num
            explosive_compound = compound_id
        elif (
            triggered_num == maximal_compound
            and compound_id < explosive_compound
        ):
            explosive_compound = compound_id

    return explosive_compound


def build_adjacency_list(
    compounds: list[Compound], adjacency_list: Map
) -> Map:
    for i in range(len(compounds)):
        adjacency_list.insert_kv(i, [])
    for i in range(len(compounds)):
        compound_i = compounds[i]
        for j in range(len(compounds)):
            if i == j:
                continue
            compound_j = compounds[j]
            if reaction_range(compound_i, compound_j):
                neighbors = adjacency_list.find(i)
                neighbors.append(j)
                adjacency_list.insert_kv(i, neighbors)
    return adjacency_list


def chain_bfs(start: int, adjacency_list: dict, trigger_count: Map) -> int:
    # queue = PriorityQueue()
    queue = DoublyLinkedList()
    queue.insert_to_back(start)
    # queue.insert_fifo(start)
    visited = Map()
    visited.insert_kv(start, True)
    count = 0

    # while not queue.is_empty():
    while queue.get_size() != 0:
        origin = queue.remove_from_front()
        # origin = queue.remove_min()
        count += 1
        for neighbor in adjacency_list[origin]:
            if visited.find(neighbor) is None:
                visited.insert_kv(neighbor, True)
                queue.insert_to_back(neighbor)
                # queue.insert_fifo(neighbor)
    trigger_count.insert_kv(start, count)
    return count


def reaction_range(compound_one: Compound, compound_two: Compound) -> bool:
    x1, y1 = compound_one.get_coordinates()
    x2, y2 = compound_two.get_coordinates()
    r1 = compound_one.get_radius()
    distance_squared = (x1 - x2) ** 2 + (y1 - y2) ** 2
    return distance_squared <= r1**2


def labyrinth(offers: list[Offer]) -> tuple[int, int]:
    """
    Task 3.4: Labyrinth

    @offers@ is a list of Offer types, see structures/entry.py for the
    definition of an Offer. In short, an Offer stores n (number of nodes),
    m (number of edges), and k (diameter) of the given Labyrinth. Each
    Offer also has an associated cost, and a unique offer identifier.

    Return the offer identifier and the associated cost for the cheapest
    labyrinth that can be constructed from the list of offers. If there
    are ties, return the one with the smallest identifier.
    You are guaranteed that all offer ids are distinct.

    Limitations:
        "It works":
            @offers@ contains up to 1000 items.
            0 <= n <= 1000
            0 <= m <= 1000
            0 <= k <= 1000

        "Exhaustive":
            @offers@ contains up to 100'000 items.
            0 <= n <= 10^6
            0 <= m <= 10^6
            0 <= k <= 10^6

        "Welcome to COMP3506":
            @offers@ contains up to 5'000'000 items.
            0 <= n <= 10^42
            0 <= m <= 10^42
            0 <= k <= 10^42

    """
    best_offer_id = -1
    best_offer_cost = float("inf")

    # DO THE THING
    for quote in offers:
        offer_id, cost, nodes, edges, diameter = (
            quote.get_offer_id(),
            quote.get_cost(),
            quote.get_num_nodes(),
            quote.get_num_edges(),
            quote.get_diameter(),
        )
        if constructable(nodes, edges, diameter):
            if cost < best_offer_cost:
                best_offer_cost = cost
                best_offer_id = offer_id
            elif cost == best_offer_cost and offer_id < best_offer_id:
                best_offer_id = offer_id

    return (best_offer_id, best_offer_cost)


def constructable(nodes: int, edges: int, diameter: int) -> bool:
    if nodes <= 0 or edges < 0 or diameter < 0:
        return False

    if nodes == 1 and edges == 0 and diameter >= 0:
        return True

    # 2nodes
    if nodes == 2 and edges == 1 and diameter > 0:
        return True

    if diameter < 2:
        return False

    # connected graph must have at least n-1 edges
    if edges < nodes - 1:
        return False

    # shortest simple path between any two nodes is at most k
    # no double edges or self loops, basically cannot be more than strongly
    # connected
    if edges > nodes * (nodes - 1) // 2:
        return False

    return True