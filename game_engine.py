import model as m
import ai_client as ai # 目前还是模拟，后面换真实AI

class GameEngine: 
    def __init__(self, player, total_rounds=5): #初始化游戏状态，玩家对象和回合数
        self.player = player
        self.total_rounds = total_rounds
        self.current_round = 0        
        self.game_over = False
        self.final_ending = None

    def start_game(self): #初始化游戏状态，生成开场文本
        self.current_round = 0
        self.history = []# 存储每回合的摘要
        opening = self._generate_opening()
        return opening

    def _generate_opening(self): #根据玩家属性生成开场文本
        p = self.player
        text = f"欢迎你，{p.name}。\n"
        text += f"你的初始属性：财富{p.wealth}，能力{p.skill}，健康{p.health}，运气{p.luck}。\n"
        text += "在这个Python能力普遍下降的世界里，你肩负着特殊使命……\n"
        return text

    def get_current_scenario(self):   #根据当前回合数和玩家状态调用AI生成场景文本和选项
        recent_history = self.history[-3:] if self.history else []# 从历史中提取最近3条作为记忆上下文
        memory = "\n".join(recent_history)
        scenario = ai.generate_scenario(self.player, self.current_round + 1, memory)
        return scenario

    def process_turn(self, choice): #处理玩家选择，更新状态，返回结果
        if self.game_over:
            return True, "游戏已经结束。", None, None, None, None#对应optA, optB, effect, new_state
        self.current_round += 1
        scenario = self.get_current_scenario()  # 重新获取

        effect = scenario[choice]["effect"]
        self.player.apply_effect(effect)

        round_summary = f"第{self.current_round}回合：选择了{choice} - {scenario[choice]['text']}。效果：{effect}"# 记录本回合摘要
        self.history.append(round_summary)

        if self.current_round >= self.total_rounds:
            self.game_over = True
            self.final_ending = self._get_ending()  # 结局生成
            return True, scenario["story"], scenario["A"], scenario["B"], effect, self.player.to_dict()

        return False, scenario["story"], scenario["A"], scenario["B"], effect, self.player.to_dict()

    def _get_ending(self): #根据玩家最终状态生成结局文本
        p = self.player
        if p.wealth >= 80:
            ending = "【财富大师】你积累了惊人的财富，成为商界传奇。"
        elif p.skill >= 80:
            ending = "【技术泰斗】你的能力无人能及，引领了科技革命。"
        elif p.health <= 20:
            ending = "【健康危机】长期的操劳拖垮了身体，结局令人惋惜。"
        elif p.luck >= 70:
            ending = "【幸运之星】你凭借运气闯出了一片天。"
        else:
            ending = "【平凡人生】你没有特别突出的成就，但过得安稳知足。"
        return ending

    def get_final_state(self): #游戏结束后返回最终状态和结局文本
        return {
            "player": self.player,
            "history": self.history,
            "ending": self.final_ending
        }