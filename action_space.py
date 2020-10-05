
class CharObservations:
    def __init__(self):
        self.distance: float = 0
        self.x: float = 0
        self.Y: float = 0
        self.currentMove: float = 0
        self.canAttack: float = 0
        self.canShield: float = 0
        self.isInTheAir: float = 0
        self.isOnTheFloor: float = 0
        self.hasDoubleJump: float = 0


    def updateState(self, portNum):
        self.distance: float = 0
        self.x: float = 0
        self.Y: float = 0
        self.currentMove: float = 0
        self.canAttack: float = 0
        self.canShield: float = 0
        self.isInTheAir: float = 0
        self.isOnTheFloor: float = 0
        self.hasDoubleJump: float = 0