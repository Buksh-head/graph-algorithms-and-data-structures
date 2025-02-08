"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Compression Utilities for Task 4.
"""

from pathlib import Path
from typing import Any
import sys
import hashlib
from structures.entry import Entry, Compound, Offer
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
from structures.bit_vector import BitVector
from structures.graph import Node, Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable

static_encode = {
    'A': '00',
    'C': '01',
    'G': '10',
    'T': '11'
}

reversed_static_encode = {v: k for k, v in static_encode.items()}

def file_to_bytes(path: str) -> bytes:
    """
    Read a file into a byte array
    """
    with open(path, 'rb') as f:
        data = f.read()
    return data

def bytes_to_file(path: str, data: bytes) -> None:
    """
    Write a sequence of bytes to a file
    """
    with open(path, 'wb') as f:
        f.write(data)

def my_compressor(in_bytes: bytes) -> bytes:
    """
    Your compressor takes a bytes object and returns a compressed
    version of the bytes object. We have put xz here just as a 
    baseline general purpose compression tool.
    """
    # Implement me!
    
    content = in_bytes.decode('ascii')
    
    lines = content.splitlines()
    
    header_lines = [line for line in lines if line.startswith('>')]
 
    header = '\n'.join(header_lines) + '\n' 
    
    sequence_lines = [line.strip() for line in lines if not line.startswith('>') and not line.startswith('http')]

    kmer_sequence = ''.join(sequence_lines)
       
    bitstream = ''
    for kmer in kmer_sequence.upper():
        static_encoded = static_encode[kmer]
        bitstream += static_encoded
    
    padding_length = (8 - len(bitstream) % 8) % 8
    bitstream_padded = bitstream + '0' * padding_length
    
    compressed_bytes = bytearray()
    for i in range(0, len(bitstream_padded), 8):
        byte = bitstream_padded[i:i+8]
        compressed_bytes.append(int(byte, 2))
    
    header_bytes = header.encode('ascii')
    
    header_length = len(header_bytes)
    header_length_bytes = header_length.to_bytes(4, byteorder='big')
    
    compressed_data = header_length_bytes + header_bytes + bytes([padding_length]) + bytes(compressed_bytes)
    
    return compressed_data

def my_decompressor(compressed_bytes: bytes) -> bytes:
    """
    Your decompressor is given a compressed bytes object (from your own
    compressor) and must recover and return the original bytes.
    Once again, we've just used xz.
    """ 
    # Implement me!
    header_length = int.from_bytes(compressed_bytes[:4], byteorder='big')
    
    header_bytes = compressed_bytes[4:4 + header_length]
    header = header_bytes.decode('ascii')
    
    padding_length = compressed_bytes[4 + header_length]
    
    compressed_sequence = compressed_bytes[4 + header_length + 1:]
    
    bitstream = ''.join(f'{byte:08b}' for byte in compressed_sequence)
    
    if padding_length > 0:
        bitstream = bitstream[:-padding_length]
    
    sequence = ''
    for i in range(0, len(bitstream), 2):
        bits = bitstream[i:i+2]
        sequence += reversed_static_encode[bits]
    
    decompressed_content = header + '\n'.join([sequence[i:i+70] for i in range(0, len(sequence), 70)]) + '\n\n'
    
    return decompressed_content.encode('ascii')

def compress_file(in_path: str, out_path: str) -> None:
    """
    Consume a file from in_path, compress it, and write it to out_path.
    """
    in_size = Path(in_path).stat().st_size
    in_data = file_to_bytes(in_path)
   
    compressed = my_compressor(in_data)
    
    bytes_to_file(out_path, compressed)
    out_size = Path(out_path).stat().st_size

    print("Compression Benchmark...")
    print("Input File:", in_path)
    print("Input Size:", in_size)
    print("Output File:", out_path)
    print("Output Size:", out_size)
    print("Ratio:", out_size/in_size)

def decompress_file(compressed_path: str, out_path: str) -> None:
    """
    Consume a compressed file from compressedpath, decompress it, and
    write it to outpath.
    """
    compressed_data = file_to_bytes(compressed_path)
    
    decompressed = my_decompressor(compressed_data)

    bytes_to_file(out_path, decompressed)

def recovery_check(in_path: str, compressed_path: str) -> bool:

    original = file_to_bytes(in_path)
    expected_checksum = hashlib.md5(original).hexdigest()

    decompress_file(compressed_path, "tmp")
    recovered = file_to_bytes("tmp")
    recovered_checksum = hashlib.md5(recovered).hexdigest()

    assert expected_checksum == recovered_checksum, "Uh oh!"


if __name__ == "__main__":
    compress_file(sys.argv[1], sys.argv[2])
    recovery_check(sys.argv[1], sys.argv[2])

# reference GPT 
# how would i do this for dna kmers GCAT

# To compress DNA k-mers (subsequences of DNA of length k, made up of 'G', 'C', 'A', and 'T') efficiently, you can leverage the small alphabet size (only 4 characters) to reduce the storage requirements. Here's how you could approach the my_compressor and my_decompressor functions:

# Compression (my_compressor):
# Mapping characters: You can map 'G', 'C', 'A', and 'T' to 2-bit representations:

# 'G' = 00
# 'C' = 01
# 'A' = 10
# 'T' = 11
# Packing bits: Given that each nucleotide (base) can be represented by 2 bits, you can pack 4 bases into a single byte (8 bits). For a sequence of DNA, this would allow you to compress the data significantly.

# Handling edge cases: If the number of nucleotides is not divisible by 4, you might need padding at the end of the compressed sequence, or store the length to correctly decompress later.

# Decompression (my_decompressor):
# Unpacking bits: Reverse the bit-packing process by extracting 2 bits at a time from each byte and mapping them back to the corresponding base ('G', 'C', 'A', or 'T').
# Code Example:
# python
# Copy code
# def my_compressor(in_bytes: bytes) -> bytes:
#     """
#     Compress a DNA sequence represented as bytes by converting each base
#     ('G', 'C', 'A', 'T') into its 2-bit representation.
#     """
#     # Create a dictionary to map bases to 2-bit values
#     base_to_bits = {
#         b'G': 0b00,
#         b'C': 0b01,
#         b'A': 0b10,
#         b'T': 0b11
#     }
    
