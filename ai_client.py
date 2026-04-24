import json
import os
import time
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 智谱 AI 配置（ glm-4-flash）
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
if ZHIPU_API_KEY:
    client = OpenAI(
        api_key=ZHIPU_API_KEY,
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
    MODEL_NAME = "glm-4-flash"  
    print(f"已启用智谱 AI API (模型: {MODEL_NAME})")
else:
    client = None
    print("未配置 ZHIPU_API_KEY，将使用模拟剧情。")

def is_available():
    return client is not None

def generate_scenario(player, round_num, memory="", last_choice_result=None):
    # 0-调用检查
    if client:
        try:
            return _call_zhipu_api(player, round_num, memory, last_choice_result)
        except Exception as e:
            print(f"API 调用失败，使用模拟剧情。错误: {e}")
            return _get_mock_scenario(round_num)
    else:
        return _get_mock_scenario(round_num)

def _get_default_opening(player):   
    #1-初始化
    return f"欢迎你，{player.name}。\n你的初始属性：财富{player.wealth}，能力{player.skill}，健康{player.health}，运气{player.luck}。\n在这个Python能力普遍下降的世界里，你作为唯一还能写代码的人，即将展开一段冒险……"

def generate_opening(player):   
    # 2-开场白生成
    if not client:
        return _get_default_opening(player)
    try:
        prompt = f"""请根据以下设定，生成一段 150 字以内的开场白（直接输出文本，不要 JSON）：
【世界观】
全世界所有人的 Python 编程能力下降为原来的 1%，唯独 {player.name} 的能力保持不变。与此同时，AI 技术突然爆发，各种 AI 工具涌现。
【玩家初始属性】（此处不要修改角色属性）
财富 {player.wealth}，能力 {player.skill}，健康 {player.health}，运气 {player.luck}

请描写 {player.name} 醒来后感受到的世界变化（与 Python 能力或 AI 爆发相关）。"""
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        text = response.choices[0].message.content.strip()
        return text
    except Exception as e:
        print(f"开场白生成异常: {e}")
        return _get_default_opening(player)
    
def _build_prompt(player, round_num, memory, last_choice_result):   
    # 3-流程进行中……
    return f"""你是一个文字冒险游戏的故事生成器。请严格输出 JSON，不要加解释。

【世界观】
一觉醒来，全世界所有人的 Python 编程能力下降为原来的 1%（能力值从 100 变成 1），唯独玩家 {player.name} 能力不变。与此同时，AI 技术突然爆发，各种 AI 工具涌现。玩家既拥有稀有技能，又面临未知风险。

【当前状态】
玩家：{player.name}
财富 {player.wealth}，能力 {player.skill}，健康 {player.health}，运气 {player.luck}
当前是第 {round_num} 回合，共 5 回合。

【之前剧情摘要】
{memory if memory else "（无）"}

【上一轮选择的结果】
{last_choice_result if last_choice_result else "（开局）"}

请生成以下 JSON，每个字段含义：
- "story": 本轮场景描述（**120-200字**，必须自然衔接上一轮的结果，体现 Python 能力差距或 AI 爆发的影响。要包含具体的环境、人物或事件细节，让故事有沉浸感。）
- "A": {{
    "text": "选项 A 的文字（20字内，要体现风险和收益）",
    "immediate_story": "玩家选 A 后立刻发生的故事（60-100字，详细描述选择带来的直接后果）",
    "effect": {{"wealth": 变化, "skill": 变化, "health": 变化, "luck": 变化}}
  }}
- "B": 同上结构

要求：
1. 属性变化范围 -20 到 +20，但要符合逻辑（疯狂加班 +skill 但 -health；投机可能 +wealth 但 -luck）。
2. 剧情要有挑战性，选项不能都是好的或坏的，让玩家纠结。
3. 如果某项属性低于 20 或高于 80，剧情中要体现危机感或成就感。
4. 所有剧情要前后呼应，每一轮的问题最好是上一轮选择导致的自然结果。
5. 故事背景是现代，不要出现末日和奇幻题材。

输出示例：
{{
    "story": "你在一家初创公司担任 CTO。由于只有你能修复 AI 核心代码，公司躲过了三次黑客攻击。但你的健康因熬夜下降到了 40。今天，董事会要求你用 AI 生成一个能替代 80% 程序员的工具，否则就撤资。你望着镜子里的黑眼圈，陷入了沉思。",
    "A": {{
        "text": "接受要求，疯狂编码",
        "immediate_story": "你连续工作了 72 小时，终于写出了工具。董事会非常满意，给了你一大笔奖金。但你直接晕倒被送进医院，健康严重受损。",
        "effect": {{"wealth": 20, "skill": 10, "health": -15, "luck": 0}}
    }},
    "B": {{
        "text": "拒绝并辞职，自己创业",
        "immediate_story": "你带着核心技术和几个忠诚的工程师离开，创立了新公司。初期资金紧张，但你的能力吸引了天使投资。运气似乎站在你这边。",
        "effect": {{"wealth": -10, "skill": 5, "health": 5, "luck": 15}}
    }}
}}
"""
def _call_zhipu_api(player, round_num, memory, last_choice_result):
    # 没招了，进行模拟和解析
    prompt = _build_prompt(player, round_num, memory, last_choice_result)
    
    print(" 正在推演剧情", end="", flush=True)
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print(" 开始生成...", flush=True)
    time.sleep(0.2)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=2500,
    )
    
    content = response.choices[0].message.content
    # 尝试提取 JSON
    try:
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = content[start:end]
            scenario = json.loads(json_str)
        else:
            raise ValueError("未找到有效的 JSON")
    except Exception as e:
        print(f"JSON 解析失败: {e}\n原始内容: {content}")
        raise

    if not all(k in scenario for k in ("story", "A", "B")):# 检查 JSON 是否完整，没招了，要成功啊
        raise ValueError("AI 返回的 JSON 缺少 story/A/B 字段")
    for opt in ("A", "B"):
        if "text" not in scenario[opt] or "effect" not in scenario[opt]:
            scenario[opt].setdefault("text", "继续前进")
            scenario[opt].setdefault("effect", {})
            scenario[opt].setdefault("immediate_story", scenario[opt]["text"])
        if "immediate_story" not in scenario[opt]:
            scenario[opt]["immediate_story"] = scenario[opt]["text"]
    
    print("剧情生成完成！\n")
    return scenario
