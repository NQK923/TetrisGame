from colors import Colors
from position import Position
import pygame
# Lớp Block cơ sở bao gồm các thuộc tính và phương thức của các lớp con
class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {} #dictionary rỗng để chứa các ô
        self.cell_size = 30 #kích thước mỗi ô của khối
        self.row_offset = 0 #Tọa độ trục tung của lưới phụ chứa khối 
        self.col_offset = 0 #Tọa độ trục hoành của lưới phụ chứa khối 
        self.rotation_state = 0 #lưu trạng thái xoay của khối
        self.colors = Colors.get_cell_colors() #lấy ra danh sách màu
    # Hàm vẽ
    def draw(self,screen, offset_x, offset_y):
        tiles = self.get_cell_positions() #Lấy ra khối từ các block ở trạng thái hiện tại lưu vào biến tiles
        # Vòng vẽ từng ô trong khối
        for tile in tiles:
            # column, row là vị trí của ô tile
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
            # Vẽ lên screen, màu tương ứng với id, hình vẽ là tile_rect
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
            
    def move(self, rows, columns): #di chuyển bao nhiêu hàng, cột
        self.row_offset += rows
        self.col_offset += columns
    # Hàm trả về vị trí các ô bị chiếm sau khi di chuyển
    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state] #lấy ra khối với trạng thái xoay hiện tại
        moved_tiles = [] #list chứa vị trí các ô
        for position in tiles:
            # Vị trí mới của các ô sau khi di chuyển
            position = Position(position.row + self.row_offset, position.column + self.col_offset)
            moved_tiles.append(position)
        return moved_tiles
    # Hàm để xoay khối
    def rotate(self):
        # Mỗi lần xoay sẽ thay đổi trạng thái
        self.rotation_state += 1
        # Nếu hết trạng thái xoay thì quay về trạng thái ban đầu
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        # Trả về trạng thái trước đó
        if self.rotation_state != 0:
            self.rotation_state -= 1
        # Nếu trạng thái là 0 thì trạng thái trước đó là len(self.cells) - 1
        elif self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1