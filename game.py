from grid import Grid
from blocks import *
import random
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block() #khối hiện tại
        self.next_block = self.get_random_block()   # khối tiếp theo
        self.game_over = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound("./Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("./Sounds/Sounds_clear.ogg")
        # Lấy nhạc từ file
        pygame.mixer.music.load("./Sounds/sold_out.mp3")
        pygame.mixer.music.set_volume(0.05)
        # Lặp lại vô hạn khi chạy
        pygame.mixer.music.play(-1)
    # Cập nhật điểm(số hàng hoàn thành, điểm cộng khi di chuyển khối xuống)
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 1000
        self.score += move_down_points 
    # Lấy ngẫu nhiên một khối trong các khối
    def get_random_block(self):
        # Khi xóa hết các block thì gán lại như ban đầu
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        # Sau khi lấy thì xóa block để tránh lặp lại block trong lần sau
        self.blocks.remove(block)
        return block
    
    def move_left(self): #sang trái
        self.current_block.move(0, -1)
        # Nếu khối nằm ngoài màn hình hoặc chiếm vị trị của khối khác thì về như cũ (đứng yên)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0,1)
    def move_right(self): #sang phải
        self.current_block.move(0, 1)
        # Nếu khối nằm ngoài màn hình hoặc chiếm vị trí của khối khác thì về như cũ (đứng yên)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0,-1)
    def move_down(self):
        self.current_block.move(1, 0)
        # Nếu khối nằm ngoài màn hình hoặc chiếm vị trí của khối khác thì về như cũ (đứng yên)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1,0)
            self.lock_block()
    # hàm này làm cho khối khi chạm đáy màn hình thì khối sẽ bị dừng không điều khiển đươc nữa 
    def lock_block(self):
        # Lấy ra vị trí các ô tạo nên khối hiện tại
        tiles = self.current_block.get_cell_positions()
        # Duyệt qua các vị trí đó
        for position in tiles:
            # Gán các vị trí đó lên lưới của màn hình làm cho nó nằm yên ở đáy màn hình(id: cho biết khối đó là khối gì)
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block #khối hiện tại sẽ được gán bằng khối tiếp theo
        self.next_block = self.get_random_block() #khối tiếp theo sẽ được random ra khối mới
        rows_cleared = self.grid.clear_full_rows() #Duyệt qua tất cả hàng và kiểm tra xem hoàn thành hay chưa
        # Nếu có dòng hoàn thành thì phát ra âm thanh
        if rows_cleared > 0:
            self.clear_sound.play()
        # cộng điểm dựa vào số dòng
        self.update_score(rows_cleared, 0)
        # Nếu khối mới được tạo ra và không còn chỗ chứa thì game_over == True
        if self.block_fits() == False:
            self.game_over = True

    # Reset lại game khi thua
    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    # Kiểm tra xem khối có chiếm vị trí đã có không
    def block_fits(self):
        # Lấy ra tất cả các ô của khối
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            # Nếu ô của khối chiếm vị trí đã có thì False ngược lại thì True
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    # Hàm xoay khối
    def rotate(self):
        self.current_block.rotate()
        # Nếu khối nằm ngoài màn hình hoặc khi xoay thì chiếm vị của khối khác thì không xoay được
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:#Nếu xoay khối thì phát ra âm thanh
            self.rotate_sound.play()

    # Kiểm tra xem khối có nằm ngoài màn hình không
    def block_inside(self):
        # Lấy ra vị trí các ô của khối
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            # Nếu có ô nằm ngoài màn hình thì return False
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        # Sau khi duyệt qua hết các ô và tất cả chúng nằm trong màn hình thì return True
        return True
        
    def draw(self, screen):
        self.grid.draw(screen) #vẽ lưới cho màn hình
        # Nếu khối được sinh ra mà vị trí xuất hiện của nó đã có khối khác chiếm thì thua và không vẽ khối
        if self.block_fits() == True:
            self.current_block.draw(screen, 11, 11) #vẽ khối lên màn hình
        # Căn chỉnh lại để khối không bị lệch
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270) #Vẽ khối tiếp theo tại 270,270