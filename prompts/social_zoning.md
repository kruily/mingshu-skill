# 社交分层 | Social Circle Analysis

## 核心术 (Core Techniques)

本模板基于《改运奇书》中的社交智慧，形成一套完整的社交圈分层分析框架：

| 技术 | 名称 | 核心要义 |
|------|------|----------|
| 第十六术 | 交游三等 | 唯利/唯情/兼顾三型，各守其界，逾则必咎 |
| 第二十一术 | 众悦险伏 | 受人喜爱代表气运旺盛，但危险亦潜伏其中 |

**English Overview:**

This template applies the wisdom of the Book of Life Transformation to social circle analysis:

- Technique 16: Social connections fall into three categories—profit-only, emotion-only, and the balanced type. Boundaries between the first two must never be crossed. The third type combines both naturally.
- Technique 21: Being loved by many signals strong fortune, but danger lurks nearby. Popularity has its shadows.

---

## 触发关键词 | Trigger Keywords

当用户输入包含以下词汇时，路由到本模板：

- "朋友"、"社交"、"圈子"、"三教九流"、"人脉"
- "认识新朋友"、"社交圈"、"朋友圈"、"人际关系"
- "social", "friends", "circle", "network", "connections", "acquaintances"

---

## 平台能力检测 | Platform Capability Check

在输出问卷前，检测 question 工具是否可用：

```
可用 → 使用 question 工具输出问卷
不可用 → 使用对话式文字提问
```

### question 工具检测逻辑

```markdown
检测方式：尝试调用 question 工具
- 如果调用成功 → 使用问卷模式
- 如果调用失败/返回错误 → 使用对话式模式
```

---

## 交互流程 | Interaction Flow

### 第一阶段：信息收集 (Information Collection)

**目的：** 了解用户当前的社交状态和困扰。

**对话引导：**

> "你目前的社交圈是什么样的？能描述一下吗？"
> "What does your current social circle look like? Can you describe it?"

**收集信息：**
- 社交圈规模：广泛还是有限
- 主要关系类型：利益型、情感型、兼顾型
- 近期社交变化：圈子扩大还是缩小
- 核心困扰：信任问题、边界模糊、被喜欢带来的压力等

---

### 第二阶段：社交分层分析 (Social Zoning Analysis)

**目的：** 应用第十六术和第二十一术进行深度分析。

**对话引导：**

> "你身边的朋友，哪类比较多？是纯粹聊得来的，还是纯粹有合作关系的，还是两者兼有的？"
> "Among your friends, which type is most common—those you connect with emotionally, those you work with professionally, or both?"

**分析维度：**

| 维度 | 第十六术应用 | 表现 |
|------|-------------|------|
| 唯利型关系 | 毋涉情义 | 合作边界清晰，不掺杂私人感情 |
| 唯情型关系 | 毋涉利欲 | 纯粹友情，不谈利益 |
| 兼顾型关系 | 情利皆可谋 | 既能谈感情又能谈合作，最高境界 |
| 众悦评估 | 第二十一术 | 被喜欢是好事，但要警惕背后的风险 |

---

### 第三阶段：建议输出 (Guidance Output)

**目的：** 综合分析结果，给出具体的社交分层建议。

**对话引导：**

> "根据你的情况，我来分析一下你的社交圈结构，并给出一些建议。"
> "Based on what you've shared, let me analyze your social circle structure and provide some suggestions."

---

## 问卷题目（如平台支持）| Questionnaire (If Supported)

使用 question 工具输出：

