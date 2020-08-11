from tkinter import *
from tkinter import ttk
from time import sleep
import random
import threading
from collections import defaultdict
import queue
import math
from helper.const import *

class Display():
    
    def __init__(self):
        self.items = [[_ for _ in range(no_of_cols)]for _ in range(no_of_rows)]
        self.start=(0,0)
        self.end=(no_of_cols-1,no_of_rows-1)
        self.parent = {}
        self.obstacles = set()
        self.initialize_graph()
        #bidirectional variables
        self.parent_rev ={}
        

    def initialize_graph(self):
        for i in range(no_of_cols):
            for j in range(no_of_rows):
                if random.random()<0.15:
                    self.create_obstable(i,j)
                self.display_cordinates(i,j)
        self.remove_obstical_crash()
        self.display_cordinates(self.start[0], self.start[1],start_color,end_outline)
        self.display_cordinates(self.end[0], self.end[1],end_color,end_outline)


    def create_obstable(self,i,j):
        self.obstacles.add((i,j))

    def remove_obstical_crash(self):
        if self.start in self.obstacles:
            self.obstacles.remove(self.start)
        if self.end in self.obstacles:
            self.obstacles.remove(self.end)

    def clear_obstacles(self):
        self.obstacles.clear()
        self.display_graph()


    def display_cordinates(self, i, j, fill_color=array_color, outline_color=array_outline):
        if (i,j) in self.obstacles:
            fill_color=obstacle_color
            outline_color=obstacle_outline
        self.items[j][i] = w.create_rectangle(
            i*box_size, j*box_size, (i+1)*box_size, (j+1)*box_size, fill=fill_color, outline=outline_color)        

    def display_graph(self):
        for i in range(no_of_cols):
            for j in range(no_of_rows):
                self.display_cordinates(i,j)
        self.display_cordinates(self.start[0], self.start[1], start_color, end_outline)
        self.display_cordinates(self.end[0], self.end[1], end_color, end_outline)

    def display_inqueue(self, i, j, queue_color=processing_color, queue_outline=processing_outline):
        w.itemconfig(self.items[j][i], fill=queue_color, outline=queue_outline)

    def display_processed(self, i, j, queue_color=processed_color, queue_outline=processed_outline):
        w.itemconfig(self.items[j][i], fill=queue_color, outline=queue_outline)

    def display_path(self, x, y):
        temp_x, temp_y, temp_parent = x, y, self.parent[(x, y)]
        while(temp_parent != (temp_x, temp_y)):
            self.display_inqueue(temp_x, temp_y, 'orange', 'cyan')
            temp_x, temp_y = temp_parent[0], temp_parent[1]
            temp_parent = self.parent[(temp_x, temp_y)]
        self.display_inqueue(temp_x, temp_y, 'orange', 'cyan')

    #used for backword search for bidirectional algorithms
    def display_path_rev(self, x, y,remove=False):
        temp_x, temp_y, temp_parent = x, y, self.parent_rev[(x, y)]
        while(temp_parent != (temp_x, temp_y)):
            self.display_inqueue(temp_x, temp_y, 'orange', 'cyan')
            temp_x, temp_y = temp_parent[0], temp_parent[1]
            temp_parent = self.parent_rev[(temp_x, temp_y)]
        self.display_inqueue(temp_x, temp_y, 'orange', 'cyan')

    def remove_visual_path(self, x, y):
        temp_x, temp_y, temp_parent = x, y, self.parent[(x, y)]
        while(temp_parent != (temp_x, temp_y)):
            self.display_processed(temp_x, temp_y)
            temp_x, temp_y = temp_parent[0], temp_parent[1]
            temp_parent = self.parent[(temp_x, temp_y)]
        self.display_processed(temp_x, temp_y)

    #backword treversal path removal for bidirectional search
    def remove_visual_path_rev(self, x, y):
        temp_x, temp_y, temp_parent = x, y, self.parent_rev[(x, y)]
        while(temp_parent != (temp_x, temp_y)):
            self.display_processed(temp_x, temp_y)
            temp_x, temp_y = temp_parent[0], temp_parent[1]
            temp_parent = self.parent_rev[(temp_x, temp_y)]
        self.display_processed(temp_x, temp_y)

