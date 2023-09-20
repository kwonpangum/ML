# 전투함

class Cannon:
    def __init__(self, caliber):
        self.caliber = caliber

    def fire(self, target):
        print(f"Firing {self.caliber} caliber cannon at {target}!")


class Radar:
    def scan(self):
        print("Scanning the horizon...")


class Ship(Cannon, Radar):
    def __init__(self, caliber):
        Cannon.__init__(self, caliber)
        Radar.__init__(self)

    def attack(self, target):
        self.scan()
        self.fire(target)


