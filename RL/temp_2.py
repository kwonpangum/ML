import pygame

# BattleShip 클래스 정의
class BattleShip:
    def __init__(self, x, y):
        self.image = pygame.image.load('player1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# pygame 초기화
pygame.init()

# 바탕화면 크기 설정
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 배경 설정
background_color = (255, 255, 255)  # 하얀색
screen.fill(background_color)

# 가운데 수평선 그리기
line_color = (255, 0, 0)  # 붉은색
line_thickness = 1
line_y = screen_height // 2  # 가운데 y좌표
pygame.draw.line(screen, line_color, (0, line_y), (screen_width, line_y), line_thickness)

# 전투함 생성
battleship = BattleShip(250, 300)  # x=250, y=300 위치에 생성

# 전투함 화면에 그리기
screen.blit(battleship.image, battleship.rect)

# 화면 업데이트
pygame.display.flip()

# pygame 창을 닫을 때까지 계속 실행
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창을 닫으면 종료
            pygame.quit()
            quit()