class Graph_Traversal(Display):

    def __init__(self):
        super().__init__()
        self.items = [[_ for _ in range(no_of_cols)]for _ in range(no_of_rows)]
        self.visited = set()
        self.distance = defaultdict(lambda:float('inf'))
        self.keybind = None
        self.keybind_helper =None
        #bidirectional variables
        self.visited_rev = set()
        self.distance_rev = defaultdict(lambda:float('inf'))


    def clear_graph(self):
        w.delete('all')
        self.obstacles.clear()
        self.initialize_graph()
        self.parent.clear()
        self.visited.clear()
        self.distance.clear()
        self.parent_rev.clear()
        self.visited_rev.clear()
        self.distance_rev.clear()

    def refresh_graph(self):
        w.delete('all')
        self.display_graph()
        self.parent.clear()
        self.visited.clear()
        self.distance.clear()
        self.parent_rev.clear()
        self.visited_rev.clear()
        self.distance_rev.clear()

    #need to switch i,j represent x,y cordinate and in the array we have 
    #y cordinate corrosponding to the row and j corrpo

    # DFS start 
    def dfs(self):
        self.refresh_graph()
        self.parent[self.start]=self.start
        self.dfs_helper(self.start)
        if self.end in self.visited:
            self.display_path(self.end[0], self.end[1])

    #DFS seems faster due to the less time consuming display process
    def dfs_helper(self,current_ele):
        if self.end in self.visited:
            return
        self.visited.add(current_ele)
        x=current_ele[0]
        y=current_ele[1]
        self.display_cordinates(x,y,'orange','cyan')
        sleep(.0025)
        #visit all neighbours
        cur_distance=self.distance[current_ele]
        for i in range(x-1, x+2):
            if i<0 or i>=no_of_cols:
                continue
            for j in range(y-1,y+2):
                if self.end in self.visited:
                    break
                if j<0 or j>=no_of_rows:
                    continue
                if (i,j) in self.obstacles:
                    continue
                if (i,j) not in self.visited:
                        self.parent[(i,j)]=(x,y)
                        self.distance[(i,j)]=cur_distance
                        self.dfs_helper((i,j))
        self.display_processed(x, y)
    #DFS end 


    #BFS Start
    def bfs(self):
        self.refresh_graph()
        processed=set()
        flag=False
        q=queue.Queue(maxsize=0)
        self.parent[self.start]=self.start
        q.put(self.start)
        processed.add((self.start))
        self.display_inqueue(self.start[0], self.start[1])
        self.distance[self.start] = 0
        while(not q.empty()):
            temp=q.get()
            self.display_path(temp[0],temp[1])
            if temp in self.visited:
                continue
            if temp==self.end:
                flag=True
                break
            self.visited.add(temp)
            self.add_neighbour(q,temp[0],temp[1],processed)
            self.remove_visual_path(temp[0], temp[1])
            self.display_processed(temp[0],temp[1])
        
        if flag:
            self.display_path(self.end[0], self.end[1])


    def add_neighbour(self,q,x,y,processed):
        cur_distance=self.distance[(x,y)]+1
        for i in range(x-1,x+2):
            if i<0 or i>=no_of_cols:
                continue
            for j in range(y-1,y+2):
                if j<0 or j>=no_of_rows:
                    continue
                if (i==x and j==y):
                    continue
                if (i, j) in self.obstacles:
                    continue
                if (i,j) not in processed:
                    processed.add((i,j))
                    self.parent[(i,j)]=(x,y)
                    self.distance[(i,j)]=cur_distance
                    q.put((i,j))
                    self.display_inqueue(i,j)
    #BFS end 

    #djkstra start
    def dijkstra(self):
        self.refresh_graph()
        #search completion
        flag = False

        #forward pass variables
        q = queue.PriorityQueue(maxsize=0)
        self.parent[self.start] = self.start
        q.put((0, self.start[0], self.start[1]))
        self.display_inqueue(self.start[0], self.start[1])
        self.distance[self.start] = 0

        #main loop
        while(not q.empty()):
            temp = q.get()
            self.display_path(temp[1], temp[2])
            if (temp[1],temp[2])==self.end:
                    flag = True
                    break
            #since we are not changing priority and just adding new element with smaller priority
            #this keeps track of weather this has been visited with a smaller distance
            if (temp[1],temp[2]) in self.visited:
                continue

            self.add_neighbours_Dijkstra(q, temp)
            self.visited.add((temp[1], temp[2]))
            self.remove_visual_path(temp[1], temp[2])
            self.display_processed(temp[1], temp[2])
                #keeping track of all the nodes to check for distance


        if flag:
            self.display_path(self.end[0],self.end[1])


    #djkstra end

    #common for Djsktra and Bidirdjkstra
    def add_neighbours_Dijkstra(self,q,temp):
        prio, x, y = temp[0]+1, temp[1], temp[2]
        for i in range(x-1,x+2):
            if i<0 or i>=no_of_cols:
                continue
            for j in range(y-1,y+2):
                if j<0 or j>=no_of_rows:
                    continue
                if (i==x and j==y) or (i,j)in self.obstacles:
                    continue
                if (i,j) not in self.visited:
                    if self.distance[(i,j)]>prio:
                        self.distance[(i,j)]=prio
                        q.put((prio,i,j))
                        self.parent[(i,j)]=(x,y)
                        self.display_inqueue(i,j)
    
    #bi_djkstra start
    def bi_dijkstra(self):
        self.refresh_graph()
        #Bi-direction search variables  for completed search
        #search completion
        flag=False
        #track visited nodes
        visited_nodes=set()       

        #forward pass variables 
        forward=queue.PriorityQueue(maxsize=0)
        self.parent[self.start] = self.start
        forward.put((0, self.start[0], self.start[1]))
        self.display_inqueue(self.start[0], self.start[1])
        self.distance[self.start] = 0
        
        #reversed pass variables
        backword = queue.PriorityQueue(maxsize=0)
        self.parent_rev[self.end]=self.end
        backword.put((0,self.end[0],self.end[1]))
        self.display_inqueue(self.end[0], self.end[1])
        self.distance_rev[self.end]=0

        #main loop 
        while(not forward.empty()):
            #forward pass
            temp_f=forward.get()
            self.display_processed(temp_f[1], temp_f[2])
            #since we are not changing priority and just adding new element with smaller priority 
            #this keeps track of weather this has been visited with a smaller distance
            if (temp_f[1],temp_f[2]) not in self.visited:           
                self.display_path(temp_f[1],temp_f[2])
                self.visited.add((temp_f[1],temp_f[2]))
                self.add_neighbours_Dijkstra(forward,temp_f)
                #keeping track of all the nodes to check for distance
                if (temp_f[1], temp_f[2]) in visited_nodes:
                    flag=True
                    break
                visited_nodes.add((temp_f[1],temp_f[2]))
            self.remove_visual_path(temp_f[1], temp_f[2])
            
            #backward pass
            temp_b=backword.get()
            self.display_path_rev(temp_b[1],temp_b[2])
            #since we are not changing priority and just adding new element with smaller priority 
            #this keeps track of weather this has been visited with a smaller distance from this direction
            if (temp_b[1],temp_b[2]) not in self.visited_rev:           
                self.visited.add((temp_b[1],temp_b[2]))
                self.add_neighbours_Dijkstra_rev(backword,temp_b)
                self.display_processed(temp_b[1], temp_b[2])
                if (temp_b[1], temp_b[2]) in visited_nodes:
                    flag=True
                    break
                visited_nodes.add((temp_b[1], temp_b[2]))
            self.remove_visual_path_rev(temp_b[1], temp_b[2])

        if flag:
            self.remove_visual_path(temp_f[1], temp_f[2])
            self.remove_visual_path_rev(temp_b[1], temp_b[2])
            self.find_optimal_path(visited_nodes)
            #self.display_path(self.end[0], self.end[1])

    #gets the optinal path for bidirectional search
    def find_optimal_path(self,visited_nodes):
        cur_min_distance=float('inf')
        for item in visited_nodes:
            if self.distance[item]+self.distance_rev[item]<cur_min_distance:
                cur_min_point=item
                cur_min_distance=self.distance[item]+self.distance_rev[item]

        self.display_path_rev(cur_min_point[0],cur_min_point[1])
        self.display_path(cur_min_point[0],cur_min_point[1])

    def add_neighbours_Dijkstra_rev(self, q, temp):
        prio, x, y = temp[0]+1, temp[1], temp[2]
        for i in range(x-1, x+2):
            if i < 0 or i >= no_of_cols:
                continue
            for j in range(y-1, y+2):                
                if j < 0 or j >= no_of_rows:
                    continue
                if (i == x and j == y) or (i, j)in self.obstacles:
                    continue
                if (i, j) not in self.visited_rev:
                    if self.distance_rev[(i, j)] > prio:
                        self.distance_rev[(i, j)] = prio
                        q.put((prio, i, j))
                        self.parent_rev[(i, j)] = (x, y)
                        self.display_inqueue(i, j)
    #bidjkstra end

    #A* start
    def astar(self):
        self.refresh_graph()
        flag=False
        q = queue.PriorityQueue(maxsize=0)
        self.parent[self.start] = self.start
        q.put((0, self.start[0], self.start[1]))
        self.display_inqueue(self.start[0], self.start[1])
        self.distance[self.start] = 0
        temp=(0,self.start[0],self.start[1])
        while(not q.empty()):
            self.remove_visual_path(temp[1], temp[2])
            temp = q.get()
            if (temp[1], temp[2]) in self.visited:
                continue
            if (temp[1], temp[2]) == self.end:
                flag=True
                break
            self.display_path(temp[1], temp[2])
            self.visited.add((temp[1], temp[2]))
            self.add_neighbours_astar(q, temp, self.end)
            self.display_processed(temp[1], temp[2])
        if flag:
            self.display_path(self.end[0], self.end[1])

    def add_neighbours_astar(self, q, temp,end):
        parent_distance, x, y = self.distance[(temp[1],temp[2])]+1, temp[1], temp[2]
        for i in range(x-1, x+2):
            if i < 0 or i >= no_of_cols:
                continue
            for j in range(y-1, y+2):
                if j < 0 or j >= no_of_rows:
                    continue
                if (i==x and j==y) or ((i,j)in self.obstacles):
                    continue
                if (i, j) not in self.visited:
                    if self.distance[(i, j)] > parent_distance:
                        self.distance[(i, j)] = parent_distance
                        q.put((self.potential(i,j), i, j))
                        self.parent[(i, j)] = (x, y)
                        self.display_inqueue(i, j)
    
    def potential(self,i,j):
        return (self.distance[(i,j)]+math.sqrt((i-self.end[0])**2+(j-self.end[1])**2))
    #A* end

    def assign_points(self,item):
        if item ==1:
            self.keybind = w.bind('<Button-1>', self.edit_start)
        elif item==2:
            self.keybind = w.bind('<Button-1>',self.edit_end)
        else:
            self.keybind = w.bind('<Button-1>',self.add_obstacles)

    def edit_start(self , event):
        if event.x < canvas_width and event.y < canvas_height:
            self.display_cordinates(self.start[0],self.start[1])
            self.start=(event.x//box_size,event.y//box_size)
            self.remove_obstical_crash()
            self.display_cordinates(event.x//box_size,event.y//box_size,start_color,start_outline)
            w.unbind('<Button-1>', self.keybind)

    def edit_end(self, event):
        if event.x < canvas_width and event.y < canvas_height:
            self.display_cordinates(self.end[0],self.end[1])
            self.end=(event.x//box_size,event.y//box_size)
            self.remove_obstical_crash()
            self.display_cordinates(event.x//box_size, event.y//box_size,end_color, end_outline)
            w.unbind('<Button-1>', self.keybind)

    def add_obstacles(self,event):
        w.unbind('<Button-1>', self.keybind)
        self.keybind = w.bind('<B1-Motion>', self.add_obstacles_helper)
        self.keybind_helper = w.bind('<ButtonRelease-1>', self.stop_add_obstacles)

    def add_obstacles_helper(self,event):
        if event.x < canvas_width and event.y < canvas_height:
            event_cordinate = (event.x//box_size ,event.y//box_size)
            if (event_cordinate != self.start) and (event_cordinate!=self.end):
                self.create_obstable(event_cordinate[0],event_cordinate[1])
                self.display_cordinates(event_cordinate[0], event_cordinate[1])

    def stop_add_obstacles(self,event):
        w.unbind('<B1-Motion>', self.keybind)
        w.unbind('<ButtonRelease-1>', self.keybind_helper)

        

def background(func, *args):
    global thread
    if not thread.is_alive():
        thread = threading.Thread(target=func, args=args,daemon=True)
        thread.start()



#Screen widget
root = Tk()
root.title('Graph Traversal Visualiser')

#create instance of sort , canvas , background rectangle, and buttons
w = Canvas(root, width=canvas_width, height=canvas_height)
w.create_rectangle(0, 0, canvas_width, canvas_height, fill=bg_color)
T = Graph_Traversal()
thread=threading.Thread()

#start end obstacle buttons
clear_graph = Button(root,text='New Maze',command=lambda:T.clear_graph())
clear_obstacles = Button(root,text='Clear Obstacles',command=lambda:T.clear_obstacles())
select_start = Button(root, text='Starting Point', command=lambda: background(T.assign_points(1)))
select_end = Button(root, text='Ending Point', command=lambda: background(T.assign_points(2)))
select_obstacle = Button(root, text='Add Obstacles', command=lambda: background(T.assign_points(3)))

#all search functionality
search_dfs=Button(root,text='DFS', command=lambda:background(T.dfs))
search_bfs=Button(root,text='BFS', command=lambda:background(T.bfs))
search_dijkstra = Button(root, text='Dijkstra',command=lambda: background(T.dijkstra))
search_bidijkstra = Button(root, text='Bi_Dijkstra', command=lambda: background(T.bi_dijkstra))
search_astar = Button(root, text='A*', command=lambda: background(T.astar))

#place stuff
w.grid(row=0,column=0,columnspan=10)
clear_graph.grid(row=1,column=0)
clear_obstacles.grid(row=1,column=1)
select_start.grid(row=1,column=2)
select_end.grid(row=1, column=3)
select_obstacle.grid(row=1,column=4)
search_dfs.grid(row=1,column=5)
search_bfs.grid(row=1,column=6)
search_dijkstra.grid(row=1,column=7)
search_bidijkstra.grid(row=1,column=8)
search_astar.grid(row=1,column=9)
root.after(20,w.update_idletasks())

#magical graphics
root.mainloop()