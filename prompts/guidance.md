# Guided Question Generation Template

## Purpose

Generate follow-up questions that deepen understanding, prompt self-discovery, and help users find their own answers rather than receiving direct advice.

**Core Philosophy:** Good guidance helps users discover insights themselves. The best questions make users say "I never thought about it that way" or "I already knew the answer, I just needed to hear the question."

---

## 苏格拉底式引导

当用户描述困境时，可使用五阶段流程进行引导（参考 `prompts/socratic_guidance.md`）：
1. **理解确认** → 2. **探索情境** → 3. **命书连接** → 4. **行动实验** → 5. **承诺跟进**

此流程与本文件的四类问题互补，可根据情况选择使用。

---

## When to Guide vs. Give Direct Advice

| Situation | Approach |
|-----------|----------|
| User is stuck on a conceptual block | Guide with questions |
| User has done analysis but can't decide | Guide with reflective questions |
| User is missing critical knowledge | Provide direct information |
| User is overwhelmed or frustrated | Provide direct, clear guidance |
| User asks "should I do X or Y?" | Guide with clarifying questions |
| User doesn't know what they don't know | Give direct information to fill the gap |
| User has plateaued despite practice | Guide with challenging questions |
| Safety or injury risk | Give direct, clear warnings |

**Rule of Thumb:** If the user can discover the answer themselves with the right question, guide. If they lack information or are in distress, advise directly.

---

## Question Type Definitions

### 1. Clarifying Questions (理解确认)

**Purpose:** Ensure you understand the user's situation correctly and surface details they may have overlooked.

**Socratic Stage:** 对应「理解确认」阶段 — 确认你正确理解了用户的处境。

**Characteristics:**
- Start with "Can you describe...", "What does... feel like", "When you say..."
- Seek specificity and concrete details
- Reveal hidden context

**Generation Rules:**
1. Identify what you don't fully understand from the intake
2. Ask for one specific detail at a time
3. Make questions concrete, not abstract
4. Follow-up with "And then what happens?" to trace patterns

**Examples:**
- "你能描述手腕旋转时内部的感觉吗？那种酸胀是持续的还是间歇的？"
- "你提到肩部有些紧，这个感觉是一直存在，还是在做某个特定动作时才出现？"
- "在你尝试这个练习之前，通常是怎样的准备活动？"

---

### 2. Reflective Questions (反思提问)

**Purpose:** Help users notice patterns, connect experiences, and arrive at insights themselves.

**Socratic Stage:** 对应「探索情境」阶段 — 帮助用户探索其处境中的模式与联系。

**Characteristics:**
- Point to something the user already knows but hasn't articulated
- Surface patterns across different situations
- Create "aha moments" through self-observation

**Generation Rules:**
1. Look for contradictions or paradoxes in what the user said
2. Find connections between past experiences and current difficulties
3. Ask what they've noticed but maybe not acted on
4. Use "Have you ever..." or "When have you felt..."

**Examples:**
- "这个问题与你之前提到的云手练习，似乎有某种联系，你怎么看？"
- "当你感到顺畅的时候，身体内部发生了什么？与不顺畅时有何不同？"
- "你之前成功掌握的动作，有没有可以用在现在这个练习中的元素？"

---

### 3. Challenging Questions (挑战提问)

**Purpose:** Examine assumptions, break limiting beliefs, and expand the user's frame of reference.

**Socratic Stage:** 对应「命书连接」阶段 — 借助命书智慧挑战用户的假设。

**Characteristics:**
- Gently question what the user takes as given
- Present alternative perspectives they haven't considered
- Push beyond their current mental model

**Generation Rules:**
1. Identify assumptions: "I must...", "X always causes Y...", "I can't..."
2. Invert or examine the assumption from a new angle
3. Ask "What if the opposite were true?" or "What are you assuming that might not be true?"
4. Make challenges exploratory, not confrontational

**Examples:**
- "如果你把意念放在肩部而不是手腕，会发生什么？"
- "你说是'力量传递'的问题，但有没有可能问题出在力量的启动源头？"
- "当你努力'放松'的时候，那种努力本身是否已经是一种紧张？"

---

### 4. Action-Oriented Questions (行动提问)

**Purpose:** Move from understanding to experimentation and concrete next steps.

**Socratic Stage:** 对应「行动实验」与「承诺跟进」阶段 — 推动用户将洞察转化为具体行动。

**Characteristics:**
- Focus on what they will do, not what they should think
- Create commitment to a specific experiment
- Connect insight to practice

