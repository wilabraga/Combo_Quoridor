from queue import PriorityQueue

class Quoridor():
    # Board: 0 - empty, 1 - player, 2 - wall
    # Players can only move to even values of i/j
    # Walls can be placed on all other spaces where players cannot move
    def __init__(self, n):
        self.n = n
        self.board = [[0 for i in range(n * 2 - 1)] for j in range(n * 2 - 1)]
        self.board[0][n - 1] = 1
        self.cpu = {"position": (0, n - 1), "walls": (n + 1)}
        self.board[n * 2 - 2][n - 1] = 1
        self.player = {"position": (n * 2 - 2, n - 1), "walls": (n + 1)}
        self.turn = True

    def print_board(self):
        st = ""
        for row in self.board:
            for cell in row:
                st += str(cell) + " "
            st += "\n"
        print(st)

    def get_movements(self, coords):
        x_dir = [-2, 0, 2, 0]
        y_dir = [0, -2, 0, 2]
        movements = []
        for i in range(0, len(x_dir)):
            pos = (coords[0] + x_dir[i], coords[1] + y_dir[i])
            wall = (coords[0] + x_dir[i] // 2, coords[1] + y_dir[i] // 2)
            if self.in_bounds(pos):
                if not self.is_wall(wall):
                    if self.board[pos[0]][pos[1]] == 0:
                        movements.append(pos)
                    # Face to Face
                    # 1. If no wall behind opposing player, jump over them
                    # 2. If wall behind player, go to left or right of player (depending on walls)
                    else:
                        new_pos = (pos[0] + x_dir[i], pos[1] + y_dir[i])
                        wall = (pos[0] + x_dir[i] // 2, pos[1] + y_dir[i] // 2)
                        # Condition 1
                        if self.in_bounds(new_pos) and not self.is_wall(wall):
                            movements.append(new_pos)
                        # Condition 2
                        else:
                            # Direction 1
                            new_pos = (pos[0] + y_dir[i], pos[1] + x_dir[i])
                            wall = (pos[0] + y_dir[i] // 2, pos[1] + x_dir[i] // 2)
                            if self.in_bounds(new_pos) and not self.is_wall(wall):
                                movements.append(new_pos)
                            # Direction 2
                            new_pos = (pos[0] - y_dir[i], pos[1] - x_dir[i])
                            wall = (pos[0] - y_dir[i] // 2, pos[1] - x_dir[i] // 2)
                            if self.in_bounds(new_pos) and not self.is_wall(wall):
                                movements.append(new_pos)
        return movements

    def in_bounds(self, coords):
        return 0 <= coords[0] < len(self.board) and 0 <= coords[1] < len(self.board)

    def is_wall(self, coords):
        return self.board[coords[0]][coords[1]] == 2

    def get_walls(self, coords, turn):
        num_walls = self.player['walls']
        if not turn:
            num_walls = self.cpu['walls']
        walls = []
        if num_walls <= 0:
            return walls
        for i in range(0, len(self.board) - 1):
            for j in range(0, len(self.board) - 1):
                if not ((i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j > len(self.board) - 3)):
                    wall = (i, j)
                    # i is odd: wall is vertical; i is even: wall is horizontal
                    add = [0, 1]
                    if i % 2 == 0:
                        add = [1, 0]
                    # Wall not already placed
                    if not self.is_wall(wall) and not self.is_wall((wall[0] + 2 * add[0], wall[1] + 2 * add[1])):
                        self.board[wall[0]][wall[1]] = 2
                        self.board[wall[0] + add[0]][wall[1] + add[1]] = 2
                        self.board[wall[0] + 2 * add[0]][wall[1] + 2 * add[1]] = 2
                        cpu_dist = self.astar(self.cpu["position"], self.n * 2 - 2)
                        player_dist = self.astar(self.player["position"], 0)
                        # Check if any player would get trapped
                        if cpu_dist != -1 and player_dist != -1:
                            walls.append(wall)
                        self.board[wall[0]][wall[1]] = 0
                        self.board[wall[0] + add[0]][wall[1] + add[1]] = 0
                        self.board[wall[0] + 2 * add[0]][wall[1] + 2 * add[1]] = 0
        return walls

    def astar(self, coords, goal):
        queue = PriorityQueue()
        visited = []
        queue.put((0, 0, coords))
        x_dir = [-2, 0, 2, 0]
        y_dir = [0, -2, 0, 2]
        while queue.qsize() > 0:
            current = queue.get()
            g = current[1]
            curr = current[2]
            visited.append(curr)
            for i in range(0, len(x_dir)):
                pos = (curr[0] + x_dir[i], curr[1] + y_dir[i])
                wall = (curr[0] + x_dir[i] // 2, curr[1] + y_dir[i] // 2)
                if self.in_bounds(pos) and not self.is_wall(wall):
                    if pos not in visited and self.board[pos[0]][pos[1]] == 0:
                        dist = abs(goal - pos[0])
                        if pos[0] == goal:
                            return g + 1
                        queue.put((g + dist + 1, g + 1, pos))
                    # Face to Face
                    elif self.board[pos[0]][pos[1]] == 1:
                        new_pos = (pos[0] + x_dir[i], pos[1] + y_dir[i])
                        wall = (pos[0] + x_dir[i] // 2, pos[1] + y_dir[i] // 2)
                        if self.in_bounds(new_pos) and not self.is_wall(wall) and new_pos not in visited:
                            dist = abs(goal - new_pos[0])
                            if new_pos[0] == goal:
                                return g + 1
                            queue.put((g + dist + 1, g + 1, new_pos))
                        # Condition 2
                        else:
                            # Direction 1
                            new_pos = (pos[0] + y_dir[i], pos[1] + x_dir[i])
                            wall = (pos[0] + y_dir[i] // 2, pos[1] + x_dir[i] // 2)
                            if self.in_bounds(new_pos) and not self.is_wall(wall) and new_pos not in visited:
                                dist = abs(goal - new_pos[0])
                                if new_pos[0] == goal:
                                    return g + 1
                                queue.put((g + dist + 1, g + 1, new_pos))
                            # Direction 2
                            new_pos = (pos[0] - y_dir[i], pos[1] - x_dir[i])
                            wall = (pos[0] - y_dir[i] // 2, pos[1] - x_dir[i] // 2)
                            if self.in_bounds(new_pos) and not self.is_wall(wall) and new_pos not in visited:
                                dist = abs(goal - new_pos[0])
                                if new_pos[0] == goal:
                                    return g + 1
                                queue.put((g + dist + 1, g + 1, new_pos))
        return -1


    # 0 (False) - CPU, 1 (True) - player
    def get_successors(self, turn):
        coords = self.player['position']
        if not turn:
            coords = self.cpu['position']
        actions = {"movements": self.get_movements(coords), "walls": self.get_walls(coords, turn)}
        return actions

game = Quoridor(9)
game.print_board()
print(game.get_successors(True))
print(game.get_successors(False))