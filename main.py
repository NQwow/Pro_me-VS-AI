import random
import model as m
import utils as u
import game as g

def create_player():
    #角色创建
    name = input("请输入你的角色名：").strip()
    if not name:
        print("没有名字?那就是'普通人喽'")
        name = "普通人"
    print("请选择属性生成方式：")
    print("财富 能力 健康 运气（0-100）")
    print("1.随机生成")
    print("2.手动输入")
    choice = int(input("请输入1或2："))

    if choice == 1:
        wealth = random.randint(0,100)
        skill = random.randint(0,100)
        health = random.randint(0,100)
        luck = random.randint(0,100)
        print("您的属性为：财富：{}、能力：{}、健康：{}、运气：{}".format(wealth, skill, health, luck))
    else:
        wealth =u.get_int_input("请输入财富：")
        skill = u.get_int_input("请输入能力：")
        health = u.get_int_input("请输入健康：")
        luck = u.get_int_input("请输入运气：")

    return m.Player(name,wealth,skill,health,luck)

if __name__ == "__main__":
    print("欢迎来到 AI 文字冒险游戏！")
    player = create_player()
    print("\n初始角色属性：", player)
    final_player = g.play_game(player, total_rounds=5)

    print("\n========== 游戏结束 ==========")
    ending = g.get_ending(final_player)
    print(f"最终属性：财富={final_player.wealth}, 能力={final_player.skill}, 健康={final_player.health}, 运气={final_player.luck}")
    print(f"结局：{ending}")