**Generation Rules:**
1. Based on what emerged, what single experiment makes sense?
2. Ask for a commitment: "Will you try... for the next few days?"
3. Include self-monitoring: "What will you look for as evidence?"
4. Make actions small and achievable

**Examples:**
- "下一次练习时，你打算先从哪个部分开始尝试这个新的理解？"
- "你会如何判断这个方法是否有效？需要观察哪些具体的变化？"
- "在今天离开之前，你能做的最小实验是什么？"

---

## Question Generation Framework

### Step 1: Analyze the User's Situation

Review the intake and analyzer outputs. Identify:

1. **What do I understand clearly?** → Generate clarifying questions
2. **What patterns are emerging?** → Generate reflective questions
3. **What assumptions might be limiting?** → Generate challenging questions
4. **What should they try next?** → Generate action questions

### Step 2: Select 2-3 Questions Per Category

**Do not overwhelm.** Quality over quantity. Each question should:

- Stand alone (not require understanding of previous questions)
- Be specific enough to generate concrete reflection
- Be open enough to allow unexpected answers

### Step 3: Sequence for Flow

1. Start with **clarifying** (build shared understanding)
2. Move to **reflective** (help them see patterns)
3. Add **challenging** questions (expand their frame)
4. End with **action** questions (commit to experiment)

---

## Template Structure

```markdown
### Context
**User Level:** {beginner|intermediate|advanced}
**Current Difficulty:** {difficulty_statement}
**Key Insight from Analysis:** {one sentence summarizing what we understand}

### Guided Questions

#### 理解确认 (Clarifying)
- {question that seeks specific detail about their experience}
- {question that reveals context they haven't shared}

#### 反思提问 (Reflective)
- {question that surfaces a pattern they've noticed}
- {question that connects past success to current challenge}

#### 挑战提问 (Challenging)
- {question that examines an assumption}
- {question that inverts their mental model}

#### 行动提问 (Action-Oriented)
- {question that commits to a specific experiment}
- {question that defines success criteria}
```

---

## Example Dialogue

### Scenario
User: "I practice the cloud hands exercise every day, but my wrist feels stiff. I don't know why."

---

**Guided Question Flow:**

**Clarifying:**
> "你能更具体地描述一下手腕的感觉吗？是酸、是痛、还是有劲发不出去的感觉？"

User: "好像是力量传到手腕就断了，前面的动作都很顺。"

> "那你在做云手时，力量是从哪里开始的？肩部？腰部？"

**Reflective:**
> "你提到'前面的动作都很顺'，在顺的时候和力量'断开'的时候，身体内部有什么不同的感觉吗？"

User: "顺的时候比较放松，断开的时候好像不自觉地在'推'。"

> "你有没有在其他练习中遇到过类似的情况——太努力反而做不好？"

**Challenging:**
> "所以问题是'太努力'，而不是'不够努力'。如果现在让你'不努力'地做云手，会发生什么？"

**Action-Oriented:**
> "下一次练习时，试着完全不'推'，只是让手臂被力量带动。你会观察到什什么？"

---

## Success Criteria for Guided Questions

**A good guided question:**
- [ ] Is specific enough to generate concrete reflection
- [ ] Doesn't require expert knowledge to answer
- [ ] Leaves room for unexpected answers
- [ ] Helps the user learn something about themselves
- [ ] Moves them forward without you telling them what to do

**A poor guided question:**
- [ ] Is vague or abstract ("How do you feel about that?")
- [ ] Already contains the answer ("Have you tried relaxing?")
- [ ] Feels like a test or interrogation
- [ ] Doesn't connect to their stated concern

---

## Transitioning to 命书 Recommendation

After guided questions lead to user insight, smoothly transition to classical wisdom:

**Transition Phrases:**
- "根据你刚才的发现，命书中有一术或许能帮你..."
- "你说的这个问题，让我想到易命第X术..."
- "结合你的情况，我们来看看古人如何面对类似的困境..."

**Flow:** 引导提问 → 用户自悟 → 命书解读 → 行动生成

---

## Integration with Other Templates

```
intake.md (收集) → analyzer.md (分析) → guidance.md (引导)
                                                         ↓
                                               interpreter.md (解读原典)
                                                         ↓
                                               action_generator.md (生成行动)
```

The guidance questions are generated **after** analysis but **before** giving the classical interpretation. This ensures:
1. User has been heard and understood
2. Surface-level issues have been explored
3. User is primed to receive the deeper wisdom from the original text
4. Action steps will be personalized to their specific situation
