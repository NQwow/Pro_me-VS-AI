class Player:
    def __init__(self, name, wealth, skill, health, luck):
        self.name = name
        self.wealth = wealth
        self.skill = skill
        self.health = health
        self.luck = luck

    def apply_effect(self, effect):
        for attr, delta in effect.items():
            current = getattr(self, attr)
            new_value = current + delta
            # 钳制到 0~100，但允许 0 存在（后续会判定死亡）
            if new_value < 0:
                new_value = 0
            elif new_value > 100:
                new_value = 100
            setattr(self, attr, new_value)

    def is_alive(self):
        """返回 True 表示所有属性都大于 0"""
        return (self.wealth > 0 and self.skill > 0 and 
                self.health > 0 and self.luck > 0)

    def to_dict(self):
        return {
            "name": self.name,
            "wealth": self.wealth,
            "skill": self.skill,
            "health": self.health,
            "luck": self.luck
        }

    def __repr__(self):
        return f"Player(名字={self.name},财富={self.wealth},能力={self.skill},健康={self.health},运气={self.luck})"