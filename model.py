class Player:   # 玩家这个类
    def __init__(self, name, wealth, skill, health, luck):  # 自动运行的
        self.name = name    #我自己的名字是名字，指向自己
        self.wealth = wealth    #创建实例本身
        self.skill = skill
        self.health = health
        self.luck = luck

    def apply_effect(self, effect): # 应用效果
        for attr, delta in effect.items():
            current = getattr(self, attr)
            new_value = current + delta
            if new_value < 0:
                new_value = 0
            elif new_value > 100:
                new_value = 100
            setattr(self, attr, new_value)

    def is_alive(self): # 判断是否还活着
        return (self.wealth > 0 and self.skill > 0 and 
                self.health > 0 and self.luck > 0)

    def to_dict(self):  # 字典
        return {
            "name": self.name,
            "wealth": self.wealth,
            "skill": self.skill,
            "health": self.health,
            "luck": self.luck
        }

    def __repr__(self): # 打印
        return f"Player(名字={self.name},财富={self.wealth},能力={self.skill},健康={self.health},运气={self.luck})"