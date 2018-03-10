import numpy as np
import random

class Robot(object):
    def __init__(self):

        self.walled = False
        self.color = random.randrange(4)
        self.moved = False
    def next_move(self):
            
        if self.color == 0:
            if self.walled == False:
                rotation = 0
                movement = 1
            else:
                rotation = 90
                movement = 0

        elif self.color == 1:
            if self.walled == False:
                rotation = 0
                movement = 1    
            else:
                rotation = -90
                movement = 0
        elif self.color == 2:
            if self.walled == False:
                rotation = 0
                movement = 1
            else:
                rotation = -90
                movement = 1
        elif self.color == 3:
            if self.walled == False:
                rotation = 0
                movement = 1
            else:
                rotation = 90
                movement = 1

        return rotation, movement
        