# Filename: 112301044.py
# Name = Rajat Bhootra
# Roll No. = 112301044

class YantraCollector:
    """
    YantraCollector class to solve the yantra collection puzzle.
    The player must collect all yantras sequentially and reach the exit.
    """
    
    def __init__(self, grid):
        """
        Initializes the game with the provided grid.

        Args:
            grid (list of list of str): The grid representing the puzzle.
        """
        self.grid = grid
        self.n = len(grid)
        self.start = self.find_position('P')
        self.exit = None
        self.yantras = self.find_all_yantras()
        self.revealed_yantra = self.find_position('Y1')
        self.collected_yantras = 0
        self.total_frontier_nodes = 0
        self.total_explored_nodes = 0
        
    def find_position(self, symbol):
        """
        Finds the position of a given symbol in the grid.

        Args:
            symbol (str): The symbol to locate.

        Returns:
            tuple or None: The position of the symbol, or None if not found.
        """
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == symbol:
                    return (i, j)
        return None

    def find_all_yantras(self):
        """
        Finds and stores the positions of all yantras in the grid.

        Returns:
            dict: A dictionary mapping yantra numbers to their positions.
        """
        positions = {}
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j].startswith('Y'):
                    positions[int(self.grid[i][j][1:])] = (i, j)
                elif self.grid[i][j] == 'E':
                    self.exit = (i, j)
        return positions

    def reveal_next_yantra_or_exit(self):
        """
        Reveals the next yantra in sequence or the exit when all yantras are collected.
        """
        self.collected_yantras += 1
        if self.collected_yantras + 1 in self.yantras:
            self.revealed_yantra = self.yantras[self.collected_yantras + 1]
        elif self.collected_yantras == len(self.yantras):
            self.revealed_yantra = self.exit
        else:
            self.revealed_yantra = None

    def goal_test(self, position):
        """
        Checks if the given position matches the currently revealed yantra or exit.

        Args:
            position (tuple): The current position to check.
        """
        #check if the current position is goal state or not.
        
        if position == self.revealed_yantra :
            return True
        else :
            return False


    def get_neighbors(self, position):
        """
        Generates valid neighboring positions for the given position.

        Args:
            position (tuple): The current position of the player.
        """
        neighbors = [] #empty list to store neighbors
        directions = [(-1,0), (0,1), (1,0), (0,-1)] #to move in N, E, S, W direction
        
        x,y = position
        
        for dx, dy in directions: 
        
            nx, ny= x+dx, y+dy
        
            # check for the boundary condition and also for Walls and Traps.
            if 0<=nx<self.n and 0<=ny<self.n and self.grid[nx][ny] != '#' and self.grid[nx][ny] != 'T':
                neighbors.append((nx,ny))    
        
        return neighbors
           
    def bfs(self, start, goal):
        """
        Performs Breadth-First Search (BFS) to find the path to the goal.

        Args:
            start (tuple): The starting position.
            goal (tuple): The goal position.
        """
        path_lst = [[start]]  #list for keeping track of the path to goal.
       
        frontier_lst = [start] #list for expansion.
        self.total_frontier_nodes += 1 
       
        explored_lst = [] #list for node which have been explored.
        
        #starting BFS search.
        while path_lst :
            path = path_lst.pop(0)
            current = frontier_lst.pop(0)
            self.total_frontier_nodes -= 1
            
            explored_lst.append(current)
            self.total_explored_nodes += 1
              
            if self.goal_test(current):
                return path

            
            for neighbor in self.get_neighbors(current):
                if neighbor not in frontier_lst and neighbor not in explored_lst:
                    
                    new_path = path + [neighbor]
                    path_lst.append(new_path)
                    
                    frontier_lst.append(neighbor)
                    self.total_frontier_nodes += 1
                    
        return None


    def dfs(self, start, goal):
        """
        Performs Depth-First Search (DFS) to find the path to the goal.

        Args:
            start (tuple): The starting position.
            goal (tuple): The goal position.

        Returns:
            tuple: The path to the goal, frontier count, and explored count.
        """
        path_lst = [[start]]  #list for keeping track of the path to goal.
        
        frontier_lst = [start]  #list for expansion.
        self.total_frontier_nodes += 1
        
        explored_lst = [] #list for node which have been explored.
        
        #starting DFS search.
        while path_lst:
            path = path_lst.pop(0)
            current = frontier_lst.pop(0)
            self.total_frontier_nodes -= 1
        
            explored_lst.append(current)
            self.total_explored_nodes += 1

            if self.goal_test(current):
                return path 
     
            for neighbor in reversed(self.get_neighbors(current)):
                if neighbor not in explored_lst and neighbor not in frontier_lst:
                    new_path = path + [neighbor]
                    path_lst.insert(0, new_path)
                    frontier_lst.insert(0, neighbor)
                    self.total_frontier_nodes += 1        
        
        return None
        
    def solve(self, strategy):
        """
        Solves the yantra collection puzzle using the specified strategy.

        Args:
            strategy (str): The search strategy (BFS or DFS).
        """
        current_position = self.start 
        solution_path = [self.start]

        while self.revealed_yantra :
            if strategy == "BFS" :          
               path = self.bfs(current_position, self.revealed_yantra)
            elif strategy == "DFS" :
               path = self.dfs(current_position, self.revealed_yantra)
            else :
               print("Unsupported startegy!!!")       
             
            if not path:
               return None, self.total_frontier_nodes, self.total_explored_nodes
            
            solution_path.extend(path[1:])
            current_position = self.revealed_yantra
            self.reveal_next_yantra_or_exit()
             
        return solution_path, self.total_frontier_nodes, self.total_explored_nodes           
       
if __name__ == "__main__":

    grid = [
        ['P', '.', '.', '#', 'Y2'],
        ['#', 'T', '.', '#', '.'],
        ['.', '.', 'Y1', '.', '.'],
        ['#', '.', '.', 'T', '.'],
        ['.', '.', '.', '.', 'E']
    ]
    
    game = YantraCollector(grid)
    strategy = "DFS"  # or "DFS"
    solution, total_frontier, total_explored = game.solve(strategy)
    if solution:
        print("Solution Path:", solution)
        print("Total Frontier Nodes:", total_frontier)
        print("Total Explored Nodes:", total_explored)
    else:
        print("No solution found.")
