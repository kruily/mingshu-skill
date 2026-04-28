# 命书 Ming Shu 安装指南 | Installation Guide

---

## For Humans

将以下内容粘贴给你的 Agent：

```
请帮我安装命书 skill：https://github.com/kruily/mingshu-skill/blob/main/INSTALL.md

安装完成后，输入 /ming-shu 或"每日一术"开始使用。
```

---

## For LLM Agents

If you're an LLM Agent helping set up ming-shu skill, follow these steps:

### Step 1: Detect Platform

| 平台 | 检测方式 |
|------|----------|
| Hermes | 有 `hermes` 命令 |
| OpenClaw | 有 `clawhub` 或 `npx clawhub` |
| Claude Code | 有 `claude` 命令 |
| Codex | 有 `codex` 命令 |

### Step 2: Install

**Hermes:**
```bash
hermes skills add ming-shu --repo https://github.com/kruily/ming-shu
```

**OpenClaw:**
```bash
npx clawhub@latest install ming-shu
```

**Claude Code:**
```bash
git clone https://github.com/kruily/ming-shu ~/.claude/skills/ming-shu
```

**Codex:**
```bash
git clone https://github.com/kruily/ming-shu ~/.codex/skills/ming-shu
```

### Step 3: Verify

```bash
# Hermes
hermes skills list | grep ming-shu

# OpenClaw
openclaw skills list

# Claude Code/Codex
ls ~/.claude/skills/ming-shu
```

### Step 4: Test

告诉用户输入：
- `/ming-shu` - 随机获取一条命书智慧
- `每日一术` - 每日一术功能

---

## Platform Details Table

| 平台 | 安装路径 | 使用命令 |
|------|----------|----------|
| Hermes | `~/.hermes/skills/ming-shu` | `/ming-shu` |
| OpenClaw | `~/.openclaw/skills/ming-shu` | `/ming-shu` |
| Claude Code | `~/.claude/skills/ming-shu` | `/ming-shu` |
| Codex | `~/.codex/skills/ming-shu` | `/ming-shu` |

---

## Directory Structure

```
ming-shu/
├── SKILL.md              # 入口
├── references/          # 命书原文
├── prompts/             # 交互模板
│   ├── journal_intake.md        # 日记打卡收集
│   ├── journal_feedback.md       # AI分析反馈
│   ├── socratic_guidance.md     # 苏格拉底引导
│   └── reminder_templates.md    # 早晚提醒模板
└── tools/               # 工具
    ├── journal_manager.py       # 日记管理CLI
    ├── reminder_scheduler.py    # 提醒调度器
    └── memory_sync.py           # 记忆同步
```

---

## Platform-Specific Automation Features

Both Hermes and OpenClaw support scheduling. These are **optional** features that enhance the ming-shu experience.

### Hermes Agent - Scheduling

Hermes has a built-in cron scheduler. Use natural language or `/cron` command:

**Natural language (in chat):**
```
"Every morning at 7:30 AM, send me a daily ming-shu technique"
"Every evening at 9 PM, remind me to record my journal"
```

**Using /cron command:**
```
/cron add "0 7 * * *" "Send me today's 易命术 with action suggestions"
/cron add "0 21 * * *" "Remind me to use journal_manager.py to record today's reflection"
```

**Key commands:**
| Command | Description |
|---------|-------------|
| `/cron list` | List all scheduled jobs |
| `/cron pause <id>` | Pause a job |
| `/cron resume <id>` | Resume a job |
| `/cron run <id>` | Trigger immediately |
| `/cron remove <id>` | Delete job |

**Configuration** (`~/.hermes/config.yaml`):
```yaml
scheduler:
  enabled: true
  timezone: Asia/Shanghai
```

---

### OpenClaw - Scheduling

OpenClaw uses `cron` with session styles:

**Morning reminder:**
```bash
openclaw cron add \
  --name "ming-shu-morning" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "Give me today's 易命术 with action suggestions" \
  --announce
```

**Evening reminder:**
```bash
openclaw cron add \
  --name "ming-shu-evening" \
  --cron "0 21 * * *" \
  --tz "Asia/Shanghai" \
  --session main \
  --message "Reminder: Use journal_manager.py to record today's reflection" \
  --announce
```

**Session styles:**
| Style | Description | Best for |
|-------|-------------|----------|
| `main` | Context-aware | Reminders, system events |
| `isolated` | Fresh session | Reports, background tasks |

**Key commands:**
| Command | Description |
|---------|-------------|
| `openclaw cron list` | List all jobs |
| `openclaw cron run <id>` | Trigger immediately |
| `openclaw cron edit <id> --disable` | Pause |
| `openclaw cron remove <id>` | Delete |

---

### Quick Setup Examples

**For Hermes (natural language):**
```
"Set up my ming-shu practice:
 - Morning at 7:30 AM: send me a random technique with action suggestions
 - Evening at 9:30 PM: remind me to record my journal"
```

**For OpenClaw (CLI):**
```bash
# Morning
openclaw cron add --name "ming-shu-am" --cron "0 7 * * *" --session isolated --message "Today's 易命术" --announce
# Evening
openclaw cron add --name "ming-shu-pm" --cron "0 21 * * *" --session main --message "Record your reflection" --announce
```

---

### Built-in CLI Tools

```bash
# Journal management
python3 tools/journal_manager.py add --user <id> --situation "..." --techniques "第五术"
python3 tools/journal_manager.py stats --user <id>
python3 tools/journal_manager.py streak --user <id>

# Reminder scheduling
python3 tools/reminder_scheduler.py schedule --user <id> --type morning
python3 tools/reminder_scheduler.py send-now --user <id> --type evening --dry-run

# Memory sync
python3 tools/memory_sync.py sync --user <id>
python3 tools/memory_sync.py search --query "焦虑"
```

---

### Optional Features Summary

| Feature | Hermes | OpenClaw | Status |
|---------|--------|----------|--------|
| Morning Reminder | ✅ | ✅ | Optional |
| Evening Reminder | ✅ | ✅ | Optional |
| Journal Tracking | ✅ tools | ✅ tools | Optional |
| Socratic Guidance | ✅ auto | ✅ auto | Built-in |

All automation features are **opt-in**. Core ming-shu works without scheduling.

---

## Troubleshooting

**Q: 安装后找不到 ming-shu？**
A: 检查目录是否存在，重启终端

**Q: 如何卸载？**
```bash
rm -rf ~/.claude/skills/ming-shu  # Claude Code
rm -rf ~/.hermes/skills/ming-shu  # Hermes
rm -rf ~/.openclaw/skills/ming-shu # OpenClaw
rm -rf ~/.codex/skills/ming-shu   # Codex
rm -rf ~/.ming-shu-memory/         # 记忆数据
```

**Q: 定时任务不执行？**
- Hermes: 确保 `hermes cron start` 在运行，或使用 `pm2 start hermes` 保持后台
- OpenClaw: 检查 `~/.openclaw/cron/jobs.json`，查看 `openclaw cron list`

---

> 本技能内容基于《改运奇书》小说中的命书，仅供娱乐参考。