import model as m
import ai_client as ai

class GameEngine:   # 游戏引擎
    def __init__(self, player, total_rounds=5):# 初始化游戏引擎
        self.player = player
        self.total_rounds = total_rounds
        self.current_round = 0
        self.game_over = False
        self.final_ending = None
        self.history = []   #列表
        self.last_immediate = None  # 上一次的即时故事
        self.current_scenario = None

    def start_game(self):
        #   开始游戏状态
        self.current_round = 0
        self.history = []
        self.last_immediate = None
        opening = ai.generate_opening(self.player)
        return opening

    def get_current_scenario(self): 
        # 获取当前场景
        if self.current_scenario is None:
            recent_history = self.history[-3:] if self.history else []
            memory = "\n".join(recent_history)

            self.current_scenario = ai.generate_scenario(
                self.player,
                self.current_round + 1,
                memory,
                self.last_immediate
            )
            
        return self.current_scenario

    def process_turn(self, choice):
        # 处理玩家选择
        if self.game_over:
            return True, "游戏已经结束。", "", None, None

        scenario = self.get_current_scenario()
        opt = scenario[choice]
        effect = opt.get("effect", {})
        immediate_story = opt.get("immediate_story", opt.get("text", ""))


        self.player.apply_effect(effect)


        if not self.player.is_alive():# 判断玩家是否死亡
            self.game_over = True

            failed_attr = []
            if self.player.wealth <= 0:
                failed_attr.append("财富耗尽")
            if self.player.skill <= 0:
                failed_attr.append("能力全失")
            if self.player.health <= 0:
                failed_attr.append("健康崩溃")
            if self.player.luck <= 0:
                failed_attr.append("运气归零")
            reason = "、".join(failed_attr)
            self.final_ending = f"【游戏失败】{self.player.name} 因 {reason}，未能走完人生旅程。"

            round_summary = f"第{self.current_round+1}回合：选择了{choice} - {opt['text']}。\n结果：{immediate_story}\n属性变化：{effect}\n最终属性：{self.player.to_dict()}\n【游戏结束：{reason}】"
            self.history.append(round_summary)
            return True, scenario.get("story", ""), immediate_story, effect, self.player.to_dict()


        round_summary = f"第{self.current_round+1}回合：选择了{choice} - {opt['text']}。\n结果：{immediate_story}\n属性变化：{effect}\n最终属性：{self.player.to_dict()}"
        self.history.append(round_summary)
        self.last_immediate = f"第{self.current_round+1}回合的结果：{immediate_story}"

        self.current_round += 1
        self.current_scenario = None

        if self.current_round >= self.total_rounds:
            self.game_over = True
            self.final_ending = ai.generate_ending(self.player, self.history)
            return True, scenario.get("story", ""), immediate_story, effect, self.player.to_dict()

        return False, scenario.get("story", ""), immediate_story, effect, self.player.to_dict()

    def get_final_state(self):
        return {
            "player": self.player,
            "history": self.history,
            "ending": self.final_ending
        }
    
'''
GameEngine (游戏引擎)
├── 状态管理 (属性)
├── 游戏流程控制 (方法)
│   ├── start_game()      - 开始游戏
│   ├── get_current_scenario() - 获取当前场景
│   ├── process_turn()    - 处理玩家选择
│   └── get_final_state() - 获取最终状态
└── 协作模块
    ├── ai_client         - AI剧情生成
    └── model.Player      - 玩家属性管理
'''