def _generate_detailed_ending_by_rules(player, history):
    # 4-结局草稿
    w, s, h, l = player.wealth, player.skill, player.health, player.luck
    
    if w >= 80 and s >= 70:
        title = "【技术商业巨擘】"
        desc = "你一手创建的科技帝国改变了世界，财富与技术双丰收。"
    elif s >= 80 and h >= 70:
        title = "【编程宗师】"
        desc = "你活到老学到老，成为后世程序员敬仰的传奇。"
    elif w >= 80 and l >= 70:
        title = "【幸运投机者】"
        desc = "你总能在关键时刻押对宝，财富滚滚而来，但同行评价两极分化。"
    elif h >= 80 and l >= 70:
        title = "【福星高照】"
        desc = "你一生无病无灾，家庭美满，活成了别人眼中的奇迹。"
    elif w >= 90:
        title = "【财富神话】"
        desc = "你积累的财富足以买下一个小国，但代价是失去了许多平凡快乐。"
    elif s >= 90:
        title = "【代码之神】"
        desc = "你的 Python 能力无人可及，开源项目影响全球，但孤独常伴。"
    elif h >= 90:
        title = "【不老传说】"
        desc = "你年过百岁仍精神矍铄，见证了时代的变迁，却感叹故人已逝。"
    elif l >= 90:
        title = "【天选之人】"
        desc = "你一生如同开挂，每次危机都有贵人相助，连自己都觉得不真实。"
    elif w <= 15:
        title = "【一贫如洗】"
        desc = "你最终身无分文，流落街头，AI 时代的光芒并未照耀你。"
    elif s <= 15:
        title = "【技术废人】"
        desc = "你失去了所有编程能力，在这个依赖代码的世界寸步难行。"
    elif h <= 15:
        title = "【英年早逝】"
        desc = "长期的透支压垮了身体，你没能看到自己种下的树开花。"
    elif l <= 15:
        title = "【霉运缠身】"
        desc = "喝凉水都塞牙，你的一生被厄运笼罩，最终默默无闻。"
    elif 40 <= w <= 70 and 40 <= s <= 70 and 40 <= h <= 70 and 40 <= l <= 70:
        title = "【平凡幸福】"
        desc = "你没有大富大贵，但家庭和睦，身体健康，平安度过了 AI 浪潮。"
    else:
        total = w + s + h + l
        if total >= 200:
            title = "【中产典范】"
            desc = "你过上了舒适的中产阶级生活，有房有车，偶尔还能度假。"
        else:
            title = "【普通人生】"
            desc = "你像大多数人一样，为生活奔波，偶尔回味年轻时的冒险。"

    details = []# 详细描述
    if w >= 80:
        details.append(f"积累了 {w} 点财富，晚年住在科技豪宅中，偶尔投资新项目。")
    elif w <= 20:
        details.append(f"财富仅有 {w} 点，生活拮据，靠社区救济度日。")
    else:
        details.append(f"拥有 {w} 点财富，生活小康，不必为柴米油盐发愁。")
    
    if s >= 80:
        details.append(f"能力值高达 {s}，仍有人慕名请教 Python 技巧。")
    elif s <= 20:
        details.append(f"能力只剩 {s}，连简单脚本都写不流畅，被时代遗忘。")
    else:
        details.append(f"能力保持在 {s}，偶尔接点私活，维持技术敏感度。")
    
    if h >= 80:
        details.append(f"健康值 {h}，每天晨跑，体检报告让年轻人羡慕。")
    elif h <= 20:
        details.append(f"健康仅剩 {h}，常年卧床，药不离口。")
    else:
        details.append(f"健康 {h}，有些小毛病但无大碍。")
    
    if l >= 80:
        details.append(f"运气 {l}，买彩票经常中奖，出门遇贵人。")
    elif l <= 20:
        details.append(f"运气只有 {l}，喝凉水都塞牙，投资必赔。")
    else:
        details.append(f"运气 {l}，偶尔小惊喜，总体平淡。")
    
    key_events = _extract_key_events(history)# 提取关键事件
    events_text = "\n".join(key_events) if key_events else "一路平稳，无大风大浪。"
    
    if h > 50:# 健康和财富决定离世方式，严谨！
        death = "在睡梦中安详离世"
    elif h < 30:
        death = "在病榻上留下遗憾"
    else:
        death = "在家人的陪伴下告别"
    
    base_age = 60
    if w > 50:
        base_age += 10
    if h > 60:
        base_age += 10
    elif h < 40:
        base_age -= 10
    age_str = f"{base_age}岁"
    
    ending_text = f"""{title}
{desc}

{details[0]} {details[1]} {details[2]} {details[3]}

{events_text}

{player.name} 常对后辈说：“在这个 Python 能力贬值、AI 泛滥的世界，能保持初心已是万幸。”
最终，{player.name} 在{death}，享年{age_str}。他的故事，成为了那个特殊时代的一个注脚。"""
    
    return ending_text

