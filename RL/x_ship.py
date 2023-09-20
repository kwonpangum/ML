import pygame
import math
import random
# from x_cannon import Cannon  # x_cannon 모듈에서 Cannon 클래스를 가져옵니다.
# from x_radar import Radar  # x_radar 모듈에서 Radar 클래스를 가져옵니다.

class Ship:
    def __init__(self, screen, color, position):
        self.screen = screen
        self.color = color
        self.position = position
        self.radius = 5

        # 초기 각도 (방향) 설정
        if color == (255, 0, 0):  # RED
            self.angle = 270
        elif color == (0, 0, 255):  # BLUE
            self.angle = 90
        elif color == (128, 128, 128):  # GRAY
            self.angle = random.randint(0, 360)
        else:
            self.angle = 0

        self.speed = 5  # 움직이는 속도
        # self.cannon = Cannon()  # Cannon 객체 생성
#        self.radar = Radar()  # Radar 객체 생성

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.radius)

        # 이동 방향을 표시하는 선분 그리기
        end_x = self.position[0] + 2 * self.speed * math.cos(math.radians(self.angle))
        end_y = self.position[1] - 2 * self.speed * math.sin(math.radians(self.angle))
        pygame.draw.line(self.screen, self.color, self.position, (end_x, end_y), 2)

    def move_forward(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.position = (self.position[0] + dx, self.position[1] - dy)

    def move_backward(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.position = (self.position[0] - dx, self.position[1] + dy)

    def turn_left(self, degrees):
        self.angle = (self.angle + degrees) % 360

    def turn_right(self, degrees):
        self.angle = (self.angle - degrees) % 360

    def detect(self):
        self.radar.scan()

    def fire(self):
        self.cannon.fire()
