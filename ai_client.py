import json
#模拟ai输出
def generate_scenario(player, round_num, memory=""):
    scenarios = [#一个字典
        {
            "story": "你在街头遇到一位神秘的商人，他向你展示了一件神奇的物品。",
            "A": {"text": "花一些财富买下它", "effect": {"wealth": -15, "luck": 10}},
            "B": {"text": "无视商人继续前进", "effect": {"skill": 5}}
        },
        {
            "story": "一位老者邀请你参加他的技术讲座，声称能提升你的能力。",
            "A": {"text": "认真听课", "effect": {"skill": 15, "health": -5}},
            "B": {"text": "悄悄离开去锻炼身体", "effect": {"health": 10, "skill": -5}}
        },
        {
            "story": "你发现了一个隐藏的训练场所，可以提升多项能力。",
            "A": {"text": "投入时间训练", "effect": {"skill": 10, "health": 5}},
            "B": {"text": "寻找合作伙伴一起训练", "effect": {"wealth": -10, "skill": 15}}
        },
    ]
    # 根据回合数循环使用场景（简单演示）
    idx = (round_num - 1) % len(scenarios)
    return scenarios[idx]