def _extract_key_events(history):# 提取关键事件
    if not history:
        return []
    events = []
    for record in history[-5:]: # 提取属性变化较大的部分
        changes = re.findall(r'(\w+):\s*([+-]?\d+)', record)
        big_changes = [f"{attr}{delta}" for attr, delta in changes if abs(int(delta)) >= 10]
        if big_changes:
            events.append(f"• 重大转折：{', '.join(big_changes)}")
        else:
            choice_match = re.search(r'选择了([AB]) - (.*?)[。.]', record)
            if choice_match:
                choice_letter, choice_text = choice_match.group(1), choice_match.group(2)
                events.append(f"• 第{choice_letter}选项：{choice_text}")
    unique_events = []
    for e in events:
        if e not in unique_events:
            unique_events.append(e)
    return unique_events[:3]

def generate_ending(player, history):
    # 5-结局的润色
    draft = _generate_detailed_ending_by_rules(player, history)
    
    if not client:
        return draft
    
    try:
        prompt = f"""你是一个文字润色专家。请将下面的结局草稿改写得更加优美、流畅、有文学感，但不要改变任何事实信息（属性数值、结局名称、关键事件）。润色后直接输出文本，不要添加额外说明。
草稿内容：
{draft}
要求：
- 保持原有长度（约200-300字）
- 语言更生动，可适当增加比喻或情感描写
- 不要新增事实性内容（如新的财富数字、结局类型变化）
- 输出纯文本，不要加引号或标记
"""
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800,
        )
        polished = response.choices[0].message.content.strip()
        if len(polished) > 100:  # 确保润色有效
            return polished
        else:
            return draft
    except Exception as e:
        print(f"AI 润色失败，使用本地草稿。错误: {e}")
        return draft
def _get_mock_scenario(round_num):# 模拟场景
    base = {
        "story": "你走在街上，突然遇到一个神秘的商人。他向你展示了一件神奇的物品，声称能改变你的命运。",
        "A": {
            "text": "花一些财富买下它",
            "immediate_story": "你买下了物品，感觉运气有所提升。",
            "effect": {"wealth": -15, "luck": 10}
        },
        "B": {
            "text": "无视商人继续前进",
            "immediate_story": "你继续赶路，感觉自己的能力有所增长。",
            "effect": {"skill": 5}
        }
    }
    return base