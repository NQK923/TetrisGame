import threading  # Import thư viện threading để hỗ trợ việc tạo và quản lý các thread
import mediapipe as mp  # Import thư viện mediapipe để xử lý Computer Vision
import cv2  # Import thư viện OpenCV để xử lý hình ảnh
from screeninfo import get_monitors  # Import hàm get_monitors từ thư viện screeninfo để lấy thông tin màn hình

from game import Game


class HandControl:
    def __init__(self):
        self.lock = threading.Lock()  # Khởi tạo một Lock để đảm bảo tính toàn vẹn dữ liệu khi sử dụng đa luồng
        self.mp_drawing = mp.solutions.drawing_utils  # Khởi tạo drawing utilities từ mediapipe
        self.mp_hand = mp.solutions.hands  # Khởi tạo hand solution từ mediapipe
        # Khởi tạo model nhận diện bàn tay
        self.hands = self.mp_hand.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.cap = cv2.VideoCapture(0)
        self.count = 0  # Khởi tạo biến đếm

    def handcontrol(self):
        game = Game()
        while self.cap.isOpened():  # Vòng lặp chạy khi webcam đang mở
            success, img = self.cap.read()  # Đọc hình ảnh từ webcam
            if not success:  # Nếu không đọc được hình ảnh thì thoát khỏi vòng lặp
                break
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Chuyển đổi hình ảnh từ BGR sang RGB
            result = self.hands.process(img)  # Xử lý hình ảnh bằng model nhận diện bàn tay
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Chuyển đổi lại hình ảnh từ RGB sang BGR

            if result.multi_hand_landmarks:  # Nếu nhận diện được bàn tay trong hình ảnh
                myHand = []  # Khởi tạo một list để lưu thông tin về các điểm trên bàn tay
                self.count = 0  # Đặt lại biến đếm
                for idx, hand in enumerate(result.multi_hand_landmarks):  # Duyệt qua các bàn tay được nhận diện
                    self.mp_drawing.draw_landmarks(img, hand, self.mp_hand.HAND_CONNECTIONS)  # Vẽ các điểm và đường nối trên bàn tay
                    for id, lm in enumerate(hand.landmark):  # Duyệt qua các điểm trên bàn tay
                        h, w, _ = img.shape  # Lấy kích thước của hình ảnh
                        myHand.append([int(lm.x * w), int(lm.y * h)])  # Thêm tọa độ của điểm vào list
                        if len(myHand) >= 21:  # Nếu đã lấy đủ 21 điểm trên bàn tay
                            if myHand[8][1] < myHand[5][1]:  # Nếu điểm thứ 8 nằm trên điểm thứ 5
                                self.count = self.count + 1  # Tăng biến đếm lên 1
                            if myHand[12][1] < myHand[10][1]:  # Nếu điểm thứ 12 nằm trên điểm thứ 10
                                self.count = self.count + 1  # Tăng biến đếm lên 1
                            if myHand[16][1] < myHand[14][1]:  # Nếu điểm thứ 16 nằm trên điểm thứ 14
                                self.count = self.count + 1  # Tăng biến đếm lên 1
                            if myHand[20][1] < myHand[18][1]:  # Nếu điểm thứ 20 nằm trên điểm thứ 18
                                self.count = self.count + 1  # Tăng biến đếm lên 1

            cv2.namedWindow("Hand Control", cv2.WINDOW_NORMAL)  # Tạo một cửa sổ mới với tên là "Hand Control"
            monitor = get_monitors()[0]  # Lấy thông tin màn hình
            window_width = 640  # Đặt chiều rộng cho cửa sổ
            window_height = 480  # Đặt chiều cao cho cửa sổ
            cv2.moveWindow("Hand Control", monitor.width - window_width,0)  # Di chuyển cửa sổ đến vị trí góc phải
            cv2.imshow("Hand Control", cv2.flip(img, 1))  # Hiển thị hình ảnh đã được xử lý lên cửa sổ
            key = cv2.waitKey(1)
            if key == 27:  # Nếu người dùng nhấn phím ESC thì thoát khỏi vòng lặp
                break
        self.cap.release()  # Giải phóng VideoCapture
