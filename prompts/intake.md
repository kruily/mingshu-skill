# User Difficulty Intake Template

## 意图判断 | Intent Detection

在收集困境之前，先判断用户意图：

### 意图类型

| 意图 | 判断条件 | 路由到 |
|------|---------|--------|
| **困境咨询** | 描述问题、寻求帮助、迷茫、不知道怎么办 | 继续本模板（intake） |
| **功能请求** | "帮我看人"、"分析一下"、"判断"、明确请求某个功能 | 直接路由到对应prompt |
| **求命书智慧** | "每日一术"、"随机一条"、"给我一条命书" | 每日一术 |
| **其他** | 不明确 | 每日一术 |

### 功能请求识别

当用户明确请求某个功能时，直接路由到对应prompt：

| 功能 | 触发词示例 | 路由到 |
|------|-----------|--------|
| 识人术 | "帮我看人"、"分析他"、"判断他"、"评估这个人" | people_reading.md |
| 言语分析 | "怎么说"、"这样说话"、"怎么表达" | guidance.md(言语分析) |
| 婚恋关系 | "分析关系"、"分析伴侣"、"分析夫妻" | relationship.md |
| 贵人识别 | "识别贵人"、"谁是我的贵人" | guidance.md(贵人识别) |
| 社交分层 | "分析社交"、"分析圈子" | social_zoning.md |
| 时机把握 | "判断时机"、"该不该"、"要不要" | guidance.md(时机把握) |
| 合作之道 | "评估合作"、"分析合伙人" | guidance.md(合作之道) |
| 财富管理 | "分析投资"、"财务分析" | wealth_management.md |

### 困境咨询后的延伸推荐

在完成困境咨询后，可以推荐相关功能作为延伸工具：
- 如果涉及人际关系问题 → 推荐"识人术"
- 如果涉及伴侣/感情问题 → 推荐"婚恋关系分析"
- 如果涉及时机选择困惑 → 推荐"时机把握"
- 如果涉及财务决策 → 推荐"财富管理"

推荐话术示例：
> "基于你的情况，命书第十术提到...如果你想深入分析[关系/人/时机],我可以帮你使用对应的命书分析工具。"

### 平台能力检测

在输出问卷前：
1. 检测 question 工具是否可用
2. 如果可用 → 使用 question 工具输出问卷
3. 如果不可用 → 使用对话式文字提问

### 默认路由

如果无法确定意图或没有匹配关键词，默认走"每日一术"流程。

## Purpose
Collect user-reported difficulty information when they encounter a challenging situation or technique. This template helps users articulate their 困境 (difficulties) clearly so that appropriate guidance can be provided.

## Guiding Questions

Use these questions to help users describe their situation:

1. **What is the current difficulty/problem?**
   - Describe specifically what you're struggling with
   - {user_description}

2. **How long has this been an issue?**
   - When did it start?
   - {duration}

3. **What have you tried before?**
   - List approaches you've attempted
   - {attempted_approaches}

4. **What is your emotional state regarding this?**
   - How does this difficulty make you feel?
   - {emotional_state}

5. **What kind of help/guidance are you seeking?**
   - What outcome do you hope for?
   - {help_type}

6. **What is the context where this difficulty occurs?**
   - Where/when does this problem manifest?
   - {context_where_encountered}

7. **How would you rate the difficulty level?**
   - Scale: 1 (easy) to 5 (extremely difficult)
   - {difficulty_rating}

## Structured Template

### User Input

**Problem Description:**
{user_description}

**Duration:**
{how_long_this_has_been_an_issue}

**Context:**
{context_where_encountered}

**Attempted Approaches:**
{what_user_tried_before}

**Emotional State:**
{user_feelings_about_this_difficulty}

**Expected Help:**
{what_kind_of_guidance_seeking}

**Difficulty Level (1-5):**
{difficulty_rating}

## Example Dialogues

### Example 1 (Chinese)
**User Input:**
- Problem: 在练习"凤凰起舞"时，手腕转动的角度总是不到位
- Duration: 已经练习了两周
- Context: 在练习混元步法时尝试结合手法
- Attempted: 看了视频教程，尝试模仿动作
- Emotion: 有些沮丧，担心影响进度
- Help: 希望得到具体的纠正方法
- Difficulty: 3

**Structured Output:**
```
**Problem Description:**
在练习"凤凰起舞"时，手腕转动的角度总是不到位

**Duration:**
已经练习了两周

**Context:**
在练习混元步法时尝试结合手法

**Attempted Approaches:**
看了视频教程，尝试模仿动作

**Emotional State:**
有些沮丧，担心影响进度

**Expected Help:**
希望得到具体的纠正方法

**Difficulty Level (1-5):**
3
```

### Example 2 (English)
**User Input:**
- Problem: Having trouble maintaining focus during evening meditation
- Duration: About a month
- Context: Usually meditate in my room after dinner
- Attempted: Tried different times, shorter sessions
- Emotion: Frustrated but willing to persist
- Help: Looking for techniques to improve concentration
- Difficulty: 4

**Structured Output:**
```
**Problem Description:**
Having trouble maintaining focus during evening meditation

**Duration:**
About a month

**Context:**
Usually meditate in my room after dinner

**Attempted Approaches:**
Tried different times, shorter sessions

**Emotional State:**
Frustrated but willing to persist

**Expected Help:**
Looking for techniques to improve concentration

**Difficulty Level (1-5):**
4
```

### Example 3 (Mixed/Bilingual)
**Problem Description:**
练习"蛟龙出海"第三式时，身体总是跟不上意念

**Duration:**
三天

**Context:**
每天早晨在公园练习

**Emotional State:**
感觉有点困惑，但不放弃

**Expected Help:**
想要了解身体和意念如何协调

**Difficulty Level (1-5):**
4

## Notes
- Support both Chinese and English input
- Use {placeholders} for variables to be filled by user
- The emotional state question helps understand the user's mindset for tailored guidance
- Both problem-focused and emotion-focused questions are included