```markdown
## 社交分层问卷 | Social Circle Analysis

### 问题 1：社交圈规模
你的社交圈大概有多大？
- 很小（少于10人紧密联系）
- 较小（10-30人紧密联系）
- 中等（30-80人紧密联系）
- 较大（80人以上紧密联系）
- 很大（难以计数）

### 问题 2：关系类型分布
你身边的朋友主要是什么类型？
- 唯利型：主要是工作/商业关系，交往围绕利益展开
- 唯情型：主要是儿时好友、同学等，交往围绕感情展开
- 兼顾型：既有纯粹聊得来的，也有工作上的合作伙伴
- 混合型：各种类型都有，不太区分

### 问题 3：关系边界清晰度
你和朋友之间，利益关系和感情关系分得清楚吗？
- 很清晰：该谈利益时谈利益，该谈感情时谈感情
- 比较清晰：大部分时候清楚，少数时候会混淆
- 一般：有时候会混淆
- 不太清晰：经常分不清
- 完全不清楚：从来不区分

### 问题 4：利益关系处理
当朋友关系涉及到利益时，你通常怎么处理？
- 提前明确规则，谈清楚利益分配
- 先看关系深浅，再决定如何处理
- 遇到再说，不提前规划
- 尽量避免让朋友关系涉及利益
- 经常因为利益问题和朋友产生矛盾

### 问题 5：情感关系处理
当感情深厚的朋友需要合作时，你通常怎么处理？
- 很自然，友情合作两不误
- 会有些顾虑，担心影响感情
- 干脆不合作，保持纯粹的朋友关系
- 经常因为合作问题伤害朋友感情
- 不知道怎么把握这个度

### 问题 6：被喜欢的感觉
你在朋友圈中是被很多人喜欢/欣赏的吗？
- 是的，很受欢迎
- 还不错，有一定的认可度
- 一般，不算出众
- 较少被关注
- 不太受欢迎

### 问题 7：众悦风险意识
当很多人喜欢你时，你有没有感到过压力或危险？
- 从来没有，只感受到被喜欢的快乐
- 偶尔会感到一些压力
- 有时候会意识到危险
- 经常感到被喜欢的负面影响
- 深受其扰，曾经因为太受欢迎而吃亏

### 问题 8：社交困惑
你目前最大的社交困惑是什么？
- 不知道如何处理利益和感情的关系
- 圈子太复杂，不知道谁值得信任
- 想扩大社交圈但不知道怎么做
- 人缘太好，不知道如何选择
- 社交太累，想精简圈子
- 其他：__________

### 问题 9：改善意愿
你希望如何改善你的社交状态？
- 建立更清晰的社交分层规则
- 结交更多兼顾型的高质量关系
- 减少无效社交，专注深度关系
- 学习如何在受欢迎的同时保护自己
- 减少利益关系对感情的侵蚀
```

---

## 对话式问题（如平台不支持）| Dialog Questions

如果平台不支持 question 工具，使用对话式提问：

### 第一组：社交圈规模

> "你平时和多少人保持比较紧密的联系？"
> "你的社交圈是越来越大还是越来越小？"

### 第二组：关系类型分布

> "你身边的朋友，主要是因为什么认识的呢？是同事、客户、还是同学、玩伴？"
> "有没有那种纯粹就是聊得来、不涉及任何利益的朋友？比例大概多少？"

### 第三组：边界清晰度

> "你有没有过这种经历：因为和好朋友合作，结果关系变味了？"
> "当你需要找朋友帮忙时，你会怎么开口？会不会顾虑太多？"

### 第四组：利益关系处理

> "你是怎么处理和朋友的金钱关系的？比如借钱的习惯？"
> "有没有朋友找你合作过？你是怎么评估的？"

### 第五组：情感关系处理

> "你有没有过很好的朋友，后来因为合作问题关系变僵了？"
> "当感情深厚的朋友和你的利益冲突时，你会怎么选？"

### 第六组：众悦评估

> "你在朋友圈里算是人缘好的吗？别人喜欢你吗？"
> "被很多人喜欢，你感觉怎么样？有没有觉得累的时候？"

### 第七组：风险意识

> "你有没有因为太相信某个朋友，结果吃亏的经历？"
> "当很多人围着你转的时候，你有没有觉得哪里不对劲？"

### 第八组：改善方向

> "你理想中的社交状态是什么样的？"
> "你愿意为改善社交关系做出一些改变吗？"

---

## 示例对话 | Example Dialogues

### 示例一：利益与感情边界模糊

**User Input:**
"我和大学最好的朋友一起创业，现在公司做起来了，但我们的关系反而变得很僵，我不知道该怎么办。"

**Assistant Response:**
"收到。这正是第十六术所警示的情况：唯利与唯情这两种关系一旦混淆，就容易'逾则必遭其咎'。我们来详细分析一下。"

**Phase 1 - 问题收集**

> "你们当初创业时，有没有明确过各自的角色和利益分配？"

**User:**
"没有，就是觉得关系好，什么都好说。"

