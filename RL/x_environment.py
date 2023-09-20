class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def is_inside(self, position):
        x, y = position
        return 0 <= x <= self.width and 0 <= y <= self.height

    def apply_action(self, ship, action):
        if action == "move_forward":
            ship.move_forward()
        elif action == "move_backward":
            ship.move_backward()
        elif action == "turn_left":
            ship.turn_left(5)  # 예시로 5도 회전
        elif action == "turn_right":
            ship.turn_right(5)  # 예시로 5도 회전
        elif action == "detect":
            ship.detect()
        elif action == "fire":
            ship.fire()
        else:
            print("Invalid action")

# 종료조건 추가
# reset 함수 추가
    def reset(self):
        self.width = width
        self.height = height
        return (self.width, self.height)