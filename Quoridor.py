class Quoridor():
    # Board: 0 - empty, 1 - player, 2 - wall
    # Players can only move to even values of i/j
    # Walls can be placed on all other spaces where players cannot move
    def __init__(self, n):
        self.n = n
        self.board = [[0 for i in range(n * 2 - 1)] for j in range(n * 2 - 1)]
        self.board[0][n - 1] = 1
        self.cpu = {"position": (0, (n - 1)), "walls": (n + 1)}
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
        for i in range(0, len(self.board) - 2):
            for j in range(0, len(self.board) - 2):
                wall = (i, j)
                second = self.board[i][j + 1]
                if i % 2 == 1:
                    second = self.board[i + 1][j]
                # Wall not already placed
                if not self.is_wall(wall) and not self.is_wall(second):
                    self.board[wall[0]][wall[1]] = 2
                    self.board[second[0]][second[1]] = 2

            # Odd: Horizontal Walls

    def shortest_path(self, coords, turn):
        

    # 0 - CPU, 1 - player
    def get_successors(self, turn):
        coords = self.player['position']
        if not turn:
            coords = self.cpu['position']
        actions = {"movements": self.get_movements(coords), "walls": self.get_walls(coords, turn)}
        return actions

game = Quoridor(5)
game.print_board()
print(game.get_successors(1))