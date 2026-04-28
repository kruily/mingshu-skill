# Difficulty Analysis Template

## Purpose
Analyze user difficulty descriptions and match with appropriate interpretation techniques from the 41 命术.

## Matching Flow

```
用户输入 → 语义提取 → 情绪识别 → 领域分类 → 关键词匹配 → 候选排序 → 最终选择(1-2术)
```

## Semantic Analysis Logic

### 1. Core Difficulty Extraction
Identify the **central concept** expressed by the user:
- What is the actual problem being described?
- What is the underlying cause or symptom?
- What dimension of life does it touch?

### 2. Emotional Undertone Recognition
Map emotional signals to technique categories:

| 情绪 | 可能对应的领域 | 相关命术 |
|------|--------------|---------|
| 焦虑、急躁、坐立不安 | 处世哲学-节奏/耐心 | 第31术(勿急) |
| 迷茫、困惑、不知所措 | 做事智慧-方向选择 | 第6术其二(康庄大道) |
| 沮丧、消沉、想放弃 | 处世哲学-自我激励 | 第38术(深坑爬出)、第37术(勿自怜) |
| 恐惧、害怕、担忧 | 处世哲学-直面恐惧 | 第36术(正对内惧) |
| 愤怒、生气、怨恨 | 财富之道-情绪管理 | 第34术(怒则智散) |
| 后悔、纠结、反复回想 | 言行修养-放下执念 | 第5术(旧过勿恋)、第28术(勿自贻伊威) |
| 孤独、无人理解 | 人际之道-贵人识别 | 第9术(初遇生人)、第10术(贵人) |
| 疲惫、压力过大 | 环境健康-生活节奏 | 第2术(四时有序) |

### 3. Context Category Mapping
Map problem domains to technique categories:

| 领域 | 关键词 | 对应命术范围 |
|------|--------|-------------|
| 事业/工作 | 创业、投资、合作、项目、事业、转型 | 第8术(旧业勿轻弃)、第16术(交游分三等)、第18术(共事三要素)、第25术(投资如博戏)、第41术(破釜沉舟) |
| 财富/金钱 | 钱、赚钱、亏损、投资、债务、节省 | 第4术(取利之道)、第25术(投资风险)、第26术(用财之道)、第27术(勿求险)、第32术(勿占便宜)、第33术(借财还利) |
| 人际关系 | 朋友、夫妻、贵人、合作、信任、陌生人 | 第9术(识人)、第19术(试友)、第22术(夫妇之道)、第30术(用度可奢) |
| 健康/环境 | 身体、环境、睡眠、饮食、作息 | 第1术(环境整洁)、第2术(四时有序) |
| 决策/行动 | 选择、犹豫、判断、时机、运气 | 第6术(顺应天时)、第15术(判事成否)、第17术(方时运至)、第35术(避而俟之) |
| 内心/修养 | 心态、修养、贪婪、恐惧、自我 | 第7术(不贪)、第11术(事未成勿泄)、第12术(竭诚以赴)、第13术(识人)、第14术(御人之疑)、第20术(困厄自疏)、第28术(勿自贻伊威)、第29术(鉴物勿溺)、第36术(正对内惧)、第37术(勿自怜)、第39术(念所有)、第40术(灵根身树) |

## Technique Selection Algorithm

### Step 1: Collect Candidate Techniques
For each matched category, collect all techniques. Score each technique:

### Step 2: Score by Relevance
- **Direct keyword match**: 3 points
- **Semantic similarity**: 2 points
- **Emotional undertone alignment**: 2 points
- **Same category as primary concern**: 1 point

### Step 3: Select Top 2
Select the **highest-scoring 1-2 techniques** that address:
1. The **core difficulty** (highest priority)
2. The **root cause** (if different from core)

### Selection Constraints
- If multiple techniques tie, prefer: 做事智慧 > 处世哲学 > 人际之道 > 财富之道 > 言行修养 > 环境健康
- If user explicitly mentions a domain, prioritize that domain's techniques

## Template

### Input
**User Description:**
{user_difficulty_description}

### Semantic Analysis
**Core Difficulty:**
{core_difficulty_concept_extracted}