#     compressed_bits = 0
#     num_bits = 0
#     compressed_bytes = bytearray()

#     # Iterate over the input bytes
#     for base in in_bytes:
#         # Shift current bits to the left by 2 and add the new base
#         compressed_bits = (compressed_bits << 2) | base_to_bits[bytes([base])]
#         num_bits += 2

#         # If we have 8 bits, we can append a full byte
#         if num_bits == 8:
#             compressed_bytes.append(compressed_bits)
#             compressed_bits = 0
#             num_bits = 0

#     # If there are leftover bits (in case in_bytes length is not divisible by 4)
#     if num_bits > 0:
#         compressed_bits <<= (8 - num_bits)  # Padding remaining bits to fill a byte
#         compressed_bytes.append(compressed_bits)

#     return bytes(compressed_bytes)

# def my_decompressor(compressed_bytes: bytes) -> bytes:
#     """
#     Decompress a compressed DNA sequence back into the original
#     'G', 'C', 'A', 'T' sequence.
#     """
#     # Reverse mapping from 2-bit values to DNA bases
#     bits_to_base = {
#         0b00: b'G',
#         0b01: b'C',
#         0b10: b'A',
#         0b11: b'T'
#     }

#     decompressed = bytearray()

#     for byte in compressed_bytes:
#         # Process 4 bases per byte (2 bits for each base)
#         for shift in [6, 4, 2, 0]:
#             base_bits = (byte >> shift) & 0b11
#             decompressed.extend(bits_to_base[base_bits])

#     return bytes(decompressed)
# How It Works:
# Compression: The my_compressor function packs 4 DNA bases into each byte by shifting bits and appending full bytes to the compressed output.
# Decompression: The my_decompressor function unpacks 2 bits at a time from each byte and converts them back to DNA bases.
# This approach takes advantage of the small alphabet size of DNA to reduce storage by representing each base using only 2 bits. You can now plug these functions into your compression utility and test them on DNA data.

# Let me know if you need further clarifications or enhancements!