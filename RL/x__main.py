import pygame
import sys
from x_ship import Ship  # x_ship 모듈에서 Ship 클래스를 가져옵니다.
from x_environment import Environment  # x_environment 모듈에서 Environment 클래스를 가져옵니다.

# 상수 정의
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
LINE_WIDTH = 1

def main():
    # 초기화
    pygame.init()

    # 화면 설정
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("인공지능 전투함")

    # 환경 생성
    environment = Environment(SCREEN_WIDTH, SCREEN_HEIGHT)

    # blue_1(우군) 생성
    blue_1 = Ship(screen, BLUE, (300, 500))

    # red_1 (적군) 생성
    red_1 = Ship(screen, RED, (300, 100))

    # 게임 루프
    while True:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 배경 채우기
        screen.fill(WHITE)

        # 수평선 그리기
        pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), LINE_WIDTH)

        # blue, red, gray 그리기
        red_1.draw()
        blue_1.draw()

        # 화면 업데이트
        pygame.display.flip()

if __name__ == "__main__":
    main()
