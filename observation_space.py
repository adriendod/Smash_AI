class Observations:
    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.agent = self.Character(self.gamestate, 2)
        self.adversary = self.Character(self.gamestate, 1)
        self.distance: float = 0
        self.observations = []
        self.observations += self.agent.obs_list
        self.observations += self.adversary.obs_list

    def reward(self, previous_obs_space):
        previous_agent_damage = previous_obs_space.agent.percent
        previous_adversary_damage = previous_obs_space.adversary.percent
        agent_damage = self.agent.percent - previous_agent_damage
        adversary_damage = self.adversary.percent - previous_adversary_damage
        return adversary_damage - agent_damage

    class Character:
        def __init__(self, gamestate, port):
            self.port = port
            player = gamestate.player[self.port]
            self.percent = player.percent
            self.x = player.x
            self.Y = player.y
            self.shield = player.shield_strength
            self.currentMove = 0
            self.canAttack = 0
            self.isOffStage = int(player.off_stage)
            self.isOnTheFloor = int(player.on_ground)
            self.jumpsLeft = player.jumps_left
            self.stocks = player.stock
            print(self.stocks)
            self.obs_list = [self.x,
                             self.Y,
                             self.currentMove,
                             self.canAttack,
                             self.shield,
                             self.isOffStage,
                             self.isOnTheFloor,
                             self.jumpsLeft
                             ]
