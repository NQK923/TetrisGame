# File main dùng để khởi chạy trò chơi(chứa vòng lặp trò chơi) và khởi tạo các giá trị cần thiết cho màn hình trò chơi
import pygame, sys, time
import threading
from game import Game
from colors import Colors
import pygame.font
import math
from handControl import HandControl
# Khởi tạo pygame
pygame.init()
# Khai báo font chữ mặc định, kích thước 40
font_path = "./font.ttf"

# Kích thước font
font_size = 30
lv = 1

# Tạo đối tượng font
# custom_font = pygame.font.Font(font_path, font_size)
title_font = pygame.font.Font(font_path, 28)
title_font_replay = pygame.font.Font(font_path, 17)
# Khởi tạo chữ Score, anti-aliasing = True(để mịn chữ), màu
level_surface = title_font_replay.render("Level", True, Colors.white)
lv_surface = title_font_replay.render(str(lv), True, Colors.white)

score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
replay_surface = title_font_replay.render("Press R to Replay", True, Colors.white)
pause_surface = title_font_replay.render("Press P to Pause", True, Colors.white)
continue_surface = title_font_replay.render("Press P to Continue", True, Colors.white)
record_surface = title_font_replay.render("Record score", True, Colors.green)
# Khởi tạo hình chữ nhật tại vị trí 320,55 kích thước 170x60
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
record_rect = pygame.Rect(320, 140, 170, 40)
# Khởi tạo màu cho màn hình trò chơi

# Khởi tạo kích thước màn hình
screen = pygame.display.set_mode((500,620))

# Đặt caption cho màn hình trò chơi
pygame.display.set_caption("Python Tetris")

# Biến clock dùng để điều chỉnh tốc độ khung hình của trò chơi
clock = pygame.time.Clock()
# Cập nhật sự kiện mỗi khi khối di chuyển hoặc thay đổi trạng thái(không có dòng này sẽ bị lag do không bắt được sự kiện của khối)
speed = 500

GAME_UPDATE = pygame.USEREVENT + 1 #để độc lập với tốc độ của vòng lặp trò chơi
update_interval = 500
pygame.time.set_timer(GAME_UPDATE, update_interval) #cập nhật mỗi 300 milisecond (tốc độ rơi của khối)

