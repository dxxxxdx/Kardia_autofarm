
import logging
import math
import time
from selarm_recongnize import *
import keyboard
import core.recongnize_process as rp

class BoardGird:
    def __init__(self,gird_num):
        self.girdx = 0
        self.girdy = 0
        self.gird_num = gird_num

    def set_gird_num(self, gird_num):
        #logging.debug(f"Setting grid number: {gird_num}")
        self.gird_num = gird_num

class SlimeRecongnizeResult:
    def __init__(self, windows_pos, num):
        self.windows_pos = windows_pos
        self.num = num

# noinspection DuplicatedCode,PyMethodMayBeStatic
class Game2048Board:
    #类变量
    slime_martix = []
    board_center = []
    gird_board = []



    def __init__(self):
        #logging.debug("Initializing Game2048Board...")
        #logging.debug(f"Board center initialized: {self.boardcenter}")
        self.slime_martix = [[BoardGird(-1) for _ in range(4)] for _ in range(4)]


    def print_board(self):
        #logging.debug("Printing board (Rotated 90° Counterclockwise + Inverted Rows)...")
        board_state = [[cell.gird_num for cell in row] for row in self.slime_martix]
        rotated = list(zip(*board_state))[::-1]  # 转置并翻转行顺序
        print("\n=== Rotated 90° Counterclockwise + Inverted Rows ===")
        for row in reversed(rotated):  # 反转行顺序
            print(list(row))

    def move_up(self, board):
        """调整后的 UP 操作：对应原始棋盘的 LEFT"""
        for row in range(4):
            tiles = [board[row][col] for col in range(4) if board[row][col] != 0]  # 提取非零值
            for i in range(len(tiles) - 1):
                if tiles[i] == tiles[i + 1]:  # 合并相同数字
                    tiles[i] *= 2
                    tiles[i + 1] = 0
            tiles = [tile for tile in tiles if tile != 0]  # 去掉合并后的 0
            for col in range(4):
                board[row][col] = tiles[col] if col < len(tiles) else 0
        return board

    def move_down(self, board):
        """调整后的 DOWN 操作：对应原始棋盘的 RIGHT"""
        for row in range(4):
            tiles = [board[row][col] for col in range(4) if board[row][col] != 0]
            for i in range(len(tiles) - 1, 0, -1):
                if tiles[i] == tiles[i - 1]:  # 合并相同数字
                    tiles[i] *= 2
                    tiles[i - 1] = 0
            tiles = [tile for tile in tiles if tile != 0]
            for col in range(4):
                board[row][3 - col] = tiles[col] if col < len(tiles) else 0
        return board

    def move_left(self, board):
        """调整后的 LEFT 操作：对应原始棋盘的 UP"""
        for col in range(4):
            tiles = [board[row][col] for row in range(4) if board[row][col] != 0]
            for i in range(len(tiles) - 1):
                if tiles[i] == tiles[i + 1]:
                    tiles[i] *= 2
                    tiles[i + 1] = 0
            tiles = [tile for tile in tiles if tile != 0]
            for row in range(4):
                board[row][col] = tiles[row] if row < len(tiles) else 0
        return board

    def move_right(self, board):
        """调整后的 RIGHT 操作：对应原始棋盘的 DOWN"""
        for col in range(4):
            tiles = [board[row][col] for row in range(4) if board[row][col] != 0]
            for i in range(len(tiles) - 1, 0, -1):
                if tiles[i] == tiles[i - 1]:
                    tiles[i] *= 2
                    tiles[i - 1] = 0
            tiles = [tile for tile in tiles if tile != 0]
            for row in range(4):
                board[3 - row][col] = tiles[row] if row < len(tiles) else 0
        return board

    def find_best_move(self):
        moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        best_move = None
        max_score = -1

        #logging.debug("Evaluating best move...")
        for move in moves:
            #logging.debug(f"Simulating move: {move}")
            temp_board = self.simulate_move(move)
            score = self.evaluate_board(temp_board)
            #logging.debug(f"Move: {move}, Score: {score}")
            if score > max_score:
                max_score = score
                best_move = move

        #logging.info(f"Best move determined: {best_move}")
        # 打印预期结果的棋盘
        print("\n=== Simulated Board After Best Move ===")
        self.print_simulated_board(best_move)
        return best_move

    def simulate_move(self, move):
        temp_matrix = [[cell.gird_num for cell in row] for row in self.slime_martix]
        if move == 'UP':
            temp_matrix = self.move_up(temp_matrix)
        elif move == 'DOWN':
            temp_matrix = self.move_down(temp_matrix)
        elif move == 'LEFT':
            temp_matrix = self.move_left(temp_matrix)
        elif move == 'RIGHT':
            temp_matrix = self.move_right(temp_matrix)
        return temp_matrix

    def print_simulated_board(self, move):
        temp_matrix = self.simulate_move(move)
        # 先逆时针旋转90°
        rotated = list(zip(*temp_matrix))[::-1]  # 转置并反转行顺序
        adjusted = [list(row) for row in reversed(rotated)]
        print(f"\n=== Simulated Board After Move: {move} ===")
        for row in adjusted:
            print(row)

    def evaluate_board(self, board):
        empty_cells = sum(row.count(0) for row in board)
        max_tile = max(max(row) for row in board)
        score = empty_cells * 10 + max_tile
        ##logging.debug(f"Evaluating board: Empty cells={empty_cells}, Max tile={max_tile}, Score={score}")
        return score

    def update(self):
        #logging.info("Updating board...")
        slime_list = list_files_in_directory(find_folder("2048_lib"))
        #logging.debug(f"Found slime files: {slime_list}")
        self.cleaning()
        temps = []
        recongnize_res = []
        find_img_or("update")
        time.sleep(0.05)
        try:
            ignore_area = find_img_or(fpth_selarm("2048_ignore",sub_path="game_board"))[0]
        except IndexError:
            ignore_area = None
            pass
        if ignore_area:
            print(ignore_area)

        for slime in slime_list:
            temp = find_img_or(slime)
            #logging.debug(f"Recognized positions for {slime}: {temp}")
            temps.append(temp)
            if temp is not None:
                for i in temp:
                    distance = math.sqrt((ignore_area[0] - i[0]) ** 2 + (ignore_area[1] - i[1]) ** 2)
                    if distance > 160:
                        recongnize_res.append(SlimeRecongnizeResult(i, get_num_by_slime_path(slime)))
                    else:
                        pass

        # Process grid boundaries
        minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')
        for j in temps:
            if j is not None:
                for k in j:
                    minx = min(minx, k[0])
                    miny = min(miny, k[1])
                    maxx = max(maxx, k[0])
                    maxy = max(maxy, k[1])
        ##logging.debug(f"Grid boundaries determined: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")
        self.gird_board = [minx, miny, maxx, maxy]
        self.set_center(self.gird_board)
        print(self.board_center)

        # Update game state
        for i in recongnize_res:
            gird_pos = match_grid(i.windows_pos, (minx, miny, maxx, maxy))
            ##logging.debug(f"Matching grid position for {i.windows_pos}: {gird_pos}")
            self.slime_martix[gird_pos[0]][gird_pos[1]].set_gird_num(i.num)

        for i in self.slime_martix:
            for j in i:
                if j is None:
                    print("Grid is not    complete!    ")
                    return False

        #logging.info("Board updated successfully!")
        return True


    def is_complete(self):
        for i in self.slime_martix:
            for j in i:
                if j.gird_num <= 0:
                    return False

    def cleaning(self):
        for i in self.slime_martix :
            for j in i:
                j.gird_num = -1

    def set_center(self,gird_board):
        self.gird_board = gird_board
        self.board_center = [gird_board[2]-gird_board[0], gird_board[3]-gird_board[1]]






def get_num_by_slime_path(slime_path):
    name = os.path.basename(slime_path)
    numbers = re.findall(r'\d+', name)
    if numbers:
        num = int(numbers[0])
        ##logging.debug(f"Extracted number from {slime_path}: {num}")
        return num
    ##logging.warning(f"No number found in {slime_path}")
    return 0


def get_name_by_path(pathx):
    name = os.path.basename(pathx)
    name = os.path.splitext(name)[0]
    return name


def find_img_or(tarpath):
    a = rp.operate(tarpath,"e",single_find=False,ingray=False,return_centers=True,threshold=0.9)
    return a

if __name__ == '__main__':
    rp.recongnize_process()
    rp.update_scr()
    game = Game2048Board()
    def update_event(event):
        game.update()
        #logging.info("Update event triggered.")
        game.print_board()
        print(game.find_best_move())
        print("___________________________")
        board_center = game.board_center


    def test(event):
        find_img_or(fpth_selarm("slime_4", sub_path="2048_lib"))

    keyboard.on_press_key("ctrl", update_event)
    while True:
        pass
