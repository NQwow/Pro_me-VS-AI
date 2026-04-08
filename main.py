import random
import model as m
import utils as u
from game_engine import GameEngine   
from database import init_db, save_ending, get_all_endings

init_db()

def create_player():    #创建玩家角色，输入名字和属性
    name = input("请输入你的角色名：").strip()
    if not name:
        print("没有名字？那就是'普通人'喽")
        name = "普通人"
    print("请选择属性生成方式：")
    print("财富 能力 健康 运气（0-100）")
    print("1. 随机生成")
    print("2. 手动输入")

    while True:
        try:
            choice = int(input("请输入1或2："))
            if choice in [1, 2]:
                break
            else:
                print("请输入1或2")
        except ValueError:
            print("请输入数字1或2")

    if choice == 1:
        wealth = random.randint(0, 100)
        skill = random.randint(0, 100)
        health = random.randint(0, 100)
        luck = random.randint(0, 100)

    else:
        wealth = u.get_int_input("请输入财富：")
        skill = u.get_int_input("请输入能力：")
        health = u.get_int_input("请输入健康：")
        luck = u.get_int_input("请输入运气：")

    return m.Player(name, wealth, skill, health, luck)


if __name__ == "__main__":  
    print("欢迎来到 AI 文字冒险游戏！")
    player = create_player()

    engine = GameEngine(player, total_rounds=5)

    print(engine.start_game())
    input("按回车键开始冒险...")

    while not engine.game_over:
        scenario = engine.get_current_scenario()
        print(f"\n--- 第 {engine.current_round + 1} 回合 ---")
        print(scenario["story"])
        print("A:", scenario["A"]["text"])
        print("B:", scenario["B"]["text"])

        while True:
            choice = input("请选择 A 或 B: ").strip().upper()
            if choice in ["A", "B"]:
                break
            print("输入无效，请重新输入")

        finished, story, optA, optB, effect, new_state = engine.process_turn(choice)
        print(f"\n变化：{effect}")
        print(f"当前状态：{new_state}")

        if finished:
            final = engine.get_final_state()
            print("\n========== 游戏结束 ==========")
            print(f"结局：{final['ending']}")
            save_ending(final['player'], final['ending'])
            break