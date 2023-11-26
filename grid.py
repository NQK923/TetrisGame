# lớp Grid(1 hệ thống các ô vuông được sắp xếp thành 1 lưới) để dùng để xác định vị trí của các khối
import pygame
import time
from colors import Colors

class Grid:
    def __init__(self):
        # Khởi tạo số hàng, số cột và kích thước của mỗi ô trong lưới 
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        # khởi tạo list 2D chứa 20 list 1D mỗi list chứa 10 số 0
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        # Lấy list màu đã khởi tạo trong function get_cell_colors lưu vào biến colors
        self.colors =  Colors.get_cell_colors()
    # Kiểm tra xem ô có nằm trong màn hình không
    def is_inside(self, row, column):
        # Nếu khối nằm trong giới hạn màn hình thì đúng, ngược lại thì sai
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False
    # Kiểm tra xem ô có chiếm vị trí đã có không
    def is_empty(self, row, column):
        # Nếu ô có giá trị là 0 (chưa có khối nào chiếm dụng)
        if self.grid[row][column] == 0:
            return True
        return False
    # Kiểm tra xem hoàn thành hàng hay chưa
    def is_row_full(self, row):
        # Lấy tất cả các ô ở hàng row ra
        for column in range(self.num_cols):
            # Kiểm tra xem có ô nào trong hàng row bị trống không(tức là bằng 0)
            if self.grid[row][column] == 0:
                return False
        return True
    # Xóa hàng đã hoàn thành đi
    def clear_row(self, row):
        # Lấy ra tất cả các ô ở hàng thứ row
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    # Di chuyển hàng xuống khi hàng phía dưới được hoàn thành
    def move_row_down(self, row, num_rows):
        # Lấy tất cả các ô trong hàng thứ row
        for column in range(self.num_cols):
            # Hàng đã hoàn thành sẽ được gán bằng hàng phía trên 
            self.grid[row + num_rows][column] = self.grid[row][column]
            # Sau đó xóa hàng cũ ở phía trên đi
            self.grid[row][column] = 0

    #Duyệt qua tất cả các hàng và xử lý
    def clear_full_rows(self):
        # Biến lưu số hàng đã hoàn thành
        completed = 0
        # Duyệt qua từ hàng dưới cùng lên hàng trên cùng
        for row in range(self.num_rows-1, 0, -1):
            # Nếu hàng thứ row đã hoàn thành
            if self.is_row_full(row):
                # Thì xóa hàng thứ row đi
                self.clear_row(row)
                # Tăng số lượng hàng lên 1
                completed += 1
            # Nếu hàng hiện tại chưa hoàn thành và đã có hàng bị xóa thì di chuyển hàng hiện tại xuống completed hàng
            elif completed > 0:
                self.move_row_down(row, completed)
        # Trả về số hàng đã hoàn thành để tính điểm
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen):
        for row in range(self.num_rows): #20 hàng
            for column in range(self.num_cols): #10 cột
                # lấy giá trị của mỗi ô lưu vào biến cell_value
                cell_value = self.grid[row][column] 
                # tạo ra hình chữ nhật và lưu nó vào biến cell_rect(x, y, w, h): gồm tọa độ và kích thước
                cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11,self.cell_size - 1,self.cell_size - 1) # +11 để vị trí của ô lệch so với màn hình, -1 để giảm kích thước của khối bù cho vị trí lệch(Hiện ra đường kẻ màu xanh)
                # Dùng cú pháp như sau để vẽ và cần có (bề mặt vẽ, màu, hình vẽ)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect) # self.colors[cell_value] sẽ lấy màu tương ứng với index trong danh sách colors nếu tùy vào giá trị trong grid