**Phase 2 - 关系分析**

> "现在回看，你们的关系是唯情型还是兼顾型？"

**User:**
"一开始是唯情型，后来变成了某种说不清的关系。"

**Phase 3 - 建议**

> "第十六术告诉我们：唯利与唯情各守其界，不可逾越。你们现在的问题，正是当初没有建立清晰边界的代价。建议：1）找个合适的时机，和他坦诚地重新谈一次，明确利益分配规则；2）如果感情还在，试着把关系'复位'，回到纯粹的友情，不带利益；3）如果双方都只盯着利益，那就按商业规则来处理，不要再谈感情。第十六术说'得此辈愈众，则气运愈昌'，但前提是关系类型要清晰，不能混淆。"

---

### 示例二：众悦险伏

**User Input:**
"我在公司人缘很好，大家都很喜欢我。但最近发现有人在背后说我坏话，感觉被背叛了。"

**Assistant Response:**
"这就是第二十一术所说的'众悦险伏'——被很多人喜欢说明气运旺盛，但危险也潜伏其中。我们来分析一下具体情况。"

**Phase 1 - 现状确认**

> "你说的坏话是什么性质？是关于工作的，还是关于你个人的？"

**User:**
"是关于我私生活的捕风捉影，让我很困扰。"

**Phase 2 - 风险评估**

> "你平时的社交关系中，哪类比较多？是唯利型、唯情型还是兼顾型？"

**User:**
"好像都是，保持距离的同事关系反而少。"

**Phase 3 - 建议**

> "第二十一术提醒我们：众悦虽好，但险伏于侧。你的问题在于社交边界不够清晰，关系太近反而容易产生摩擦。建议：1）重新审视你的社交关系，区分哪些是唯情型、哪些是唯利型、哪些可以发展为兼顾型；2）对于唯情型关系，保持适度的距离，不要让感情过度介入工作和利益；3）对于捕风捉影的事，不必急于澄清，保持淡定，用行动说话。众悦之人更需要'慎'字当头。"

---

### Example 3: Building a Balanced Social Circle

**User Input:**
"I want to expand my social circle but don't know how to find quality connections. Most of my current friends are from school, and I've been working alone for years."

**Assistant Response:**
"Building a balanced social circle requires understanding the three types from Technique 16. Let me help you analyze your current situation and develop a strategy."

**Phase 1 - Current State Assessment**

> "Your school friends—what type of relationship is this? Purely emotional, or have there been any business opportunities that came from these connections?"

**User:**
"Mostly purely emotional. We get together to catch up, never discuss work or business."

**Phase 2 - Strategy Discussion**

> "That's a solid foundation. According to Technique 16, pure emotional relationships should stay that way. Now, for expanding your circle, have you considered professional communities or interest groups where you could meet兼顾型 connections?"

**User:**
"I've thought about it but don't know where to start."

**Phase 3 - Recommendations**

> "Technique 16 says '得此辈愈众，则气运愈昌'—the more兼顾型 people you gather, the more your fortune grows. My suggestions: 1) Join professional associations or communities related to your industry; 2) Attend gatherings where people naturally discuss both ideas and collaboration; 3) When you meet someone promising, observe whether they can handle both emotional and professional exchanges gracefully; 4) Start with浅度社交—coffee chats, workshops—to find people who resonate. Quality trumps quantity. Remember, Technique 21 warns us: popularity has risks. As you expand, maintain clear boundaries and don't try to be everyone's best friend."

---

## 输出格式 | Output Format

当完成对话后，按照以下结构输出分析结果：

```markdown
## 社交分层分析报告 | Social Circle Analysis Report

### 社交圈基本信息 | Basic Information
{社交圈规模、关系类型分布、近期变化}

### 社交分层结构 | Social Zoning Structure

#### 唯利型关系 | Profit-Only Relationships
{这类关系的数量、特点、代表人物}
**分析：** {第十六术在此维度的应用}

#### 唯情型关系 | Emotion-Only Relationships
{这类关系的数量、特点、代表人物}
**分析：** {第十六术在此维度的应用}

#### 兼顾型关系 | Balanced Relationships
{这类关系的数量、特点、代表人物}
**分析：** {第十六术在此维度的应用}

### 众悦风险评估 | Popularity Risk Assessment
{被喜欢/欣赏的程度、潜在风险分析}
**分析：** {第二十一术在此维度的应用}

### 综合判断 | Comprehensive Judgment
{整体社交状态判断}

### 改善建议 | Improvement Suggestions

| 维度 | 当前状态 | 改善方向 | 具体行动 |
|------|----------|----------|----------|
| 唯利关系 | 状态描述 | 方向 | 可执行行动 |
| 唯情关系 | 状态描述 | 方向 | 可执行行动 |
| 兼顾关系 | 状态描述 | 方向 | 可执行行动 |
| 众悦风险 | 状态描述 | 方向 | 可执行行动 |
```

