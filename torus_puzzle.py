#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Helper method that calculate the heuristic of a state
@param state: the state represented by a list
@return h: the heuristic of the state
"""
def heuristic_calculator(state):
    h=0
    # Count the number of tiles that are in the wrong position
    for i in range(0,len(state)-1):
        if (state[i]!=(i+1)):
            h=h+1
    return h


# In[2]:


"""
Helper method that find the position of the space in the state
@param state: the state represented by a list
@return i: the index of the space
"""
def find_space(state):
    # Go through the array to find the space (0)
    for i in range(0,9):
        if (state[i]==0):
            return i


# In[3]:


"""
Helper method that swap two number in the list, or in other words, move the number
@param state: the state represented by a list
@index1: index of the space/the number needs moving
@index2: index of the number needs moving/the space
@return: the succ_state represented by a list
"""
def swap(state, index1, index2):
    # Copy the current state to the succ state
    succ = list(state)
    
    # Swap the two tiles need swaping
    temp = succ[index1]
    succ[index1] = succ[index2]
    succ[index2] = temp
    
    return succ


# In[4]:


"""
Helper method that generates a sorted list of a state successors
@param state: a state represented by a list
@return succ_list: a list of successors represented by lists
"""
def succ_state_helper(state):
    # Find the space to generate moves
    space = find_space(state)
    # List that stores succ state
    succ_list = []
    
    # Convert index of a flat list into the 2D index
    row = int(space/3)
    col = space%3
    
    # Check all posible moves and append valid ones to the list
    # Move up one step
    if (row-1)>=0:
        succ_state = swap(state, space, (space-3))
        succ_list.append(succ_state)
    # Move down one step
    if (row+1)<3:
        succ_state = swap(state, space, (space+3))
        succ_list.append(succ_state)
    # Wrap up vertically
    if (row-2)==0:
        succ_state = swap(state, space, (space-6))
        succ_list.append(succ_state)
    # Wrap down vertically
    if (row+2)==2:
        succ_state = swap(state, space, (space+6))
        succ_list.append(succ_state)
    # Move left one step
    if (col-1)>=0:
        succ_state = swap(state, space, (space-1))
        succ_list.append(succ_state)
    # Move right one step
    if (col+1)<3:
        succ_state = swap(state, space, (space+1))
        succ_list.append(succ_state)
    # Wrap right horizontally
    if (col+2)==2:
        succ_state = swap(state, space, (space+2))
        succ_list.append(succ_state)
    # Wrap left horizontally
    if (col-2)==0:
        succ_state = swap(state, space, (space-2))
        succ_list.append(succ_state)
        
    # Sort the steps
    succ_list = sorted(succ_list)
    
    return succ_list


# In[5]:


"""
Given a state of the puzzle, print to the console all of the possible successor states
@param state: a state represented as a single list of integers with a 0 in the empty space
"""
def print_succ(state):
    # Generate a list of successors
    s_list = succ_state_helper(state)
    
    # Print all elements in the list
    for s in s_list:
        print(str(s)+" h="+str(heuristic_calculator(s)))


# In[6]:


''' author: hobbes
    source: cs540 canvas
    TODO: complete the enqueue method
'''
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.close = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the initial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.

            TODO: complete this method to handle the case where a state is
                  already present in the priority queue
        """
        in_open = False
        # A boolean check whether the state is in the close queue
        in_close = False
        
        # Check whether the state is in the close queue
        for i in range(len(self.close)):
            if state_dict['state']==self.close[i]['state']:
                # Change the boolean check in_close to True
                in_close = True
                
                # Change the state
                if state_dict['g'] < self.close[i]['g']:
                    del self.close[i]
                    self.requeue(state_dict)
                break
                
        # Only check Open queue if the state is not in the close queue
        if not in_close:            
            for i in self.queue:
                if state_dict['state']==i['state']:
                    # Change in_open boolean to True if the state is in the queue
                    in_open = True
                    # Change the path and actual cost to get to the state if the new path is more optimal
                    if state_dict['g'] < i['g']:
                        i['g']=state_dict['g']
                        i['f']=state_dict['f']
                        i['parent']=state_dict['parent']
                    break

        # Enqueue is the state is not in either Open or Close queue
        if not (in_open or in_close):
            self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        self.close.append(state)
        return state


# In[7]:


"""
Helper method that generate a list of states represented as dictionaries
@param state: a state represented as a list
@return succ_state_dict: a list of states represented as dictionaries
"""
def succ_state_dict_generator(state):
    succ_list = succ_state_helper(state['state'])
    succ_state_dict = []
    for s in succ_list:
        h = heuristic_calculator(s)
        g = state['g']+1
        f = g+h
        succ_state_dict.append({'state':s, 'parent':state, 'h':h, 'g':g, 'f':f})
    return succ_state_dict


# In[29]:


"""
Given a state of the puzzle, perform the A* search algorithm and print the path from the current state to the goal state
@param state: a state represented as a list
"""
def solve(state):
    h = heuristic_calculator(state)
    state_dict = {'state':state, 'parent':None, 'h':h, 'g':0, 'f':h}
    print(str(state)+"  h="+str(h)+"  moves: 0")
    
    queue = PriorityQueue()
    queue.enqueue(state_dict)
    
    while (state_dict['h']!=0):
        for s in succ_state_dict_generator(state_dict):
            queue.enqueue(s)
        state_dict = queue.pop()

    solution = []
    while(state_dict['parent']!=None):
        solution.append(state_dict)
        state_dict = state_dict['parent']
    move = 1
    while(move<=len(solution)):
        step = solution[len(solution)-move]
        print(str(step['state'])+"  h="+str(step['h'])+"  moves: "+str(move))
        move = move +1
    print("Max queue length: " + str(queue.max_len))

