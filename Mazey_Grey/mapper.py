import numpy as np
import pprint
pp = pprint.PrettyPrinter()

class Mapper(object):
	def __init__(self, filename):
		with open(filename, 'rb') as f_in:
			self.dim = int(f_in.next())
			walls = []
			for line in f_in:
				walls.append(map(int,line.split(',')))
			self.walls = np.array(walls)

		wall_errors = []

		for x in range(self.dim-1):
			for y in range(self.dim):
				if (self.walls[x,y] & 2 != 0) != (self.walls[x+1,y] & 8 != 0):
					wall_errors.append([(x,y), 'v'])
		for y in range(self.dim-1):
			for x in range(self.dim):
				if (self.walls[x,y] & 1 != 0) != (self.walls[x,y+1] & 4 != 0):
					wall_errors.append([(x,y), 'h'])
		if wall_errors:
			for cell, wall_type in wall_errors:
				if wall_type == 'v':
					cell2 = (cell[0]+1, cell[1])
					print 'Inconsistent vertical wall betweeen {} and {}'.format(cell, cell2)
				else:
					cell2 = (cell[0], cell[1]+1)
					print 'Inconsistent horizontal wall betweeen {} and {}'.format(cell, cell2)
			raise Exception('Consistency errors found in wall specifications!')

	def is_permissible(self, cell, direction):
		dir_int = {'u': 1, 'r': 2, 'd': 4, 'l': 8,
                   'up': 1, 'right': 2, 'down': 4, 'left': 8}
                try:
                  return (self.walls[tuple(cell)] & dir_int[direction] != 0)
                except:
                  print 'Invalid direction provided!'
