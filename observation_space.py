class Observations:
    def __init__(self):
        self.agent = self.Character(2)
        self.adversary = self.Character(1)
        self.distance: float = 0
        self.observations = []

    def update(self, gamestate):
        self.distance = gamestate.distance
        self.Character.x = gamestate.player[1].x
        self.agent.update_char(gamestate)
        self.adversary.update_char(gamestate)

        self.observations = []
        self.observations.append(self.agent.obs_list)
        self.observations.append(self.adversary.obs_list)

    class Character:
        def __init__(self, port):
            self.port: int = port
            self.percent: float = 0
            self.x: float = 0
            self.Y: float = 0
            self.shield: float = 60
            self.currentMove: float = 0
            self.canAttack: float = 0
            self.canShield: float = 0
            self.isInTheAir: float = 0
            self.isOnTheFloor: float = 0
            self.jumpsLeft: float = 0
            self.obs_list = []

        def update_char(self, gamestate):
            player = gamestate.player[self.port]
            self.percent = player.percent
            self.x = player.x
            self.Y = player.y
            self.shield = player.shield_strength
            #self.currentMove = player.
            #self.canAttack = player.
            self.isInTheAir = player.off_stage
            self.isOnTheFloor = player.on_ground
            self.jumpsLeft = player.jumps_left
            self.obs_list = [self.x,
                             self.Y,
                             self.currentMove,
                             self.canAttack,
                             self.canShield,
                             self.isInTheAir,
                             self.isOnTheFloor,
                             self.jumpsLeft
                             ]
