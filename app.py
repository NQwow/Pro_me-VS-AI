from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import uuid
import random
import game_engine as ge
import model as m
import database as db

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new_game', methods=['POST'])
def new_game():
    data = request.get_json()
    name = data.get('name', '冒险者')
    random_attr = data.get('random', True)   # 是否随机生成属性
    
    if random_attr:
        wealth = random.randint(0, 100)
        skill = random.randint(0, 100)
        health = random.randint(0, 100)
        luck = random.randint(0, 100)
    else:
        wealth = data.get('wealth', 50)
        skill = data.get('skill', 50)
        health = data.get('health', 50)
        luck = data.get('luck', 50)
    
    player = m.Player(name, wealth, skill, health, luck)
    engine = ge.GameEngine(player, total_rounds=5)
    opening = engine.start_game()
    
    # 获取第一回合的场景（用于显示选项）
    first_scenario = engine.get_current_scenario()
    first_scenario_data = {
        'story': first_scenario['story'],
        'A': {'text': first_scenario['A']['text']},
        'B': {'text': first_scenario['B']['text']}
    }
    
    session_id = str(uuid.uuid4())
    games[session_id] = engine
    
    return jsonify({
        'session_id': session_id,
        'opening': opening,
        'player': player.to_dict(),
        'first_scenario': first_scenario_data,
        'total_rounds': engine.total_rounds
    })

@app.route('/api/choice', methods=['POST'])
def make_choice():
    data = request.get_json()
    session_id = data.get('session_id')
    choice = data.get('choice')
    
    engine = games.get(session_id)
    if not engine:
        return jsonify({'error': 'Invalid session'}), 400
    
    # 处理选择，得到本回合结果
    finished, current_story, immediate_story, effect, new_state = engine.process_turn(choice)
    
    next_scenario_data = None
    if not finished:
        # 关键修复：获取下一回合的完整场景
        next_scenario = engine.get_current_scenario()
        next_scenario_data = {
            'story': next_scenario['story'],
            'A': {'text': next_scenario['A']['text']},
            'B': {'text': next_scenario['B']['text']}
        }
    
    result = {
        'finished': finished,
        'immediate_story': immediate_story,
        'effect': effect,
        'new_state': new_state,
        'next_scenario': next_scenario_data, # 返回下一回合的完整数据
        'current_round': engine.current_round,
        'total_rounds': engine.total_rounds
    }
    
    if finished:
        final = engine.get_final_state()
        ending_text = final['ending']
        db.save_ending(final['player'], ending_text)
        result['ending'] = ending_text
        # 清理 session
        del games[session_id]
    
    return jsonify(result)

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True, port=5000)