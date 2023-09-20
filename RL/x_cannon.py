class Cannon:
    def __init__(self, caliber):
        self.caliber = caliber

    def fire(self, target):
        print(f"Firing {self.caliber} caliber cannon at {target}!")
