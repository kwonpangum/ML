import random
import math

class Radar:
    def __init__(self, pos):
        self.targets = {}
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def scan(self):
        print("Scanning the horizon...")
        for name, x, y in self.detect_targets():
            if self.is_detected(x, y):
                color = "red"
            else:
                color = "blue"
            if name not in self.targets:
                self.targets[name] = 0
            self.targets[name] += 1
            print(f"{color}_{name}_{self.targets[name]} detected")

    def detect_targets(self):
        targets = []
        for i in range(10):
            x = random.randint(0, 1919)
            y = random.randint(0, 1079)
            if i % 2 == 0:
                name = f"blue_{i//2}"
            else:
                name = f"red_{i//2}"
            targets.append((name, x, y))
        return targets

    def is_range(self, x, y):
        # 대상 위치와 레이더 위치 사이의 거리를 계산하여 레이더 반지름(600) 이하인지 확인
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= 600

    def is_detected(self, x, y):
        # 대상 위치가 레이더 감지 범위 내에 있는지 확인
        return self.is_range(x, y)
