from copy import deepcopy
from heapq import heappop, heappush

class Square:
    def __init__(self, x, y, type, prev_type):
        self.x = x
        self.y = y
        self.type = type
        self.prev_type = prev_type

    def __str__(self):
        if self.type == "empty":
            return '⬜️'
        elif self.type == "color":
            return '🟥'
        elif self.type == "block":
            return '⬛️'
        else:
            return '🔴'

class State:
    def __init__(self, rows, columns, board,parent=None,cost=0):
        self.columns = columns
        self.rows = rows
        self.board = board
        self.parent = parent 
        self.cost=cost

    def __str__(self):
        result = ""
        for row in self.board:
            for square in row:
                result += str(square)
            result += "\n"
        return result

    def __lt__(self, other):
        return self.cost < other.cost
    

    def getColorCoord(self):
     for rows in self.board:
        for square in rows:
            if square.type == 'color':
                return square.x, square.y
     return None
    
    def isGoal(self):
     for row in self.board:
        for square in row:
            if square.type == "target":  
                 return False
     return True  


    def move(self, direction):
        color_x, color_y = self.getColorCoord()
       
        if direction == 'up':
            dx, dy = -1, 0
        elif direction == 'down':
            dx, dy = 1, 0
        elif direction == 'left':
            dx, dy = 0, -1
        elif direction == 'right':
            dx, dy = 0, 1
        else:
            return 0

        while self.checkMove(color_x, color_y, dx, dy):
            new_color_x = color_x + dx
            new_color_y = color_y + dy
            target_square = self.board[new_color_x][new_color_y]

            if target_square.type == "target":
                target_square.type = "empty"
                self.board[color_x][color_y].type = "empty"
                print("Game end")
                return 1

            target_square.prev_type = target_square.type
            target_square.type = "color"
            self.board[color_x][color_y].type = "empty"

            color_x = new_color_x
            color_y = new_color_y

        return 0


    def checkMove(self, color_x, color_y, dx, dy):
        if color_x + dx < 0 or color_x + dx >= self.rows:
            return False
        elif color_y + dy < 0 or color_y + dy >= self.columns:
            return False
        elif self.board[color_x + dx][color_y + dy].type == "block":
            return False
        else:
            return True

    def getAllPossibleMoves(self):
        directions = ["up", "down", "left", "right"]
        children = []

        color_coord = self.getColorCoord()
        if color_coord is None:
            return children

        color_x, color_y = color_coord
        for direction in directions:
            dx, dy = 0, 0
            if direction == "up":
                dx, dy = -1, 0
            elif direction == "down":
                dx, dy = 1, 0
            elif direction == "left":
                dx, dy = 0, -1
            elif direction == "right":
                dx, dy = 0, 1

            new_state = State(
                self.rows,
                self.columns,
                [[Square(sq.x, sq.y, sq.type, sq.prev_type) for sq in row] for row in self.board],
                self,
                self.cost + 1  
            )

            temp_color_x, temp_color_y = color_x, color_y

            while new_state.checkMove(temp_color_x, temp_color_y, dx, dy):
                new_color_x = temp_color_x + dx
                new_color_y = temp_color_y + dy
                target_square = new_state.board[new_color_x][new_color_y]

                if target_square.type == "target":
                    target_square.type = "empty"
                    new_state.board[temp_color_x][temp_color_y].type = "empty"
                    break

                target_square.prev_type = target_square.type
                target_square.type = "color"
                new_state.board[temp_color_x][temp_color_y].type = "empty"

                temp_color_x, temp_color_y = new_color_x, new_color_y

            children.append(new_state)

        return children

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        if self.rows != other.rows or self.columns != other.columns:
            return False
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j].type != other.board[i][j].type:
                    return False
        return True       
    def compare_states(self, state1, state2):
        print("Are states equal?", state1 == state2)

     

class Game:
    def __init__(self, init_state):
        self.init_state = init_state
        self.states = [deepcopy(init_state)]  
        
    
    def print_all_states(self):
        print("\nAll Stored States:\n")
        for index, state in enumerate(self.states):
            print(f"State {index + 1}:")
            print(state)
    
    def print_path(self, state):
        path = []
        while state:
            path.append(state)
            state = state.parent
        path.reverse()  
        for index, s in enumerate(path):
            print(f"Step {index + 1}:\n{s}")


    def ucs(self):
        priority_queue = []
        visited = set()    
        heappush(priority_queue, (0, self.init_state))  
        while priority_queue:
            current_cost, current_state = heappop(priority_queue)
            if current_state.isGoal():
                print("Goal Found with Cost:", current_cost)
                self.print_path(current_state)
                return

            if str(current_state) in visited:
                continue
            visited.add(str(current_state))

            for move in current_state.getAllPossibleMoves():
                move.parent = current_state
                heappush(priority_queue, (move.cost, move))  

        print("Goal not found")
    
        
    def start(self):
        while not self.init_state.isGoal():
            print('Enter 8 5 4 6 , for up, down, left, right')
            user_input = input()
            if user_input == '8':
                self.init_state.move('up')
            elif user_input == '5':
                self.init_state.move('down')
            elif user_input == '6':
                self.init_state.move('right')
            elif user_input == '4':
                self.init_state.move('left')
            else:
                print('Please type 8, 6, 5, or 4 to move.\n')
                
            
            previous_state = deepcopy(self.states[-1])

            self.states.append(deepcopy(self.init_state))

            print("Current State:")
            print(self.init_state) 
            self.print_all_states()
            children = self.init_state.getAllPossibleMoves()
            print("Possible moves:")
            for state in children:
                if not state ==self.init_state:
                 print(state)
            self.init_state.compare_states(previous_state, self.init_state)
    
    
def main():
    board_1 = [
        ["⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬜️", "⬜️", "⬜️"],
        ["⬛️", "⬜️", "⬜️", "🔴", "⬜️", "⬛️", "⬛️", "⬜️", "⬜️"],
        ["⬛️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬛️", "⬛️", "⬛️"],
        ["⬛️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "🟥", "⬛️"],
        ["⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️"],
    ]
    rows = len(board_1)
    columns = len(board_1[0])

    board = [[None for b in range(columns)] for b in range(rows)]

    for i in range(rows):
        for j in range(columns):
            if board_1[i][j] == '🟥':
                square_type = "color"
            elif board_1[i][j] == '🔴':
                square_type = "target"
            elif board_1[i][j] == '⬜️':
                square_type = "empty"
            else:
                square_type = "block"
            prev_type = square_type
            if square_type == "color":
                prev_type = '⬜️'
            board[i][j] = Square(i, j, square_type, prev_type)

    init_state = State(rows, columns, board,None,0)
    print("Initial State:")
    print(init_state)
    game = Game(init_state)
    game.ucs() 


if __name__ == "__main__":
    main()
