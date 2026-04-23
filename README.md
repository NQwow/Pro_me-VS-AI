# A-pygame: AI 驱动的文字冒险引擎

A-pygame 是一个基于 Python 和 Flask 构建的交互式文字冒险游戏（Text Adventure Game）。项目最初以命令行形式呈现，现已升级为现代化的 Web 界面，并集成了 AI 剧情生成模块。在这个世界里，你将面对各种抉择，你的每一个决定都会实时影响角色的属性与命运。

##  项目特色

*   **双模运行**：支持传统的命令行交互（CLI）和现代化的 Web 图形界面。
*   **AI 剧情生成**：接入智谱 AI (GLM-4) 接口，能够根据玩家的选择动态生成独一无二的剧情分支和结局。
*   **沉浸式 Web 体验**：采用精致的卡片式 UI 设计，提供实时的属性面板、冒险日志和流式剧情展示。
*   **多结局系统**：根据财富、能力、健康、运气四项核心属性的最终状态，触发数十种不同的生涯结局。
*   **数据持久化**：内置 MySQL 数据库支持，自动保存玩家的冒险记录与最终结局。

##  技术栈

*   **后端**: Python 3.7+, Flask, Flask-CORS
*   **前端**: HTML5, CSS3, JavaScript (原生)
*   **数据库**: MySQL (PyMySQL)
*   **AI 集成**: OpenAI SDK (兼容智谱 GLM-4 等模型)
*   **环境管理**: python-dotenv

##  快速开始

### 1. 环境准备

确保你的系统中已安装 Python 3.7+ 和 MySQL 数据库。

```bash
git clone https://github.com/NQwow/PYGame.git
cd PYGame
pip install flask flask-cors pymysql python-dotenv openai
```

### 2. 配置环境变量

在项目根目录下创建 `.env` 文件，并填入以下配置：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=pygame_db

# AI 接口配置 (可选，不填则使用模拟剧情)
ZHIPU_API_KEY=your_zhipu_api_key
```

### 3. 初始化数据库

运行 Python 脚本自动创建所需的数据表：

```python
import database as db
db.init_db()
```

### 4. 启动游戏

#### 方式一：启动 Web 版（推荐）
```bash
python app.py
```
启动后，在浏览器访问 `http://127.0.0.1:5000` 即可开始冒险。

#### 方式二：启动命令行版
```bash
python main.py
```

##  游戏玩法

1.  **角色创建**：你可以手动分配初始属性点，或选择随机生成。
2.  **回合制冒险**：游戏共进行 5 个回合。每回合你会面临两个截然不同的选项。
3.  **属性博弈**：
    *   **财富**：影响你的生活质量和资源获取。
    *   **能力**：决定你解决技术难题的效率。
    *   **健康**：生命的基石，归零即宣告游戏失败。
    *   **运气**：影响突发事件的走向。
4.  **结局判定**：当回合结束或任意属性归零时，游戏将根据你的生平生成专属结局。

##  项目结构

```text
.
├── app.py              # Flask Web 服务器入口
├── main.py             # 命令行版本入口
├── game_engine.py      # 游戏核心逻辑与状态管理
├── model.py            # 玩家数据模型定义
├── ai_client.py        # AI 剧情生成客户端（含模拟数据逻辑）
├── database.py         # 数据库操作与结局持久化
├── utils.py            # 通用工具函数
├── templates/
│   └── index.html      # Web 端游戏主界面
└── README.md           # 项目说明文档
```

##  开发计划

- [ ] 增加“记忆系统”，让 AI 能更准确地引用之前的关键决策。
- [ ] 完善 Web 端的“往昔纪传”功能，支持查看历史结局列表。
- [ ] 优化移动端适配，提供更完美的手机端阅读体验。

##  许可证

本项目仅供学习与交流使用。


```