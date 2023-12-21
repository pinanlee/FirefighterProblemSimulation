#!/usr/bin/env python
from random import Random
import random
from randomPlanarGraph import graphops 
from randomPlanarGraph import graphio

width=1200  #1000
height=550 #1000
node=10
# fire_edges=55
# firefighter_edges=70
# seed=120
seed = random.randint(1, 1000)
radius=40
data_idx = 3

def default_seed():
	import os, struct
	try:
		# get very random 32-bit int from the operating system
		return struct.unpack('I', os.urandom(4))[0]
	except NotImplementedError:
		# backup seed: this can be imperfect so we don't want it always
		import time
		return int(time.time()) | os.getpid()

def make_streams(seed):
	# since triangulator is specialised and might need its own random stream
	# may as well stream the other steps too!
	streams = {}
	i=0
	for k in ['gen', 'tri', 'span', 'ext', 'double']:
		streams[k] = Random(seed+i)
		i += 1
	return streams

def main_2nd(st, node, fire_edges, firefighter_edges, data_idx):
	num_nodes = node
	if st == 'fire':
		num_edges = fire_edges
	elif st == 'firefighter':
		num_edges = firefighter_edges
	import time
	import os
	streams = make_streams(seed)

	# first generate some points in the plane, according to our constraints
	nodes = graphops.generate_nodes(num_nodes, width, height, radius, streams['gen'])
	num_nodes = len(nodes)
	# find a delaunay triangulation, so we have a list of edges that will give planar graphs
	tri_edges = graphops.triangulate(nodes, streams['tri'], 'conform')
	# compute a spanning tree to ensure the graph is joined
	span_edges = graphops.spanning_tree(nodes, tri_edges, streams['span'])
	
	# extend the tree with some more edges to achieve our target num_edges
	# pick the extra ones from tri_edges to preserve planarity
	ext_edges = graphops.extend_edges(span_edges, num_edges, tri_edges, 0.0, streams['ext'])
	# randomly double some edges
	doubled_edges = graphops.double_up_edges(ext_edges, 0.0, streams['double'])

	# write out to file
	graphio.write(st, nodes, doubled_edges, data_idx)

# def main(st):
# 	num_nodes = node
# 	if st == 'fire':
# 		num_edges = fire_edges
# 	elif st == 'firefighter':
# 		num_edges = firefighter_edges
# 	streams = make_streams(seed)

# 	# first generate some points in the plane, according to our constraints
# 	nodes = graphops.generate_nodes(num_nodes, width, height, radius, streams['gen'])
# 	num_nodes = len(nodes)
# 	# find a delaunay triangulation, so we have a list of edges that will give planar graphs
# 	tri_edges = graphops.triangulate(nodes, streams['tri'], 'conform')
# 	# compute a spanning tree to ensure the graph is joined
# 	span_edges = graphops.spanning_tree(nodes, tri_edges, streams['span'])
	
# 	# extend the tree with some more edges to achieve our target num_edges
# 	# pick the extra ones from tri_edges to preserve planarity
# 	ext_edges = graphops.extend_edges(span_edges, num_edges, tri_edges, 0.0, streams['ext'])
# 	# randomly double some edges
# 	doubled_edges = graphops.double_up_edges(ext_edges, 0.0, streams['double'])

# 	# write out to file
# 	graphio.write(st, nodes, doubled_edges, data_idx)
# 	#print(doubled_edges)

	# write out debug traces if specified -- usually not used
	# if opts.debug_tris is not None:
	# 	graphio.write(opts.debug_tris, nodes, tri_edges, opts.seed)
	# 	print(tri_edges)
	# if opts.debug_span is not None:
	# 	graphio.write(opts.debug_span, nodes, span_edges, opts.seed)
	# 	print(span_edges)

def generate_test_data(node, fire_edges, firefighter_edges, data_idx):
	defaults = {
		"width": 320,
		"height": 240,
		"nodes": 10,
		"edges": None,
		"radius": 40,
		"double": 0.0,
		"hair": 0.0,
		#"seed": default_seed(),
		"seed": 0,
		"debug_trimode": 'conform',
		"debug_tris": None,
		"debug_span": None,
	}
	main_2nd("firefighter", node, fire_edges, firefighter_edges, data_idx)
	main_2nd("fire", node, fire_edges, firefighter_edges, data_idx)

