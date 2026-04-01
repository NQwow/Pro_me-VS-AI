# game.py
import model as m
import ai_client as a

def play_game(player, total_rounds=5):
    #主要流程
    memory = ""  # 记忆摘要，用于后续传给AI
    round_num = 1

    while round_num <= total_rounds:
        print(f"\n========== 第 {round_num} 回合 ==========")# 调用AI（或模拟）获取剧情和选项
        scenario = a.generate_scenario(player, round_num, memory)
        print(scenario["story"].replace("{name}", player.name))
        print("\n选项：")
        print(f"A: {scenario['A']['text']}")
        print(f"B: {scenario['B']['text']}")

        while True:#只有输入AB正确才会继续进行
            choice = input("请选择 A 或 B：").strip().upper()
            if choice in ["A", "B"]:
                break
            print("输入无效，请重新输入 A 或 B")

        effect = scenario[choice]["effect"]
        player.apply_effect(effect)
        memory = f"第{round_num}回合：选择了{choice}：{scenario[choice]['text']}。当前属性：{player.to_dict()}"

        print(f"\n变化：{effect}")
        print(f"当前状态：财富={player.wealth}, 能力={player.skill}, 健康={player.health}, 运气={player.luck}")
        round_num += 1
    return player

def get_ending(player):
    #结局判定的
    if player.wealth >= 80:
        return "【财富大师】你积累了惊人的财富，成为商界传奇。"
    elif player.skill >= 80:
        return "【技术泰斗】你的能力无人能及，引领了科技革命。"
    elif player.health <= 20:
        return "【健康危机】长期的操劳拖垮了身体，结局令人惋惜。"
    elif player.luck >= 70:
        return "【幸运之星】你凭借运气闯出了一片天，虽不完美但充满惊喜。"
    else:
        return "【平凡人生】你没有特别突出的成就，但过得安稳知足。"