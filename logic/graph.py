from graphic.graphicForGame import draw_maze
import pygame
from logic.vertex import Vertex
import random
from logic.queue_home_made import Queue
import random
from queue import PriorityQueue
class Graph:
    def __init__(self):
       self.vertices_list = {}
       self.build_steps = []


    # function cơ bản của graph 
    def add_vertex(self, key):
        new_vertex = Vertex(key) 
        if key not in self.vertices_list:
            self.vertices_list[key] = new_vertex 

    def add_edge(self,v1, v2, weight):
        if v1 not in self.vertices_list:
            self.add_vertex(v1)
        if v2 not in self.vertices_list:
            self.add_vertex(v2)
        self.vertices_list[v1].add_neighbor(self.vertices_list[v2], weight)
        self.vertices_list[v2].add_neighbor(self.vertices_list[v1], weight)

    def display(self):
        for i in self.vertices_list:
            print(f'{i}: ',end ="")
            for neighbor in self.vertices_list[i].connected_to:
                print(neighbor.key, end = ' ')
            print()
    def bfs(self, start):
        visted = set()
        q = Queue()
        q.enqueue(self.vertices_list[start])
        visted.add(start)
        while not q.isEmpty():
            current = q.dequeue()
            print(f"{current.key} ", end = '')
            for neighbor in current.connected_to:
                if neighbor not in visted:
                    q.enqueue(self.vertices_list[start])
                    visted.add(neighbor.key)

    def dfg(self,start):
        pass

    def dijkstra(self):
        pass

    ## function mở rộng thêm, đọc ma trận ( hứng lên cho vào ) 
    def int_to_char(self,i):
        return chr(i % 26 +65)
    def char_to_int(self,c):
        return ord(c.upper()) -65

    def read_matrix(self, adj_matrix):
        for i in range(len(adj_matrix)):
            u = self.int_to_char(i)
            new_vertice = Vertex(self.int_to_char(i))
            self.vertices_list[u] = new_vertice
            for j in range(len(adj_matrix[i])): 
                v = self.int_to_char(j)
                if adj_matrix[i][j] != 0:
                    self.add_edge(u,v, adj_matrix[i][j])
    
    
    # bắt đầu function mở rộng 
    # tạo grid để bắt đầu tạo ma trận
    def add_grid(self,x,):
        for row in range(x):
            for col in range(x):
                self.add_vertex(f'{row},{col}')
    
    # trả về các kết nôis tiềm năng nhât
    def  get_potential_connection(self,vertex,size):
        potential_connection_list = []
        row, col = map(int, vertex.split(","))
        if row - 1 >= 0: 
            potential_connection_list.append(f"{row-1},{col}")

        if row + 1 < size: 
            potential_connection_list.append(f"{row+1},{col}")
                
        if col - 1 >= 0: 
            potential_connection_list.append(f"{row},{col-1}")

        if col + 1 < size: 
            potential_connection_list.append(f"{row},{col+1}")
       
        return potential_connection_list

    def hunt_and_kill(self, vertex,size):
        visited = set()
        current = vertex
        visited.add(current)
        while True:
            neighbours = [neighbour for neighbour in self.get_potential_connection(current,size) if neighbour not in visited]
            if neighbours:
                next_vertex = random.choice(neighbours)
                self.add_edge(current, next_vertex,1)
                self.build_steps.append((current, next_vertex))
                visited.add(next_vertex)
                current =next_vertex
            else:
                found = False 
                for cell in visited:
                    neighbours =[n for n in self.get_potential_connection(cell,size) if n not in visited]
                    if neighbours :
                        next_vertex = random.choice(neighbours)
                        self.add_edge(cell, next_vertex,1)
                        visited.add(next_vertex)
                        self.build_steps.append((cell, next_vertex))
                        current = next_vertex 
                        found = True
                        break
                if not found:
                    break
    def prim(self, start, size):
        visited = set()
        visited.add(start)
        # 
        frontier = []

       
        for neighbor in self.get_potential_connection(start, size):
            frontier.append((start, neighbor))

        while frontier:
            cell, neighbor = random.choice(frontier)
            frontier.remove((cell, neighbor))

            if neighbor not in visited:
                self.add_edge(cell, neighbor, 1)
                self.build_steps.append((cell, neighbor))
                visited.add(neighbor)

                for next_neighbor in self.get_potential_connection(neighbor, size):
                    if next_neighbor not in visited:
                        frontier.append((neighbor, next_neighbor))

    def dfs(self,vertex,size, visited = None): ##recursive backtracker
        if visited == None:
            visited = set()
        visited.add(vertex)
        potential = self.get_potential_connection(vertex,size)
        random.shuffle(potential)
        for i in potential:
            if i not in visited:
                self.add_edge(vertex,i,1)
                self.build_steps.append((vertex,i))
    def A_star(self): #tam
        pass

    #ultility function

    def get_num_vertices(self, graph):
        return len(graph.vertices_list)

    def find_graphs(self, vertex, graphs):
        for g in graphs:
            if vertex in g.vertices_list:
                return g
        return None

    def is_enough_vertices(self, o_graph):
        if len(self.vertices_list) != len(o_graph.vertices_list):
            return False

        return True

    def merge_graphs(self, graph1, graph2, u, v, weight):
        graph1.add_edge(u,v,weight)
        graph2.add_edge(u,v,weight)

        #merge
        graph1.vertices_list = graph1.vertices_list + graph2.vertices_list

        return graph1


    def delete_graph(self,list_graphs:list, removed_graph): #Type Hints
        for g in list_graphs:
            if g is removed_graph:
                list_graphs.remove(g)

        return list_graphs

    def kurskal(self): #vinh
        edges = set()
        for v, neighbors in self.vertices_list.items():
            for u,w in neighbors.items():
                #tránh trùng cạnh (trong undirected graph), tuple có thứ tự cố định
                edge = tuple(sorted((v,u)) + [w])

        sorted_edges = sorted(edges, key= lambda x: x[3])
        graphs = []
        graph = Graph()

        first_edge = sorted_edges.pop(0)
        u,v,weight = first_edge
        graph.add_edge(u,v,weight)
        graphs.append(graph)

        while len(sorted_edges) != 0:
            edge = sorted_edges.pop(0)
            u,v,weight = edge
            g1 = self.find_graphs(u,graphs)
            g2 = self.find_graphs(v,graphs)
            if g1 and g2:
                if g1 is g2:
                    pass
                else:
                    self.merge_graphs(g1,g2,u,v,weight)
                    self.delete_graph(graphs,g2)

                    if self.is_enough_vertices(g1):
                        break

            elif g1:
                g1.add_edge(u,v,weight)
                if self.is_enough_vertices(g1):
                    break

            elif g2:
                g2.add_edge(u,v,weight)
                if self.is_enough_vertices(g2):
                    break

            else:
                graph = Graph()
                graph.add_edge(u, v, weight)
                graphs.append(graph)

        for g in graphs:
            if self.is_enough_vertices(g):
                return g

        return None

    def wilson(self, size):
        self.add_grid(size)
        all_cells = [f"{i},{j}" for i in range(size) for j in range(size)]
        in_tree = set()

        # Chọn ngẫu nhiên một đỉnh làm gốc
        root = random.choice(all_cells)
        in_tree.add(root)
        all_cells.remove(root)

        while all_cells:
            # Chọn một đỉnh chưa thuộc cây
            walk_start = random.choice(all_cells)
            walk = [walk_start]
            visited_in_walk = {walk_start}

            current = walk_start
            while current not in in_tree:
                neighbors = self.get_potential_connection(current, size)
                next_cell = random.choice(neighbors)
                # Loại bỏ vòng lặp: nếu đã đi qua next_cell thì cắt vòng
                if next_cell in visited_in_walk:
                    idx = walk.index(next_cell)
                    walk = walk[:idx+1]
                    visited_in_walk = set(walk)
                else:
                    walk.append(next_cell)
                    visited_in_walk.add(next_cell)
                current = next_cell
            # Thêm đường đi (đã loại vòng) vào cây
            for i in range(len(walk) - 1):
                u = walk[i]
                v = walk[i + 1]
                self.add_edge(u, v, 1)
                self.build_steps.append((u, v))
                in_tree.add(u)
                if u in all_cells:
                    all_cells.remove(u)
            # Đảm bảo cell cuối cùng cũng được thêm
            if walk[-1] in all_cells:
                all_cells.remove(walk[-1])
            in_tree.add(walk[-1])


    def origin_shift(self):
        pass


        


        


            