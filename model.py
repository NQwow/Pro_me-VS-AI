class Player:
    def __init__(self,name,wealth,skill,health,luck):
        self.name=name
        self.wealth = wealth
        self.skill = skill
        self.health = health
        self.luck = luck

    def apply_effect(self,effect):
        for attr,delta in effect.items():
            current=getattr(self,attr)
            new_value=current+delta
            if new_value<0:
                new_value=0
            elif new_value>100:
                new_value=100

            setattr(self,attr,new_value)
    def to_dict(self):
        return {
            "name":self.name,
            "wealth":self.wealth,
            "skill":self.skill,
            "health":self.health,
            "luck":self.luck
        }

    def __repr__(self):
        return f"Player(名字={self.name},财富={self.wealth},能力={self.skill},健康={self.health},运气={self.luck})"
