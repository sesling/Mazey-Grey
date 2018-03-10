from maze import Maze
from robot import Robot
from mapper import Mapper
import pprint
import numpy as np
import sys

# Robot Abilities
dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
               'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
               'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
               'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
            'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
               'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}

# Possible squares for walls to be built between
valid_actions = [None,((0,0), (0,1)), ((0,1), (0,2)), ((0,2), (0,3)), ((0,3), (0,4)), ((0,4),(1,4)), ((1,4), (2,4)), ((2,4), (3,4)),
         ((3,4), (4,4)), ((4,4), (4,3)), ((4,3), (4,2)), ((4,2), (4,1)), ((4,1), (4,0)), ((4,0), (3,0)), ((3,0), (2,0)), ((2,0), (1,0)),
         ((1,0), (1,1)), ((1,1), (0,1)), ((1,1), (2,1)), ((2,1), (2,0)), ((2,1), (3,1)), ((3,1), (3,0)), ((3,1), (4,1)), ((3,1), (3,2)),
         ((3,2), (4,2)), ((3,2), (2,2)), ((2,2), (2,1)), ((2,2), (1,2)), ((1,2), (1,1)), ((1,2), (0,2)), ((1,2), (1,3)), ((1,3), (0,3)), 
         ((1,3), (1,4)), ((1,3), (2,3)), ((2,3), (2,4)), ((2,3), (2,2)), ((2,3), (3,3)), ((3,3), (3,2)), ((3,3), (3,4)), ((3,3), (4,3))]

# Miscellaneous Stuff
max_time = 10
pp = pprint.PrettyPrinter()

# This is used for encoding the current state
def get_state(rob_pos, heading, color):
    state = (rob_pos[0], rob_pos[1], heading, color)
    return state

# This is for figuring out if there's a wall in front of the robot
def wall_sense(cell, direction):

    walled = False

    if not testmaze.is_permissible(cell, direction):
        walled = True
    return walled

if __name__ == '__main__':

    # Initialize the blank 'maze.' Requires test_maze_01 template included in file
    testmap = Mapper(str(sys.argv[1]))


    # Intitialize Mazey herself
    testmaze = Maze(testmap.walls)

    for run in range(60000):
    	# Fresh robot every run, with a random color
        testrobot = Robot()
        # Reset maze to empty configuration without resetting Qtable
        testmaze.walls = np.copy(testmap.walls)
        # Reset Mazey's valid actions without resetting Qtable
        testmaze.reset()
        # Adjust exploration factor as runs apporach 60,000
        if run > 5000 and run < 10000:
            testmaze.epsilon = 0.2
        if run > 10000 and run < 15000:
            testmaze.epsilon = 0.3
        if run > 15000 and run < 20000:
            testmaze.epsilon = 0.4
        if run > 20000 and run < 25000:
            testmaze.epsilon = 0.5
        if run > 25000 and run < 30000:
            testmaze.epsilon = 0.6
        if run > 30000 and run < 35000:
            testmaze.epsilon = 0.7
        if run > 35000 and run < 40000:
            testmaze.epsilon = 0.8
        if run > 40000 and run < 45000:
            testmaze.epsilon = 0.9
        if run > 45000:
            testmaze.epsilon = 1
        if run > 50000:
            testmaze.learning = False

        total_time = 0
        print "Starting run {}.".format(run)

        # Robot enters maze, goal and exit established
        robot_pos = {'location': [2, 0], 'heading': 'u'}
        goal_bounds = [2, 4]
        exit_bounds = [2, -1]
        run_active = True
        hit_goal = False
        robot_exit = False

        while run_active:

        	# time checking
            total_time += 1
            if total_time > max_time:
                print "Allotted time exceeded."
                break
            # robot sees if its blocked or not, so it can react accordingly
            testrobot.walled = wall_sense(robot_pos['location'], robot_pos['heading'])
            # Mazey looks up/adds state to Qtable
            state = get_state(robot_pos['location'], robot_pos['heading'], testrobot.color)
            testmaze.Qtable(state)
            # Mazey finds highest Q value in table for given state
            maxQ = testmaze.bestQ(state)
            # Takes action associated with Q value
            action = testmaze.choose_action(state, maxQ)
            # Lets you know which action was taken for a state
            print state
            print action
            # Action taken; wall built
            testmaze.build(action)
            # Robot checks again to see if its walled
            testrobot.walled = wall_sense(robot_pos['location'], robot_pos['heading'])
            # Robot makes its move based on color and walled status
            rotation, movement = testrobot.next_move()
            # perform rotation
            if rotation == -90:
                robot_pos['heading'] = dir_sensors[robot_pos['heading']][0]
                print "robot rotates left"
            elif rotation == 90:
                robot_pos['heading'] = dir_sensors[robot_pos['heading']][2]
                print "robot rotates right"
            elif rotation == 0:
                pass
            else:
                print "Invalid rotation value, no rotation performed."

            # perform movement
            if abs(movement) > 3:
                print "Movement limited to three squares in a turn."
            movement = max(min(int(movement), 3), -3) # fix to range [-3, 3]
            while movement:
            # block robot from moving if its walled  
                if testmaze.is_permissible(robot_pos['location'], robot_pos['heading']):
                    robot_pos['location'][0] += dir_move[robot_pos['heading']][0]
                    robot_pos['location'][1] += dir_move[robot_pos['heading']][1]
                    movement -= 1
                    print "moved once"
                  
                else:
                    print "Movement stopped by wall."
                    movement = 0

            # Calulate reward
            reward = testmaze.reward(robot_pos['location'], goal_bounds, exit_bounds, robot_pos['heading'])
            # See where robot ended up
            newstate = get_state(robot_pos['location'], robot_pos['heading'], testrobot.color)
            # adjust reward based on highest Q value obtainable from new state
            testmaze.Qtable(newstate)
            maxQ = testmaze.bestQ(newstate)
            newaction = testmaze.choose_action(newstate, maxQ)
            reward += testmaze.Q[newstate][newaction]
            # Perfrom Q function
            testmaze.learn(state, action, reward)

            # check for goal entered
            if robot_pos['location'][0] == goal_bounds[0] and robot_pos['location'][1] == goal_bounds[1]:
                hit_goal = True
                run_active = False
                print "Goal found, too bad"
            #check for robot exited
            if robot_pos['location'][0] == exit_bounds[0] and robot_pos['location'][1] == exit_bounds[1]:
                robot_exit = True
                run_active = False
                print "Robby left. GJ Agent Mazey"
                # Print maze layout if successful
                print testmaze.walls
    # print the final Q table for the first state after all is said and done
    pp.pprint(testmaze.Q[(2, 0, 'u', 0)])
    