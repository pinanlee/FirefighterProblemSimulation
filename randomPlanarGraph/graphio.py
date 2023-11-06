import pandas as pd
import math
import random


def distance(x1,y1,x2,y2):
    return math.sqrt( (x1-x2)**2 + (y1-y2)**2)

def getTravelTime(case,d):
    ff_lb = 5
    ff_increment = 4
    fire_lb = 15
    fire_increment = 5

    if case == "firefighter":
        if d < 400:
            return random.randint(ff_lb,ff_lb+(int(d/100)+1)*ff_increment-1)
        else:
            return random.randint(ff_lb+4*ff_increment,ff_lb+5*ff_increment-1)
    elif case == "fire":
        if d < 400:
            return random.randint(fire_lb,fire_lb+(int(d/100)+1)*fire_increment-1)
        else:
            return random.randint(fire_lb+4*fire_increment,fire_lb+5*fire_increment-1)
        
def write_graph(st, nodes, edges, data_idx):
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
    N_D=[random.randint(1,len(nodes))]
    temp = random.randint(1,len(nodes))
    while True:
        if temp in N_D:
            temp = random.randint(1,len(nodes))
        else:
            N_F=[temp]
            break

    #specify number of firefighter and their ability
    K={1,2}
    P = [2,5]

    T = [300]

    fire_edges = 0
    ff_edges = 0
    fire_route_df, ff_route_df = pd.DataFrame(), pd.DataFrame()

    #write_graph_meta(stream, attribs)
    for i in range(len(nodes)):
        Position.append((nodes[i][0],nodes[i][1]))
    for i in range(len(edges)):
        Arc.append((edges[i][0]+1,edges[i][1]+1)) #let node id start from 1 to N 
    
    #save to excel
    for i in range(len(Position)):
        value = {5,10,15}
        x_list.append(Position[i][0])
        y_list.append(Position[i][1])
        q_num = random.randint(1,10)
        #b_num = random.randint(1,10)
        h_num = random.randint(1,10)
        q.append(q_num)
        b.append(random.sample(value,1)[0])
        h.append(h_num)

    if st == 'fire':
        ff_df = pd.read_excel("./randomPlanarGraph/data/FFP_n"+str(len(Position))+"_no"+str(data_idx)+".xlsx",sheet_name="ff_source")
        fire_df = pd.read_excel("./randomPlanarGraph/data/FFP_n"+str(len(Position))+"_no"+str(data_idx)+".xlsx",sheet_name="fire_source")
        N_D = list(ff_df['N_D'])
        N_F = list(fire_df['N_F'])
        print('fire',N_D,N_F)
        for i in range(len(Arc)):
            u = Arc[i][0]
            v = Arc[i][1]
            if u not in N_D and v not in N_D:
                #print((u,v))
                #print(N_D)
                d = distance(Position[u-1][0],Position[u-1][1],Position[v-1][0],Position[v-1][1])
                t = getTravelTime("fire",d)

                from_list.append(u)
                to_list.append(v)
                travel_distance.append(d)
                travel_time.append(t)
                from_list.append(v)
                to_list.append(u)
                travel_distance.append(d)
                travel_time.append(t)
                fire_edges+=1
        fire_route_df = pd.DataFrame({"i": from_list,"j":to_list,"d":travel_distance,"travel time":travel_time})
        with pd.ExcelWriter("./randomPlanarGraph/data/FFP_n"+str(len(Position))+"_no"+str(data_idx)+".xlsx", mode='a', engine='openpyxl') as writer:
            fire_route_df.to_excel(writer, sheet_name = 'fire_route', index = False)
            
        # df.to_excel("G"+str(len(Position))+"_fire_route.xlsx", index=False)
    elif st == 'firefighter':
        print('ff',N_D,N_F)
        for k in K:
            for i in range(len(Arc)):
                u = Arc[i][0]
                v = Arc[i][1]
                if u not in N_F and v not in N_F:
                    d = distance(Position[u-1][0],Position[u-1][1],Position[v-1][0],Position[v-1][1])
                    t = getTravelTime("firefighter",d)
                    print((u,v))
                    print(N_F)
                    firefighter_index.append(k)
                    from_list.append(u)
                    to_list.append(v)
                    travel_distance.append(d)
                    travel_time.append(t)
                    firefighter_index.append(k)
                    from_list.append(v)
                    to_list.append(u)
                    travel_distance.append(d)
                    travel_time.append(t)
                    ff_edges += 1

        ff_route_df = pd.DataFrame({"k":firefighter_index,"i": from_list,"j":to_list,"d":travel_distance,"travel time":travel_time})
        with pd.ExcelWriter("./randomPlanarGraph/data/FFP_n"+str(len(Position))+"_no"+str(data_idx)+".xlsx", mode='w', engine='openpyxl') as writer:
            ff_route_df.to_excel(writer, sheet_name = 'firefighter_route', index = False)
            
        # df.to_excel("G"+str(len(Position))+"_firefighter_route.xlsx", index=False)
    
    df = pd.DataFrame({'x':x_list,'y':y_list,'value':b,'burning time':h,'quantity':q})

    if len(N_D) != len(P):
        for i in range(len(P) - len(N_D)):
            N_D.append(N_D[0])

    df2 = pd.DataFrame({'N_D':N_D,'P':P})
    df3 = pd.DataFrame({'N_F':N_F})
    df4 = pd.DataFrame({'T':T})

    # with pd.ExcelWriter("G"+str(len(Position))+"_nodeInformation.xlsx") as writer:
    if st == 'firefighter':
        with pd.ExcelWriter("./randomPlanarGraph/data/FFP_n"+str(len(Position))+"_no"+str(data_idx)+".xlsx", mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name = 'coordinates', index = False)
            df2.to_excel(writer, sheet_name = 'ff_source', index = False)
            df3.to_excel(writer, sheet_name='fire_source', index = False) 
            df4.to_excel(writer, sheet_name='T', index=False)
            #print('123123')
        
    print("finish")

    #stream.write("}\n")

def write(st, nodes, edges, data_idx):
    #with open(filename, 'w') as f:
        #f.write("// random seed %d\n" % seed)
    write_graph(st, nodes, edges, data_idx)