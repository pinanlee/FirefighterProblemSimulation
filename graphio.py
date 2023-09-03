import pandas as pd
import math
import random
#ORD_A = ord('A')

# def node_id_char(i):
# 	return chr(ORD_A + i)

# def node_id(i):
# 	ident = ""
# 	i += 1
# 	while i > 0:
# 		c = (i-1) % 26
# 		ident = node_id_char(c) + ident
# 		i = int((i-c)/26)
# 	return ident

# ESCAPES = {'\\':'\\', '\n':'n', '\t':'t', '\r':'r', '"':'"', "'":"'", }
# def escape(string):
# 	result = '"'
# 	for c in string:
# 		if c in ESCAPES:
# 			result += '\\' + ESCAPES[c]
# 		else:
# 			result += c
# 	return result + '"'

# def write_attributes(stream,attribs_dict):
# 	if len(attribs_dict)==0:
# 		return
# 	stream.write(" [")
# 	first = True
# 	for key in attribs_dict:
# 		if not first:
# 			stream.write(", ")
# 		first = False
# 		value = attribs_dict[key]
# 		stream.write("%s=" % str(key))
# 		stream.write(escape(str(value)))
# 	stream.write("]")

# def write_edge(edge):
# 	id0 = node_id(edge[0])
# 	id1 = node_id(edge[1])
# 	Arc.append((id0,id1)) #append arc set
    #attribs = {}
    #if len(edge)>2:
        #attribs = edge[2]
    #stream.write("\t")
    #stream.write("%s -- %s" % (id0, id1))
    
    #write_attributes(stream, attribs)
    #stream.write(";\n")

# def write_node(node):
# 	Position.append((node[0],node[1])) #append node(x,y)
    
    #attribs = {}
    #if len(node)>2:
        #attribs = node[2]
    #attribs['pos'] = "%d,%d" % (node[0], node[1])
    #stream.write("\t")
    #stream.write(node_id(index))
    #write_attributes(stream, attribs)
    #stream.write(";\n")

# def write_graph_meta(stream, attribs):
# 	if len(attribs)==0:
# 		return
# 	stream.write("\tgraph")
# 	write_attributes(stream, attribs)
# 	stream.write(";\n")

def distance(x1,y1,x2,y2):
    return math.sqrt( (x1-x2)**2 + (y1-y2)**2)

def getTravelTime(case,d):
    if case == "firefighter":
        if d < 100:
            return random.randint(5,9)
        elif d < 200:
            return random.randint(10,14)
        elif d < 300:
            return random.randint(15,19)
        elif d < 400:
            return random.randint(20,24)
        else:
            return random.randint(25,30)
    elif case == "fire":
        if d < 100:
            return random.randint(15,19)
        elif d < 200:
            return random.randint(20,24)
        elif d < 300:
            return random.randint(25,29)
        elif d < 400:
            return random.randint(30,34)
        else:
            return random.randint(35,39)
        
def write_graph(st, nodes, edges):
    #stream.write("graph {\n")
    Arc=[] #arc
    Position=[] #coordinates
    from_list=[]
    to_list=[]
    x_list=[]
    y_list=[]
    travel_time=[]
    travel_distance=[]
    firefighter_index=[]
    q=[]
    b=[]
    h=[]
    #specify fire source and depot node ID
    N_D={26}
    N_F={1}
    #specify number of firefighter
    K={1}

    #write_graph_meta(stream, attribs)
    for i in range(len(nodes)):
        Position.append((nodes[i][0],nodes[i][1]))
    for i in range(len(edges)):
        Arc.append((edges[i][0]+1,edges[i][1]+1)) #let node id start from 1 to N 
    
    #save to excel
    for i in range(len(Position)):
        x_list.append(Position[i][0])
        y_list.append(Position[i][1])
        q.append(3)
        b.append(3)
        h.append(3)
    df = pd.DataFrame({'x':x_list,'y':y_list,'value':b,'burning time':h,'quantity':q})
    df.to_excel("G"+str(len(Position))+"_nodeInformation.xlsx", index=False)

    if st == 'fire':
        for i in range(len(Arc)):
            a = Arc[i][0]
            b = Arc[i][1]
            if a not in N_D and b not in N_D:
                d = distance(Position[a-1][0],Position[a-1][1],Position[b-1][0],Position[b-1][1])
                t = getTravelTime("fire",d)

                from_list.append(a)
                to_list.append(b)
                travel_distance.append(d)
                travel_time.append(t)
                from_list.append(b)
                to_list.append(a)
                travel_distance.append(d)
                travel_time.append(t)
        df = pd.DataFrame({"i": from_list,"j":to_list,"d":travel_distance,"travel time":travel_time})
        df.to_excel("G"+str(len(Position))+"_fire_route.xlsx", index=False)
    elif st == 'firefighter':
        for k in K:
            for i in range(len(Arc)):
                a = Arc[i][0]
                b = Arc[i][1]
                if a not in N_F and b not in N_F:
                    d = distance(Position[a-1][0],Position[a-1][1],Position[b-1][0],Position[b-1][1])
                    t = getTravelTime("firefighter",d)

                    firefighter_index.append(k)
                    from_list.append(a)
                    to_list.append(b)
                    travel_distance.append(d)
                    travel_time.append(t)
                    firefighter_index.append(k)
                    from_list.append(b)
                    to_list.append(a)
                    travel_distance.append(d)
                    travel_time.append(t)

        df = pd.DataFrame({"k":firefighter_index,"i": from_list,"j":to_list,"d":travel_distance,"travel time":travel_time})
        df.to_excel("G"+str(len(Position))+"_firefighter_route.xlsx", index=False)
    #stream.write("}\n")

def write(st, nodes, edges):
    #with open(filename, 'w') as f:
        #f.write("// random seed %d\n" % seed)
    write_graph(st, nodes, edges)