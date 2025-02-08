"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

NOTE: This file is not used for assessment. It is just a driver program for
you to write your own test cases and execute them against your data structures.
"""

# Import helper libraries
import random
import sys
import time
import argparse

# Import our structures
from structures.entry import Entry, Compound, Offer
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
from structures.bit_vector import BitVector
from structures.graph import Graph, LatticeGraph, Node
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable

from algorithms.problems import (
    maybe_maybe_maybe,
    dora,
    chain_reaction,
    labyrinth,
    constructable,
)


def test_maybe():
    """
    A simple set of tests for the 3xmaybe problem.
    This is not marked and is just here for you to test your code.
    """
    print("=== Maybe Maybe Maybe ===")
    # 0. Set some params; you can tweak these later.
    K = 17  # 17-mers
    DB_SIZE = 100_000_0  # 100k DB entries
    Q_SIZE = 500_00  # 1000 queries

    # 1. Generate a 'database' with some k-mers
    kmer_db = [
        "".join(random.choice("ACGT") for _ in range(K))
        for i in range(DB_SIZE)
    ]

    # 2. Generate a set of query k-mers. We could generate these randomly, but
    # here we might like to sample from the db to ensure the k-mers we're
    # looking for actually exist; we can test "negative" queries later...
    query_sample = random.sample(kmer_db, Q_SIZE)

    negative_queries = [
        "".join(random.choice("ACGT") for _ in range(K)) for i in range(Q_SIZE)
    ]
    query_sample.extend(negative_queries)

    # Now you need to issue the queries. The testing is up to you from here,
    # because there are many ways to solve this problem. However, there are
    # some definite hints on how to solve this in the spec.
    output = maybe_maybe_maybe(kmer_db, query_sample)

    missing_queries = 0
    for query in query_sample[
        :Q_SIZE
    ]:  # First Q_SIZE queries are guaranteed to exist
        if query not in output:
            missing_queries += 1

    false_positives = 0
    for query in negative_queries:
        if query in output:
            false_positives += 1

    print(f"Missing positive queries: {missing_queries}")
    print(f"Potential false positives: {false_positives}")

    if missing_queries == 0:
        print("All positive queries found!")
    else:
        print(f"{missing_queries} positive queries were not found.")

    print("All tests passed!")

    return


def test_dora(graph: Graph):
    """
    A simple set of tests for the Dora problem.
    This is not marked and is just here for you to test your code.
    """
    print("=== Dora ===")
    time1 = time.time()
    print("Generating a random label for each vertex in G.")
    graph.generate_labels()
    # You may prefer to fix the starting vertex instead of picking a random one
    start = graph.generate_random_node_id()

    # You can now run Dora from start across graph.
    # You will also need to set up a sequence to encode. The sequence should
    # be drawn from the symbols in the reachable component of G from the
    # given start node. Look at Figure 8 in the spec.
    sequence = ""

    codeword, codebook = dora(graph, start, sequence)

    nodes = [
        Node(0, 'A'),  # Node 0 - A
        Node(1, 'A'),  # Node 1 - A
        Node(2, 'C'),  # Node 2 - C (starting node v)
        Node(3, 'D'),  # Node 3 - D
        Node(4, 'A'),  # Node 4 - A
        Node(5, 'D'),  # Node 5 - D
        Node(6, 'K'),  # Node 6 - K
        Node(7, 'C')   # Node 7 - C
    ]

    # Create edges (undirected graph as seen in the image)
    edges = [
        [(1, 1), (2, 1)],    # Node 0 (A) is connected to 1 (A) and 2 (C)
        [(0, 1), (3, 1), (4, 1)],  # Node 1 (A) is connected to 0 (A), 3 (D), 4 (A)
        [(0, 1), (6, 1)],    # Node 2 (C) is connected to 0 (A) and 6 (K)
        [(1, 1), (5, 1)],    # Node 3 (D) is connected to 1 (A) and 5 (D)
        [(1, 1)],            # Node 4 (A) is connected to 1 (A)
        [(3, 1), (6, 1)],    # Node 5 (D) is connected to 3 (D) and 6 (K)
        [(2, 1), (5, 1), (7, 1)],  # Node 6 (K) is connected to 2 (C), 5 (D), 7 (C)
        [(6, 1)]             # Node 7 (C) is connected to 6 (K)
    ]
    # Build the graph
    graph = Graph(nodes, edges, weighted=False)
    # Starting node is 0 (A)
    start = 2
    # Sequence to encode, taken from symbols present in the graph
    symbol_sequence = "DCAKC"
    # Run Dora's function
    encoded_sequence, codebook = dora(graph, start, symbol_sequence)

    # Output results
    print("Encoded Sequence (BitVector):", encoded_sequence)
    print("Codebook (symbol -> code):")
    for entry in codebook:
        print(f"{entry.get_key()} -> {entry.get_value()}")
    time2 = time.time()



    print("Time taken:", time2 - time1)
    print("Test passed!")


def test_chain_reaction():
    """
    A simple set of tests for the Chain Reaction problem.
    This is not marked and is just here for you to test your code.
    """
    print("=== Chain Reaction ===")

    # Set up some params
    # x dim is 100
    MIN_X = 0
    MAX_X = 100
    # y dim is 100
    MIN_Y = 0
    MAX_Y = 100
    # minimum radius is 1, max is 25
    MIN_R = 1
    MAX_R = 25
    # maximum compound count
    COMPOUNDS = 100

    # compounds = []
    # locations = set() # ensure we do not duplicate x/y coords
    # for cid in range(COMPOUNDS):
    #     x = random.randint(MIN_X, MAX_X)
    #     y = random.randint(MIN_Y, MAX_Y)
    #     r = random.randint(MIN_R, MAX_R)
    #     xy_key = str(x) + "_" + str(y)
    #     if xy_key not in locations:
    #         compounds.append(Compound(x, y, r, cid))
    #         locations.add(xy_key)

    # print ("Generated", len(compounds), "compounds.")
    # #for compound in compounds:
    # #    print(str(compound))

    # # You can now run and test your algorithm
    # trigger_compound  = chain_reaction(compounds)

    # Test Case 2: No Overlapping Compounds
    compounds = [
        Compound(0, 0, 1, 3),
        Compound(100, 100, 1, 1),
        Compound(200, 200, 1, 2),
    ]
    print("\nTest 2: No Overlapping Compounds")
    trigger_compound = chain_reaction(compounds)
    print(f"Best compound to trigger: {trigger_compound} (Expected: 1)")

    # Test Case 3: All Overlapping Compounds
    compounds = [
        Compound(10, 10, 100, 0),
        Compound(20, 20, 100, 1),
        Compound(30, 30, 100, 2),
    ]
    print("\nTest 3: All Overlapping Compounds")
    trigger_compound = chain_reaction(compounds)
    print(f"Best compound to trigger: {trigger_compound} (Expected: 0)")

    # Test Case 4: Edge Case - Single Compound
    compounds = [Compound(50, 50, 10, 0)]
    print("\nTest 4: Single Compound")
    trigger_compound = chain_reaction(compounds)
    print(f"Best compound to trigger: {trigger_compound} (Expected: 0)")

    # Test Case 5: Edge Case - Two Compounds, One Overlaps
    compounds = [
        Compound(10, 10, 50, 1),
        Compound(60, 60, 20, 2),
    ]
    print("\nTest 5: Two Compounds, One Overlaps")
    trigger_compound = chain_reaction(compounds)
    print(f"Best compound to trigger: {trigger_compound} (Expected: 1)")

    compounds = [
        Compound(1, 2, 1.75, 1),  # Compound 1 at (1, 2) with radius 2.5
        Compound(2, 1, 0.5, 2),  # Compound 2 at (1, 4) with radius 1.5
        Compound(2, 4, 2.4, 3),  # Compound 3 at (3, 2) with radius 3
        Compound(4, 5, 1.2, 4),  # Compound 4 at (5, 4) with radius 2
        Compound(4, 2, 1.75, 5),  # Compound 5 at (6, 1) with radius 1.5
        Compound(5, 5, 1.2, 6),  # Compound 6 at (6, 5) with radius 2.5
    ]

    result = chain_reaction(compounds)
    print("Test result should be 3:", result)

    # The expected output based on the image is compound with ID 3
    expected = 3
    # assert result == expected, f"Expected {expected}, but got {result}"

    # Test Case 6: Exhaustive, 1000 Compounds
    COMPOUNDS = 100
    compounds = []
    locations = set()
    for cid in range(COMPOUNDS):
        x = random.randint(MIN_X, MAX_X)
        y = random.randint(MIN_Y, MAX_Y)
        r = random.uniform(MIN_R, MAX_R)
        xy_key = f"{x}_{y}"
        if xy_key not in locations:
            compounds.append(Compound(x, y, r, cid))
            locations.add(xy_key)

    print(f"\nTest 6: Exhaustive Test with {COMPOUNDS} Compounds")
    trigger_compound = chain_reaction(compounds)
    print(f"Best compound to trigger: {trigger_compound}")


def test_labyrinth():
    """
    A simple set of tests for the Labyrinth problem.
    This is not marked and is just here for you to test your code.
    """
    print("=== Labyrinth ===")

    # Set up some params - you should mess with these
    # nodes, n = |V|
    MIN_N = 10
    MAX_N = 10000
    # edges, m = |E|
    MIN_M = 1
    MAX_M = 50000
    # Diameter
    MIN_K = 0
    MAX_K = 1000
    # Cost
    MIN_C = 1
    MAX_C = 10000
    # How many?
    OFFERS =10_000

    offers = []
    for oid in range(OFFERS):
        n = random.randint(MIN_N, MAX_N)
        m = random.randint(MIN_M, MAX_M)
        k = random.randint(MIN_K, MAX_K)
        c = random.randint(MIN_C, MAX_C)
        offers.append(Offer(n, m, k, c, oid))
        if constructable(n, m, k) and c == 9:
            print(f"Offer {oid}: {n} nodes, {m} edges, diameter {k}, cost {c}")

    print("Generated", len(offers), "offers.")
    # for offer in offers:
    #    print(str(offer))
    # You can now run and test your algorithm
    best_offer, cost = labyrinth(offers)
    print(f"Best offer: {best_offer} with cost {cost}")

    # Case 1: Simple valid case (small graph)
    offers = [
        Offer(3, 2, 2, 200, 1),  # Valid graph
        Offer(3, 2, 2, 150, 2),  # Same structure, higher cost
    ]
    expected_offer = 2  # Cheapest valid offer
    expected_cost = 150
    best_offer, cost = labyrinth(offers)
    print(
        f"Test Case 1: Expected: (Offer ID: {expected_offer}, Cost: {expected_cost}), Actual: (Offer ID: {best_offer}, Cost: {cost})"
    )

    # Case 2: Invalid graph due to too few edges (disconnected)
    offers = [
        Offer(4, 2, 3, 50, 1),  # Invalid, disconnected
        Offer(4, 3, 2, 75, 2),  # Valid
    ]
    expected_offer = 2
    expected_cost = 75
    best_offer, cost = labyrinth(offers)
    print(
        f"Test Case 2: Expected: (Offer ID: {expected_offer}, Cost: {expected_cost}), Actual: (Offer ID: {best_offer}, Cost: {cost})"
    )

    # Case 3: Valid and invalid graphs with different diameters
    offers = [
        Offer(5, 4, 4, 100, 1),  # Valid, but longer diameter
        Offer(5, 5, 2, 120, 2),  # Valid, smaller diameter
    ]
    expected_offer = 1  # Cheaper one should win despite longer diameter
    expected_cost = 100
    best_offer, cost = labyrinth(offers)
    print(
        f"Test Case 3: Expected: (Offer ID: {expected_offer}, Cost: {expected_cost}), Actual: (Offer ID: {best_offer}, Cost: {cost})"
    )

    # Case 4: Two graphs with the same cost but different diameters
    offers = [
        Offer(5, 4, 4, 100, 2),  # Valid with diameter 3
        Offer(5, 5, 5, 100, 1),  # Valid, same cost, smaller diameter
    ]
    expected_offer = 1  # Same cost, smaller diameter wins
    expected_cost = 100
    best_offer, cost = labyrinth(offers)
    print(
        f"Test Case 4: Expected: (Offer ID: {expected_offer}, Cost: {expected_cost}), Actual: (Offer ID: {best_offer}, Cost: {cost})"
    )

    # Case 5: Large valid graph with many nodes and edges
    offers = [
        Offer(1000, 999, 500, 5000, 1),  # Valid large graph
        Offer(1000, 999, 500, 4500, 2),  # Cheaper valid graph
    ]
    expected_offer = 2  # Cheaper one should win
    expected_cost = 4500
    best_offer, cost = labyrinth(offers)
    print(
        f"Test Case 5: Expected: (Offer ID: {expected_offer}, Cost: {expected_cost}), Actual: (Offer ID: {best_offer}, Cost: {cost})"
    )

    # Case 6: Graph with maximum nodes but invalid due to too many edges
    offers = [
        Offer(100, 5050, 10, 500, 1),  # Invalid, too many edges
        Offer(100, 4950, 10, 550, 2),  # Valid
    ]
    expected_offer = 2  # The valid one wins
    expected_cost = 550
    best_offer, cost = labyrinth(offers)
    print(
        f"Test Case 6: Expected: (Offer ID: {expected_offer}, Cost: {expected_cost}), Actual: (Offer ID: {best_offer}, Cost: {cost})"
    )

    # Case 7: Edge case with only 2 nodes and 1 edge
    offers = [
        Offer(2, 1, 1, 100, 3),  # Smallest valid graph possible
    ]
    expected_offer = 3  # Only one offer, so this should be chosen
    expected_cost = 100
    best_offer, cost = labyrinth(offers)
    print(
        f"Test Case 7: Expected: (Offer ID: {expected_offer}, Cost: {expected_cost}), Actual: (Offer ID: {best_offer}, Cost: {cost})"
    )

    # Case 8: Multiple offers with ties in cost
    offers = [
        Offer(5, 4, 2, 100, 1),  # Valid offer with cost 100
        Offer(5, 4, 2, 100, 2),  # Same cost, different ID
        Offer(5, 4, 3, 100, 3),  # Same cost, larger diameter
    ]
    expected_offer = 1  # First one (smallest ID) should be chosen
    expected_cost = 100
    best_offer, cost = labyrinth(offers)
    print(
        f"Test Case 8: Expected: (Offer ID: {expected_offer}, Cost: {expected_cost}), Actual: (Offer ID: {best_offer}, Cost: {cost})"
    )

    offers = [
        Offer(3, 2, 1, 100, 0),  # Valid
        Offer(3, 1, 1, 120, 1),  # Invalid (not enough edges)
        Offer(4, 3, 1, 90, 2),  # Valid, cheaper
        Offer(4, 6, 1, 110, 3),  # Invalid (too many edges)
        Offer(5, 4, 2, 200, 4),  # Valid
        Offer(6, 5, 2, 250, 5),  # Valid
        Offer(7, 6, 3, 150, 6),  # Valid
        Offer(8, 10, 3, 300, 7),  # Invalid (too many edges)
        Offer(9, 8, 3, 180, 8),  # Valid
        Offer(10, 9, 3, 220, 9),  # Valid
        Offer(11, 12, 4, 400, 10),  # Valid
        Offer(12, 13, 4, 360, 11),  # Valid
        Offer(13, 14, 5, 410, 12),  # Valid
        Offer(14, 10, 3, 290, 13),  # Valid
        Offer(15, 15, 5, 330, 14),  # Valid
        Offer(16, 14, 4, 350, 15),  # Valid
        Offer(17, 16, 6, 500, 16),  # Valid
        Offer(18, 16, 5, 550, 17),  # Valid
        Offer(19, 18, 7, 620, 18),  # Valid
        Offer(20, 20, 8, 700, 19),  # Valid
    ]
    expected = (2, 90)  # Offer 2 is valid and the cheapest
    actual = labyrinth(offers)
    print(
        f"Test 1 - Expected: {expected}, Actual: {actual}, Pass: {expected == actual}"
    )

    # Test 2: 30 offers with a mix of valid and invalid offers
    offers = [
        Offer(10, 9, 3, 500, 0),  # Valid
        Offer(10, 9, 3, 400, 1),  # Invalid (too few edges)
        Offer(11, 10, 3, 480, 2),  # Valid
        Offer(11, 12, 4, 600, 3),  # Valid
        Offer(12, 11, 5, 700, 4),  # Valid
        Offer(12, 15, 4, 650, 5),
        Offer(15, 14, 4, 800, 6),  # Valid
        Offer(15, 14, 5, 750, 7),  # Valid
        Offer(16, 13, 6, 900, 8),  # Valid
        Offer(16, 14, 7, 1000, 9),  # Valid
        Offer(17, 15, 6, 850, 10),  # Valid
        Offer(17, 14, 5, 820, 11),  # Valid
        Offer(18, 17, 6, 950, 12),  # Valid
        Offer(18, 18, 8, 980, 13),  # Valid
        Offer(19, 16, 7, 1020, 14),  # Valid
        Offer(20, 19, 7, 1050, 15),  # Valid
        Offer(21, 20, 8, 1100, 16),  # Valid
        Offer(22, 21, 9, 1150, 17),  # Valid
        Offer(23, 22, 9, 1200, 18),  # Valid
        Offer(24, 23, 10, 1250, 19),  # Valid
        Offer(25, 24, 10, 1300, 20),  # Valid
        Offer(26, 25, 11, 1350, 21),  # Valid
        Offer(27, 26, 12, 1400, 22),  # Valid
        Offer(28, 27, 12, 1450, 23),  # Valid
        Offer(29, 28, 13, 1500, 24),  # Valid
        Offer(30, 29, 14, 1550, 25),  # Valid
        Offer(30, 30, 15, 1600, 26),  # Valid
        Offer(31, 31, 15, 1650, 27),  # Valid
        Offer(32, 32, 16, 1700, 28),  # Valid
        Offer(33, 33, 16, 1750, 29),  # Valid
    ]
    expected = (1, 400)  # Offer 1 is valid and the cheapest
    actual = labyrinth(offers)
    print(
        f"Test 2 - Expected: {expected}, Actual: {actual}, Pass: {expected == actual}"
    )

    # Test 3: All offers invalid due to insufficient edges
    offers = [
        Offer(10, 5, 3, 500, 0),  # Invalid (too few edges)
        Offer(11, 6, 4, 600, 1),  # Invalid (too few edges)
        Offer(12, 7, 5, 700, 2),  # Invalid (too few edges)
        Offer(13, 8, 6, 800, 3),  # Invalid (too few edges)
        Offer(14, 9, 7, 900, 4),  # Invalid (too few edges)
    ]
    expected = (-1, float("inf"))  # No valid offers
    actual = labyrinth(offers)
    print(
        f"Test 3 - Expected: {expected}, Actual: {actual}, Pass: {expected == actual}"
    )

    # Test 4: All offers valid, pick cheapest
    offers = [
        Offer(10, 9, 3, 500, 0),  # Valid
        Offer(11, 10, 4, 600, 1),  # Valid
        Offer(12, 11, 5, 700, 2),  # Valid
        Offer(13, 12, 6, 800, 3),  # Valid
        Offer(14, 13, 7, 400, 4),  # Valid and cheapest
    ]
    expected = (4, 400)  # Offer 4 is the cheapest
    actual = labyrinth(offers)
    print(
        f"Test 4 - Expected: {expected}, Actual: {actual}, Pass: {expected == actual}"
    )

    # Test 5: Complex case with varying diameters and costs
    offers = [
        Offer(10, 9, 2, 800, 0),  # Valid
        Offer(10, 9, 3, 750, 1),  # Valid and cheaper
        Offer(11, 10, 3, 740, 2),  # Valid and cheaper
        Offer(11, 10, 2, 850, 3),  # Valid
        Offer(12, 11, 3, 720, 4),  # Valid and cheapest
    ]
    expected = (4, 720)  # Offer 4 is valid and cheapest
    actual = labyrinth(offers)
    print(
        f"Test 5 - Expected: {expected}, Actual: {actual}, Pass: {expected == actual}"
    )
    # Case 1: Valid single node labyrinth
    offer1 = Offer(1, 0, 0, 100, 1)  # 1 node, 0 edges, 0 diameter, cost 100
    offer2 = Offer(1, 0, 0, 200, 2)  # 1 node, 0 edges, 0 diameter, cost 200
    offers = [offer1, offer2]
    assert labyrinth(offers) == (1, 100)  # offer 1 is the cheapest valid

    # Case 2: Invalid graph (not connected)
    offer3 = Offer(
        5, 3, 10, 1000, 3
    )  # 5 nodes, 3 edges, diameter 10 (invalid, not enough edges)
    offer4 = Offer(5, 5, 3, 500, 4)  # 5 nodes, 5 edges, diameter 3 (valid)
    offers = [offer3, offer4]
    assert labyrinth(offers) == (
        4,
        500,
    )  # offer 4 is valid and has lowest cost

    # Case 3: Valid graph but more expensive
    offer5 = Offer(10, 10, 8, 1000, 5)  # 10 nodes, 10 edges, diameter 8
    offer6 = Offer(
        10, 15, 8, 800, 6
    )  # 10 nodes, 15 edges, diameter 8 (valid and cheaper)
    offers = [offer5, offer6]
    assert labyrinth(offers) == (6, 800)  # offer 6 is cheaper

    # Case 4: Invalid diameter
    offer7 = Offer(
        10, 9, 11, 600, 7
    )  # 10 nodes, 9 edges, diameter 11 (invalid, diameter too large)
    offer8 = Offer(10, 9, 8, 700, 8)  # 10 nodes, 9 edges, diameter 8 (valid)
    offers = [offer7, offer8]
    assert labyrinth(offers) == (7, 600)  # offer 8 is valid

    # Case 5: Large graph, many nodes and edges
    offer9 = Offer(
        1000, 999, 500, 10000, 9
    )  # 1000 nodes, 999 edges, valid diameter
    offer10 = Offer(
        1000, 1000, 999, 9500, 10
    )  # 1000 nodes, 1000 edges, valid diameter, cheaper
    offers = [offer9, offer10]
    assert labyrinth(offers) == (10, 9500)  # offer 10 is valid and cheaper

    print("All test cases passed!")


# The actual program we're running here
if __name__ == "__main__":
    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(
        description="COMP3506/7505 Assignment Two: Testing Problems"
    )

    parser.add_argument(
        "--maybe", action="store_true", help="Test your Maybex3 solution."
    )
    parser.add_argument("--dora", type=str, help="Test your Dora solution.")
    parser.add_argument(
        "--chain",
        action="store_true",
        help="Test your Chain Reaction solution.",
    )
    parser.add_argument(
        "--labyrinth",
        action="store_true",
        help="Test your Labyrinth solution.",
    )
    parser.add_argument(
        "--seed", type=int, default="42", help="Seed the PRNG."
    )
    args = parser.parse_args()

    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # Seed the PRNG in case you are using randomness
    random.seed(args.seed)

    # Now check/run the selected algorithm
    if args.maybe:
        test_maybe()

    if args.dora:
        in_graph = Graph()
        in_graph.from_file(args.dora)
        test_dora(in_graph)

    if args.chain:
        test_chain_reaction()

    if args.labyrinth:
        test_labyrinth()
