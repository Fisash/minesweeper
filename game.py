import random

class Cell:
    is_mined = False
    is_flagged = False
    is_opened = False

    def __init__(self) -> None:
        pass
    
class Map:
    size = 0
    grid = [[]]

    def __init__(self, size = 16, mine_count = 6):
        self.size = size
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]

        all_cells = [(row, col) for row in range(self.size) for col in range(self.size)]
        cells_to_modify = random.sample(all_cells, min(mine_count, len(all_cells)))
        for row, col in cells_to_modify:
            self.grid[row][col].is_mined = True

    def open_all_mines(self):
        for x in range(0, self.size):
            for y in range(0, self.size):
                if self.grid[x][y].is_mined:
                    self.grid[x][y].is_opened = True

    def is_win(self):
        for x in range(0, self.size):
            for y in range(0, self.size):
                cell = self.grid[x][y]
                if cell.is_opened == False and cell.is_mined == False:
                    return False
        return True
            
    def get_mine_count(self, x, y):
        def is_valid_index(i, j):
            return 0 <= i < self.size and 0 <= j < self.size
        count = sum(1 for nx in range(x-1, x+2) for ny in range(y-1, y+2) if is_valid_index(nx, ny) and self.grid[nx][ny].is_mined)
        return count
    
    def move(self, x, y, flag_setting = False, deep = 0):
        cell = self.grid[x][y]
        if cell.is_opened:
            return 0
        if flag_setting:
            cell.is_flagged = not(cell.is_flagged)
            return 3
        if cell.is_flagged:
            return 4
        if cell.is_mined:
            return 1
        cell.is_opened = True
        if self.is_win():
            return 5
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if not self.grid[nx][ny].is_opened:
                        mine_count = self.get_mine_count(nx, ny)
                        if mine_count <= 5: 
                            self.move(nx, ny, False, deep + 1)
        return 2

    def draw(self):
        print("   a b c d e f g h j k l m n o p q r s t u v w x y z й ъ з б ю ь я э ц "[:(self.size*2)+2])
        for x in range(0, self.size):
            line_text = str(x+1) + ("  " if (x+1) < 10 else " ")
            for y in range(0,self.size):
                cell = self.grid[x][y]
                line_text += (("Б" if cell.is_mined else str(self.get_mine_count(x, y))) if cell.is_opened else ("Ф" if cell.is_flagged else "-")) + " "
            print(line_text)


class Game:
    map = None

    def __init__(self, size, mine_count) -> None:
        self.map = Map(size, mine_count)
    
    def convert_move(self, move):
        ch = move[0]
        num = move[1:]
        return ["abcdefghjklmnopqrstuvwxyzйъзбюьяэц".index(ch), int(num)-1]
    
    def play(self):
        self.map.draw()
        while True:
            i = input("input the move coordinates (if you want to put/remove the flag, enter the 'flag ' before that): ")
            move = self.convert_move(i[len("flag "):] if i.startswith("flag ") else i)
            move_status = self.map.move(move[1], move[0], i.startswith("flag "))
            print("\n")
            if move_status == 1:
                self.map.open_all_mines()
                self.map.draw()
                print("you lose :(")
                return
            elif move_status == 4:
                print("to open this cell, first remove the flag from it")
            elif move_status == 5:
                self.map.draw()
                print("you won :)")
                return
            else:
                self.map.draw()

game = Game(16, 65)
game.play()