if __name__=='__main__':
	#import argparse
	defaults = {
		"width": 320,
		"height": 240,
		"nodes": 10,
		"edges": None,
		"radius": 40,
		"double": 0.0,
		"hair": 0.0,
		#"seed": default_seed(),
		"seed": 0,
		"debug_trimode": 'conform',
		"debug_tris": None,
		"debug_span": None,
	}
	generate_test_data(15, 30, 30, 1)
	# # argument types, for input-checking
	# def posint(string):
	# 	value = int(string)
	# 	if value <= 0:
	# 		raise argparse.ArgumentTypeError("positive value expected")
	# 	return value

	# def nonnegative_int(string):
	# 	value = int(string)
	# 	if value < 0:
	# 		raise argparse.ArgumentTypeError("non-negative value expected")
	# 	return value

	# def probability(string):
	# 	value = float(string)
	# 	if value < 0.0 or value > 1.0:
	# 		raise argparse.ArgumentTypeError("value in the range [0.0, 1.0] expected")
	# 	return value

	# definition of argument structure

	# parser = argparse.ArgumentParser(
	# 	description="Create random planar graphs, suitable as input to graphviz neato.",
	# 	epilog="Note that sometimes neato decides to pick a nonplanar embedding.  Try giving neato the -n1 argument to use the node coordinates specified by this script, which are always planar but might not look as pretty."
	# )
	# parser.add_argument("--width", metavar="SIZE", type=posint, required=False, help="Width of the field on which to place points.  neato might choose a different width for the output image.")
	# parser.add_argument("--height", metavar="SIZE", type=posint, required=False, help="Height of the field on which to place points.  As above, neato might choose a different size.")
	# parser.add_argument("--nodes", metavar="NUM", type=posint, required=False, help="Number of nodes to place.")
	# parser.add_argument("--edges", metavar="NUM", type=posint, required=False, help="Number of edges to use for connections.  Double edges aren't counted.")
	# parser.add_argument("--radius", metavar="SIZE", type=nonnegative_int, required=False, help="Nodes will not be placed within this distance of each other.  Default %d." % defaults["radius"])
	# parser.add_argument("--double", metavar="CHANCE", type=probability, required=False, help="Probability of an edge being doubled.  Ranges from 0.00 to 1.00.  Default %.2f." % defaults["double"])
	# parser.add_argument("--hair", metavar="AMOUNT", type=probability, required=False, help="Adjustment factor to favour dead-end nodes.  Ranges from 0.00 (least hairy) to 1.00 (most hairy).  Some dead-ends may exist even with a low hair factor.  Default %.2f." % defaults["hair"])
	# parser.add_argument("--seed", metavar="NUMBER", type=int, required=False, help="Seed for the random number generator.  You can check the output file to see what seed was used.")
	# parser.add_argument("--debug-trimode", type=str, choices=['pyhull', 'triangle', 'conform'], required=False, help="Triangulation mode to generate the initial triangular graph.  Default is conform.")
	# parser.add_argument("--debug-tris", metavar="FILENAME", type=str, required=False, help="If a filename is specified here, the initial triangular graph will be saved as a graph for inspection.")
	# parser.add_argument("--debug-span", metavar="FILENAME", type=str, required=False, help="If a filename is specified here, the spanning tree will be saved as a graph for inspection.")
	# #parser.add_argument("filename", type=str, help="The graphviz output will be written to this file.")

	# set defaults and parse!
	#parser.set_defaults(**defaults)
	#options = parser.parse_args()

	# post-twiddling of arguments, and cross-checking
	# if options.edges is None:
	# 	options.edges = int(options.nodes * 1.25)
	# options.edges = max(options.edges, options.nodes-1) # necessary to avoid a disjoint graph

	# run!
	# main("firefighter")
	# print('tttttttttt')
	# main("fire")