# Khởi tạo màn hình gamne
game = Game()
handControl = HandControl()
# Biến tạm dừng
game_paused = False
# Vòng lặp trò chơi
while True:
    # Nếu handControl được mở và game không pause hoặc không thua, xử lý sự kiện game
    if game.game_over == False and game_paused == False and handControl.count !=0:
        time.sleep(0.3)
        if handControl.count == 1:
            game.move_right()
        elif handControl.count == 2:
            game.move_left()
        elif handControl.count == 3:
            game.rotate()
        elif handControl.count == 4:
            game.move_down()
        handControl.count = 0
    # Lặp qua tất cả các sự kiện mà người chơi tác động vào pygame
    for event in pygame.event.get():
        # Nếu người chơi nhấn vào nút quit
        if event.type == pygame.QUIT:
            # Sẽ thoát pygame
            pygame.quit()
            # Đóng hoàn toàn chương trình
            sys.exit()
        if event.type == pygame.KEYDOWN: #xử lý sự kiện khi nhấn
            if game.game_over == True: # Khi nhấn phím R khi thua để chơi lại
                if event.key == pygame.K_r:
                    # Cap nhat lai level khi choi lai
                    lv = 1
                    lv_surface = title_font_replay.render(str(lv), True, Colors.white)
                    game.game_over = False
                    game.reset()
            # Nếu không thua và không dừng game thì sự kiện được bắt
            if event.key == pygame.K_m and game.game_over == False and game_paused == False:
                t = threading.Thread(target=handControl.handcontrol)
                # Bắt đầu thread
                t.start()
            if event.key == pygame.K_LEFT and game.game_over == False and game_paused == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False and game_paused == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False and game_paused == False:
                game.move_down()
                game.update_score(0, 1)#0 thì sẽ cộng vào 1 cho điểm thưởng
            if event.key == pygame.K_UP and game.game_over == False and game_paused == False:
                game.rotate()
            if event.key == pygame.K_p and game.game_over == False:  # Xử lý sự kiện phím P
                game_paused = not game_paused
                pygame.mixer.music.pause() #Khi Pause sẽ dừng nhạc
        if event.type == GAME_UPDATE and game.game_over == False and game_paused == False: #move down mỗi khi GAME_UPDATE chứ không phải cập nhật mỗi lần lặp game
            game.move_down()
            pygame.mixer.music.unpause() #Khi 
            # Mỗi 1000 điểm thì speed sẽ tăng lên(-10) và lv tăng 1
            new_level = math.floor(game.score / 1000) + 1
            if new_level > lv:
                lv = new_level
                speed = speed - 10
                # Để speed != 0 để chương trình không bị dừng
                if speed < 10:
                    speed = 10
                pygame.time.set_timer(GAME_UPDATE, speed)
                lv_surface = title_font_replay.render(str(lv), True, Colors.white)

    # Khởi tạo điểm cho giao diện
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    # Gán màu xanh đậm đã khởi tạo cho màn hình trò chơi
    screen.fill(Colors.dark_blue)
    # Hiển thị tại ví trí có tọa độ 365,20 kích thước 50x50
    screen.blit(score_surface, (370, 20, 50, 50))
    screen.blit(next_surface, (380, 182, 50, 50))
    screen.blit(record_surface, (360, 120, 50, 50)) 
    screen.blit(level_surface, (380,400,50,50))
    screen.blit(lv_surface, (430, 400, 50, 50))
    if game.game_over == True: #Nếu thua thì hiển thị chữ GAME OVER
        screen.blit(game_over_surface, (340, 450, 50, 50))
        screen.blit(replay_surface, (345, 500, 50, 50))
        game_paused = False #Khi thua thì không được dừng game
    if game_paused == False and game.game_over == False: #Nếu chưa dừng game và chưa thua thì hiển thị pause
        screen.blit(pause_surface, ((345, 500, 50, 50)))
    elif game_paused == True and game.game_over == False: #Nếu dừng game và chưa thua thì hiển thị continue
        screen.blit(continue_surface, ((338, 500, 50, 50)))
    # Vẽ hình chữ nhật chứa điểm 0 là màu của hình chữ nhật và không có viền, 10 là bo góc 10px
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    # Vẽ điểm vào giữa hình chữ nhật
    screen.blit(score_value_surface, (score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery)))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)

    # Đọc file lưu điểm kỷ lục
    f = open("./record_score.txt","r")
    record_score = f.read()
    # Kiểm tra xem chuỗi có giá trị không trước khi chuyển đổi
    if record_score:
        record_score = int(record_score)
    else:
        record_score = 0
    # Trả về vị trí đầu tiên của của con trỏ
    f.seek(0)
    f.close()
    # Lấy ra điểm kỷ lục
    record_score_surface = title_font_replay.render(str(record_score), True, Colors.green)
    # Vẽ hình chữ nhật chứa điểm kỷ lục
    pygame.draw.rect(screen, Colors.light_blue, record_rect, 0, 10)
    # Vẽ điểm kỷ lục vào giữa hình chữ nhật
    screen.blit(record_score_surface, (record_score_surface.get_rect(centerx = record_rect.centerx, centery = record_rect.centery)))
    if game.score > record_score:
        # File sẽ tự close
        with open("./record_score.txt", "w") as f:
            f.write(str(game.score))
    
    # Vẽ lưới và khối lên màn hình
    game.draw(screen)
    # Cập nhật lại màn hình pygame qua mỗi lần lặp 
    pygame.display.update()

    # Chỉnh tốc độ khung hình(fps): 120 lần/giây
    clock.tick(120)
