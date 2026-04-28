# 命书 Ming Shu 安装指南 | Installation Guide

---

## For Humans

将以下内容粘贴给你的 Agent：

```
请帮我安装命书 skill：https://github.com/kruily/ming-shu

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
└── tools/              # 工具
```

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

---

> 本技能内容基于《改运奇书》小说中的命书，仅供娱乐参考。