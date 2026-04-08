import json
import os
from dotenv import load_dotenv
from zai import ZhipuAiClient

load_dotenv()

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

if ZHIPU_API_KEY:
    client = ZhipuAiClient(api_key=ZHIPU_API_KEY)
else:
    client = None
    print("警告：未配置 ZHIPU_API_KEY，将使用模拟剧情。")


def generate_scenario(player, round_num, memory=""):#生成剧情，调用智谱API，失败则使用模拟剧情
    if client:
        try:
            return _call_zhipu_api(player, round_num, memory)
        except Exception as e:
            print(f"智谱 AI 调用失败，使用模拟剧情。错误: {e}")
            return _get_mock_scenario(round_num)
    else:
        return _get_mock_scenario(round_num)

def _call_zhipu_api(player, round_num, memory):#调用智谱 API 生成剧情
    prompt = _build_prompt(player, round_num, memory)

    response = client.chat.completions.create(
        model="glm-4.7-flash",         
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=2048,                
        thinking={"type": "disabled"} # 深度思考，加快速度
    )

    content = response.choices[0].message.content
    scenario = json.loads(content)

    if not all(k in scenario for k in ("story", "A", "B")):
        raise ValueError("AI 返回的 JSON 缺少 story/A/B 字段")

    return scenario


def _build_prompt(player, round_num, memory):

    return f"""你是一个文字冒险游戏的故事生成器。请严格按照 JSON 格式输出，不要添加任何解释。
背景：一觉醒来，全世界Python能力下降100倍而玩家不变。但恰逢AI技术爆发，玩家能否在这个世界生存下去？

玩家信息：
- 名字：{player.name}
- 财富：{player.wealth}
- 能力：{player.skill}
- 健康：{player.health}
- 运气：{player.luck}

当前是第 {round_num} 回合。
之前的记忆摘要：
{memory if memory else "（无）"}

请生成：
1. 一段 80 字以内的剧情（需自然融入玩家名字），或用“你”代替
2. 两个选项 A 和 B，每个选项包含文本和对应的属性变化（effect）
   - effect 是一个字典，键可以是 "wealth", "skill", "health", "luck" 中的任意组合
   - 每个属性的变化范围在 -20 到 +20 之间
   - 注意变化不能过于离谱，要符合剧情逻辑
3. 每次输出要结合玩家当前属性，设计合理的选项和效果，在做出选择后输出相关剧情再进行属性变化与下一轮，每一轮故事要有连接性，前后呼应。

输出格式必须严格为以下 JSON，不要有额外内容：
{{
    "story": "剧情文本",
    "A": {{
        "text": "选项A描述",
        "effect": {{"wealth": 数值, "skill": 数值}}
    }},
    "B": {{
        "text": "选项B描述",
        "effect": {{"health": 数值, "luck": 数值}}
    }}
}}
"""

def _get_mock_scenario(round_num):
    """原有的模拟场景"""
    scenarios = [
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
    idx = (round_num - 1) % len(scenarios)
    return scenarios[idx]


