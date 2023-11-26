from block import Block
from position import Position
# Khối L
class LBlock(Block):
    def __init__(self):
        super().__init__(id = 1) #Kế thừa từ lớp cha Block
        self.cells = { #dictionary chứa các trạng thái xoay của khối
            0: [Position(0,2), Position(1,0), Position(1,1), Position(1,2)],
            1: [Position(0,1), Position(1,1), Position(2,1), Position(2,2)],
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,0)],
            3: [Position(0,0), Position(0,1), Position(1,1), Position(2,1)]
        }   
        self.move(0,3) #vị trí ban đầu của khối
# Khối J
class JBlock(Block):
    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0,0), Position(1,0), Position(1,1), Position(1,2)],
            1: [Position(0,1), Position(0,2), Position(1,1), Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,2)],
            3: [Position(0,1), Position(1,1), Position(2,0), Position(2,1)]
        }
        self.move(0,3) #vị trí ban đầu của khối
# Khối I
class IBlock(Block):
    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1,0), Position(1,1), Position(1,2), Position(1,3)],
            1: [Position(0,2), Position(1,2), Position(2,2), Position(3,2)],
            2: [Position(2,0), Position(2,1), Position(2,2), Position(2,3)],
            3: [Position(0,1), Position(1,1), Position(2,1), Position(3,1)]
        }
        self.move(-1,3) #vị trí ban đầu của khối
# Khối O
class OBlock(Block):
    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)],
            1: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)],
            2: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)],
            3: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)]
        }
        self.move(0,4) #vị trí ban đầu của khối
# Khối S
class SBlock(Block):
    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0,1), Position(0,2), Position(1,0), Position(1,1)],
            1: [Position(0,1), Position(1,1), Position(1,2), Position(2,2)],
            2: [Position(1,1), Position(1,2), Position(2,0), Position(2,1)],
            3: [Position(0,0), Position(1,0), Position(1,1), Position(2,1)]
        }
        self.move(0,3) #vị trí ban đầu của khối
# Khối T
class TBlock(Block):
    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0,1), Position(1,0), Position(1,1), Position(1,2)],
            1: [Position(0,1), Position(1,1), Position(1,2), Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,1)],
            3: [Position(0,1), Position(1,0), Position(1,1), Position(2,1)]
        }
        self.move(0,3) #vị trí ban đầu của khối
# Khối Z
class ZBlock(Block):
    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0,0), Position(0,1), Position(1,1), Position(1,2)],
            1: [Position(0,2), Position(1,1), Position(1,2), Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(2,1), Position(2,2)],
            3: [Position(0,1), Position(1,0), Position(1,1), Position(2,0)]
        }
        self.move(0,3) #vị trí ban đầu của khối