import numpy as np
import random
import math

class Maze(object):
    def __init__(self, walls, learning = True, epsilon = 0.1, alpha = 0.001):
        # For resetting maze and available walls to initial configuration without resetting Q table
        self.walls = walls
        self.available_actions = [None, ((0,0), (0,1)), ((0,1), (0,2)), ((0,2), (0,3)), ((0,3), (0,4)), ((0,4),(1,4)), ((1,4), (2,4)), ((2,4), (3,4)),
         ((3,4), (4,4)), ((4,4), (4,3)), ((4,3), (4,2)), ((4,2), (4,1)), ((4,1), (4,0)), ((4,0), (3,0)), ((3,0), (2,0)), ((2,0), (1,0)),
         ((1,0), (1,1)), ((1,1), (0,1)), ((1,1), (2,1)), ((2,1), (2,0)), ((2,1), (3,1)), ((3,1), (3,0)), ((3,1), (4,1)), ((3,1), (3,2)),
         ((3,2), (4,2)), ((3,2), (2,2)), ((2,2), (2,1)), ((2,2), (1,2)), ((1,2), (1,1)), ((1,2), (0,2)), ((1,2), (1,3)), ((1,3), (0,3)), 
         ((1,3), (1,4)), ((1,3), (2,3)), ((2,3), (2,4)), ((2,3), (2,2)), ((2,3), (3,3)), ((3,3), (3,2)), ((3,3), (3,4)), ((3,3), (4,3))]
        self.valid_actions = [None, ((0,0), (0,1)), ((0,1), (0,2)), ((0,2), (0,3)), ((0,3), (0,4)), ((0,4),(1,4)), ((1,4), (2,4)), ((2,4), (3,4)),
         ((3,4), (4,4)), ((4,4), (4,3)), ((4,3), (4,2)), ((4,2), (4,1)), ((4,1), (4,0)), ((4,0), (3,0)), ((3,0), (2,0)), ((2,0), (1,0)),
         ((1,0), (1,1)), ((1,1), (0,1)), ((1,1), (2,1)), ((2,1), (2,0)), ((2,1), (3,1)), ((3,1), (3,0)), ((3,1), (4,1)), ((3,1), (3,2)),
         ((3,2), (4,2)), ((3,2), (2,2)), ((2,2), (2,1)), ((2,2), (1,2)), ((1,2), (1,1)), ((1,2), (0,2)), ((1,2), (1,3)), ((1,3), (0,3)), 
         ((1,3), (1,4)), ((1,3), (2,3)), ((2,3), (2,4)), ((2,3), (2,2)), ((2,3), (3,3)), ((3,3), (3,2)), ((3,3), (3,4)), ((3,3), (4,3))]
        # miscellaneous 
        self.Q = dict()
        self.epsilon = epsilon
        self.alpha = alpha
        self.learning = learning

    # Prevents robot from moving through walls
    def is_permissible(self, cell, direction):

        dir_int = {'u': 1, 'r': 2, 'd': 4, 'l': 8,
                   'up': 1, 'right': 2, 'down': 4, 'left': 8}
        try:
            return (self.walls[tuple(cell)] & dir_int[direction] != 0)
        except:
            print 'Invalid direction provided!'

    # Adds state to Qtable if it isn't in it
    def Qtable(self,state):
        if state not in self.Q:
            self.Q[state] = dict()
            for action in self.valid_actions:
                self.Q[state][action] = 0.0
        return

    # Find highest Q in table for state
    def bestQ(self, state):
        action_pool = []
        for action in self.available_actions:
            action_pool.append(self.Q[state][action])
        maxQ = max(action_pool)
                
        return maxQ
    # Choose action associated with highest Q
    def choose_action(self, state, maxQ):
        best_action = []
        # Occasionally pick a random action instead, based on exploration factor, if learning
        if self.learning:
            if random.random < self.epsilon:
                for action in self.available_actions:
                    if self.Q[state][action] == maxQ:
                        best_action.append(action)
            else:
                return random.choice(self.available_actions)
        else:
            for action in self.available_actions:
                if self.Q[state][action] == maxQ:
                    best_action.append(action)

        # Helps Mazey out a bit. If the robot is facing up, place a wall directly above it if possible
        if state[2] == 'u' and ((state[0], state[1] + 1), (state[0], state[1])) in best_action:
            return  ((state[0], state[1] + 1), (state[0], state[1]))
        else:
            return random.choice(best_action)

    # Adjust maze to add wall, also remembers whether or not a wall was placed this turn
    def build(self, action):

        if action == None:
            self.built = False
            return
        # Find out if wall is up, down, left or right
        the_number = ((action[0][0] - action[1][0]), (action[0][1] - action[1][1]))

        # Find squares walls are to be built between
        cn1 = self.walls[action[0]]
        cn2 = self.walls[action[1]]

        # If upper wall subtract first square by 4, second by 1. Cap at 0
        if the_number == (0,1):
            cn1 = max(cn1 - 4, 0)
            cn2 = max(cn2 - 1, 0)
        
        # If lower wall subtract first square by 1, second by 4. Cap at 0  
        elif the_number == (0,-1):
            cn1 = max(cn1 - 1, 0)
            cn2 = max(cn2 - 4, 0)
        
        # if right wall subtract first square by 8, second by 2. Cap at 0
        elif the_number == (1,0):
            cn1 = max(cn1 - 8, 0)
            cn2 = max(cn2 - 2, 0)
        
        # if left wall subtract first square by 2, second by 8. Cap at 0

        elif the_number == (-1,0):
            cn1 = max(cn1 - 2, 0)
            cn2 = max(cn2 - 8, 0)

        # Makes sure same wall can't be built twice
        self.available_actions.remove(action)
        self.walls[action[0]] = cn1
        self.walls[action[1]] = cn2
        self.built = True
        return    

    # Calculate reward
    def reward(self, rob_pos, goal, exit, facing):
        space = 0
        build = 0
        if rob_pos[0] == 2:
            if rob_pos[1] == -1:
                space = 1
            elif rob_pos[1] == 4:
                space = -1
            elif rob_pos[1] == 1:
                space = 0.5
            elif rob_pos[1] == 0:
                space = 1
        else:
            space = 0
        if self.built:
            build = 0.01


        return space - build

    # Q function
    def learn(self,state,action,reward):
        if self.learning:
            self.Q[state][action] = (1-self.alpha) * self.Q[state][action] + self.alpha * reward
        return

    # For resetting available walls without resetting Q table
    def reset(self):
        self.available_actions = [None, ((0,0), (0,1)), ((0,1), (0,2)), ((0,2), (0,3)), ((0,3), (0,4)), ((0,4),(1,4)), ((1,4), (2,4)), ((2,4), (3,4)),
         ((3,4), (4,4)), ((4,4), (4,3)), ((4,3), (4,2)), ((4,2), (4,1)), ((4,1), (4,0)), ((4,0), (3,0)), ((3,0), (2,0)), ((2,0), (1,0)),
         ((1,0), (1,1)), ((1,1), (0,1)), ((1,1), (2,1)), ((2,1), (2,0)), ((2,1), (3,1)), ((3,1), (3,0)), ((3,1), (4,1)), ((3,1), (3,2)),
         ((3,2), (4,2)), ((3,2), (2,2)), ((2,2), (2,1)), ((2,2), (1,2)), ((1,2), (1,1)), ((1,2), (0,2)), ((1,2), (1,3)), ((1,3), (0,3)), 
         ((1,3), (1,4)), ((1,3), (2,3)), ((2,3), (2,4)), ((2,3), (2,2)), ((2,3), (3,3)), ((3,3), (3,2)), ((3,3), (3,4)), ((3,3), (4,3))]
        self.epsilon = 0.1
        return 




        