**Physical/External Components:**
- {component_1}
- {component_2}

**Mental/Internal Components:**
- {mental_aspect_1}
- {mental_aspect_2}

**Identified Emotions:**
- {emotion_1} → suggests {related_domain}
- {emotion_2} → suggests {related_domain}

**Primary Category:** {category}
**Secondary Category:** {category}

### Technique Matching
**Candidate Techniques (scored):**
1. {technique_name} ({第X术}) - Score: {score}/10
   - Match reason: {why_this_technique}
2. {technique_name} ({第X术}) - Score: {score}/10
   - Match reason: {why_this_technique}

**Selected Technique(s):**
1. **{technique_name}** - Relevance: {relevance}/10
   - Rationale: {why_this_is_primary_solution}
2. **{technique_name}** - Relevance: {relevance}/10
   - Rationale: {complementary_or_alternative}

**Analysis Summary:**
{summary_of_how_difficulty_leads_to_technique_selection}

---

## Example

### Input
**User Description:**
"最近工作压力特别大，每天加班到很晚，感觉自己快要撑不下去了。晚上睡不着，白天没精神，对什么都提不起兴趣。同事都说我最近脾气变差了，我也知道这样不好，但就是控制不住。"

### Semantic Analysis
**Core Difficulty:**
身心俱疲，情绪失控，失去生活与工作的平衡

**Physical/External Components:**
- 作息紊乱（加班、晚睡）
- 身体疲劳（精力透支）

**Mental/Internal Components:**
- 焦虑情绪（控制不住脾气）
- 消沉倾向（提不起兴趣）
- 自我否定（知道不好但无法改变）

**Identified Emotions:**
- 疲惫、焦虑 → 建议节奏调整
- 沮丧、失控 → 建议情绪管理与自我认知
- 愤怒（对自身） → 第34术关联

**Primary Category:** 环境健康 (作息与身心节奏)
**Secondary Category:** 处世哲学 (自我认知与接纳)

### Technique Matching
**Candidate Techniques (scored):**
1. 易命第二术(四时有序) - Score: 9/10
   - Match reason: 直接对应作息紊乱问题，"应时而兴，应时而食，应时而作，应时而息"
2. 易命第三术(言善心真) - Score: 5/10
   - Match reason: 涉及脾气控制，但非核心
3. 易命第三十一术(勿急) - Score: 6/10
   - Match reason: 急躁情绪相关，但范围较窄
4. 易命第二术(环境整洁) - Score: 4/10
   - Match reason: 间接相关，非主要

**Selected Technique(s):**
1. **易命第二术** - Relevance: 9/10
   - Rationale: 用户核心问题是作息紊乱导致的身心失衡。第二术"四时有序"直接对应——该起床时起床，该吃饭时吃饭，该工作时工作，该睡觉时睡觉。恢复生活节奏是解决一切问题的基础。

2. **易命第三十一术** - Relevance: 6/10
   - Rationale: 作为补充，"勿急"帮助用户在恢复节奏的过程中放下急躁心态。心神乃一，先有外在节奏的恢复，才有内在心态的平和。

**Analysis Summary:**
用户描述的核心是身心失衡的第二术（第二层身体，第三层心理，第四层事业）。"四时有序"解决根本的生活方式问题，"勿急"帮助调整急于求成的心态。两术配合，先调整生活节奏，再调整做事节奏，层层递进。

---

## Category Reference

| 类别 | 命术编号 | 核心主题 |
|------|---------|---------|
| 环境健康 | 1, 2 | 整洁、节奏 |
| 言行修养 | 3, 5, 12 | 言语、诚意、专注 |
| 财富之道 | 4, 25, 26, 27, 32, 33, 34 | 取利、用财、勿贪、情绪 |
| 人际之道 | 9, 19, 22, 30 | 识人、交友、夫妇、用度 |
| 做事智慧 | 6, 15, 16, 17, 18, 38, 41 | 顺势、判事、合作、行动 |
| 处世哲学 | 7, 8, 10, 11, 13, 14, 20, 21, 23, 24, 28, 29, 31, 35, 36, 37, 39, 40 | 不贪、贵人、自知、淡定 |
