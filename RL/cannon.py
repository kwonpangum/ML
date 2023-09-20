import pygame
import math

pygame.init()

# 배경화면: 흰색, 800*600
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((255, 255, 255))

# 대포 이미지 생성
cannon_img = pygame.Surface((2, 2), pygame.SRCALPHA)
pygame.draw.circle(cannon_img, (0, 0, 0), (1, 1), 1)

# 포탄 이미지 생성
bullet_img = pygame.Surface((2, 2), pygame.SRCALPHA)
pygame.draw.circle(bullet_img, (0, 0, 0), (1, 1), 1)

# 대포 이미지와 포탄 이미지 출력
screen.blit(cannon_img, (100, 100))
screen.blit(bullet_img, (110, 100))
pygame.display.update()

class Cannon:
    def __init__(self, cannon_pos):
        self.x, self.y = cannon_pos
        self.angle = 0

    def fire(self, target):
        # 포탄 객체 생성
        bullet = Bullet(self.x, self.y, self.angle, target)

        # 포탄 발사
        bullet.fire()


class Bullet:
    def __init__(self, cannon_pos, angle, target):
        self.x, self.y = cannon_pos
        self.angle = angle
        self.target = target

        # 포탄의 최초 위치를 대포 위치로 지정
        self.start_x = cannon_pos
        self.start_y = cannon_pos

    def fire(self):
        # 포탄 이동
        while self.x < self.target[0] or self.y < self.target[1]:
            # 대포 발사각도에 따라 포탄 이동
            self.x += int(5 * math.cos(math.radians(self.angle)))
            self.y -= int(5 * math.sin(math.radians(self.angle)))

            # 화면을 흰색으로 채우고 대포와 포탄 이미지를 다시 출력
            screen.fill((255, 255, 255))
            screen.blit(cannon_img, (self.x, self.y))
            screen.blit(bullet_img, (self.start_x, self.start_y))

            # 화면 업데이트
            pygame.display.update()


# 대포 객체 생성
cannon = Cannon(100, 100)

# 발사 명령 받으면 포탄 발사
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 마우스 클릭 위치가 포탄이 발사될 목표물의 좌표
            target = pygame.mouse.get_pos()

            # 대포에서 포탄 발사
            cannon.fire(target)



