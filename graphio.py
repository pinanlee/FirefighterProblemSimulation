import pandas as pd
ORD_A = ord('A')
Arc=[] #arc
Position=[] #coordinates
def node_id_char(i):
	return chr(ORD_A + i)

def node_id(i):
	ident = ""
	i += 1
	while i > 0:
		c = (i-1) % 26
		ident = node_id_char(c) + ident
		i = int((i-c)/26)
	return ident

ESCAPES = {'\\':'\\', '\n':'n', '\t':'t', '\r':'r', '"':'"', "'":"'", }
def escape(string):
	result = '"'
	for c in string:
		if c in ESCAPES:
			result += '\\' + ESCAPES[c]
		else:
			result += c
	return result + '"'

def write_attributes( attribs_dict):
	if len(attribs_dict)==0:
		return
	#stream.write(" [")
	first = True
	for key in attribs_dict:
		#if not first:
			#stream.write(", ")
		first = False
		value = attribs_dict[key]
		#stream.write("%s=" % str(key))
		#stream.write(escape(str(value)))
	#stream.write("]")

def write_edge( edge, index):
	attribs = {}
	if len(edge)>2:
		attribs = edge[2]

	id0 = node_id(edge[0])
	id1 = node_id(edge[1])

	#stream.write("\t")
	#stream.write("%s -- %s" % (id0, id1))
	Arc.append((id0,id1)) #append arc set
	write_attributes(attribs)
	#stream.write(";\n")

def write_node( node, index):
	attribs = {}
	if len(node)>2:
		attribs = node[2]
	attribs['pos'] = "%d,%d" % (node[0], node[1])
	
	Position.append((node[0],node[1])) #append node(x,y)

	#stream.write("\t")
	#stream.write(node_id(index))
	write_attributes(attribs)
	#stream.write(";\n")

def write_graph_meta(attribs):
	if len(attribs)==0:
		return
	#stream.write("\tgraph")
	write_attributes( attribs)
	#stream.write(";\n")

def write_graph(st, nodes, edges, attribs):
	#stream.write("graph {\n")
	from_list=[]
	to_list=[]
	x_list=[]
	y_list=[]
	write_graph_meta( attribs)
	for i in range(len(nodes)):
		write_node(nodes[i], i)
	for i in range(len(edges)):
		write_edge(edges[i], i)
	#save to excel
	#print(len(Arc))
	#print(len(Position))
	for i in range(len(Arc)):
		from_list.append(Arc[i][0])
		to_list.append(Arc[i][1])
	for i in range(len(Position)):
		x_list.append(Position[i][0])
		y_list.append(Position[i][1])
	df = pd.DataFrame({"i":from_list,"j":to_list,"num":len(nodes)})
	if(st == "fire"):
		df.to_excel("adjacent data -- fire.xlsx", index=False)
	elif(st == "FF"):
		df.to_excel("adjacent data -- ff.xlsx", index=False)
		df = pd.DataFrame({"x":x_list,"y":y_list})
		df.to_excel("coordinates data.xlsx", index=False)
	#stream.write("}\n")

def write(st, nodes, edges, seed, graph_attribs={}):
	#with open(filename, 'w') as f:
	#	f.write("// random seed %d\n" % seed)
	write_graph(st, nodes, edges, graph_attribs)