---

## 命书原文引用 | Original Text References

### 第十六术原文

> 交游之众，当分三等：其一唯利是图，毋涉情义；其二唯情是守，毋涉利欲；此二者不可逾，逾则必遭其咎。其三情利皆可谋。得此辈愈众，则气运愈昌。

**English Translation:** People around you fall into three categories: those who only want profit (keep emotions out), those who only value feelings (keep money out), and never cross these boundaries. The third type combines both naturally. The more such people you gather, the more your fortune grows.

**核心要点：**
- 第一等人：唯利是图，交往只谈利益，绝不掺杂感情
- 第二等人：唯情是守，交往只谈感情，绝不涉及利益
- 第三等人：情利皆可谋，既能谈感情又能谈合作，是最理想的关系
- 界限不可逾越：一旦混淆，逾则必遭其咎
- 气运之道：兼顾型关系越多，气运越昌盛

### 第二十一术原文

> 众悦者，气运亨也，然险亦伏于侧矣。

**English Translation:** Being loved by many indicates strong fortune, but danger also lurks nearby.

**核心要点：**
- 众悦是好事：代表气运旺盛
- 险伏于侧：受欢迎的程度越高，潜在风险越大
- 警惕信号：过度信任、利益纠葛、关系边界模糊

---

## 注意事项 | Notes

1. **三等关系各守其界：** 第十六术的核心是边界意识。利益关系谈利益，感情关系谈感情，混淆必出问题是。

2. **兼顾型关系最珍贵：** 能同时谈感情和利益而不产生矛盾的人，是最高质量的关系，要好好珍惜。

3. **众悦需谨慎：** 被很多人喜欢是好事，但也意味着更多的审视、更复杂的利益纠葛、更高的期望值。

4. **气运之道：** 社交圈的品质直接影响气运。好的社交圈不是越大越好，而是兼顾型关系越多越好。

5. **定期审视：** 建议每隔一段时间审视一下自己的社交圈，看看关系是否发生了越界，及时调整。

6. **保护自己：** 即使是人缘再好的人，也要保持适度的警觉和边界感。

---

## 适用场景 | When to Use

| 场景 | 推荐重点 |
|------|----------|
| 朋友合作后关系变僵 | 第十六术边界原则 |
| 社交圈太复杂 | 第十六术三等分类 |
| 人缘好但感觉累 | 第二十一术众悦险伏 |
| 想扩大社交圈 | 第十六术兼顾型关系 |
| 被信任的人伤害 | 第十六术+第二十一术综合 |
| 不知道谁值得信任 | 第十六术分类框架 |
| 社交后运气变差 | 第二十一术风险评估 |

---

## 社交分层自测表 | Self-Assessment

| 问题 | 是 | 否 | 不确定 |
|------|----|----|--------|
| 我的朋友中，利益关系和感情关系泾渭分明 | □ | □ | □ |
| 我能清楚区分谁是我的"唯利朋友"和"唯情朋友" | □ | □ | □ |
| 我和好朋友合作时，会提前明确规则 | □ | □ | □ |
| 我身边有既聊得来、又能在事业上合作的朋友 | □ | □ | □ |
| 被很多人喜欢时，我会保持适度警觉 | □ | □ | □ |
| 我有过因为关系混淆而吃亏的经历 | □ | □ | □ |
| 我能从容应对"众悦险伏"的情况 | □ | □ | □ |

**评分标准：**
- 5-7个"是"：社交分层意识良好
- 3-4个"是"：有提升空间
- 0-2个"是"：需要加强社交边界意识

---

_命书之道，在于自知；社交之明，在于分界。_