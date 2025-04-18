# session4prompt.py

class zebra:
    def __init__(self, arm_len, leg_len, eyes, has_tail, is_furry):
        self.arm_len = arm_len
        self.leg_len = leg_len
        self.eyes = eyes
        self.has_tail = has_tail
        self.is_furry = is_furry

    def describe(self):
        print(f"Arm length: {self.arm_len}m")
        print(f"Leg length: {self.leg_len}m")
        print(f"Eyes: {self.eyes}")
        print(f"Tail: {self.has_tail}")
        print(f"Furry: {self.is_furry}")

panda = zebra(0.4, 0.5, 2, True, True)
panda.describe()