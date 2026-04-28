#!/usr/bin/env python3
"""
Journal Manager for Ming Shu - Manages journal entries, statistics, and insights.
Stores data in {skill_dir}/data/journal.json (single-user, skill directory based)
"""

import json
import argparse
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

# Skill directory based storage (single user)
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
JOURNAL_FILE = DATA_DIR / "journal.jsonl"


class JournalManager:

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.journal_file = self.data_dir / "journal.jsonl"

    def _load_entries(self) -> list:
        entries = []
        if self.journal_file.exists():
            with open(self.journal_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entries.append(json.loads(line))
        return entries

    def _get_next_id(self) -> int:
        entries = self._load_entries()
        return len(entries) + 1

    def add_entry(
        self,
        situation: str,
        techniques: str,
        effectiveness: int,
        tags: Optional[list] = None,
        notes: Optional[str] = None
    ) -> dict:
        entry = {
            "id": self._get_next_id(),
            "timestamp": datetime.now().isoformat(),
            "situation": situation,
            "techniques": techniques,
            "effectiveness": effectiveness,
            "tags": tags or [],
            "notes": notes
        }

        with open(self.journal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return entry

    def get_entries(self, limit: int = 10) -> list:
        entries = self._load_entries()
        return entries[-limit:] if limit > 0 else entries

    def get_stats(self) -> dict:
        journal = self._load_entries()

        if not journal:
            return {
                "total_entries": 0,
                "total_days_practiced": 0,
                "current_streak": 0,
                "best_streak": 0,
                "average_effectiveness": 0,
                "most_used_techniques": [],
                "tag_distribution": {},
                "situation_distribution": {}
            }

        total_entries = len(journal)
        effectiveness_sum = sum(e.get("effectiveness", 0) for e in journal)
        avg_effectiveness = effectiveness_sum / total_entries if total_entries > 0 else 0

        dates = []
        for entry in journal:
            try:
                dt = datetime.fromisoformat(entry["timestamp"])
                dates.append(dt.date())
            except (ValueError, KeyError):
                continue

        unique_dates = sorted(set(dates))
        total_days = len(unique_dates)

        current_streak, best_streak = self._calculate_streaks(unique_dates)

        techniques_counter = Counter(e.get("techniques", "") for e in journal)
        most_used = techniques_counter.most_common(5)

        all_tags = []
        for entry in journal:
            all_tags.extend(entry.get("tags", []))
        tag_dist = dict(Counter(all_tags).most_common(10))

        situations = [e.get("situation", "") for e in journal]
        situation_dist = dict(Counter(situations).most_common(10))

        stats = {
            "total_entries": total_entries,
            "total_days_practiced": total_days,
            "current_streak": current_streak,
            "best_streak": best_streak,
            "average_effectiveness": round(avg_effectiveness, 2),
            "most_used_techniques": most_used,
            "tag_distribution": tag_dist,
            "situation_distribution": situation_dist
        }

        return stats

    def _calculate_streaks(self, unique_dates: list) -> tuple:
        if not unique_dates:
            return 0, 0

        today = datetime.now().date()
        current_streak = 0
        best_streak = 0
        temp_streak = 1

        if unique_dates[-1] == today:
            current_streak = 1
            check_date = today - timedelta(days=1)
        elif unique_dates[-1] == today - timedelta(days=1):
            current_streak = 1
            check_date = today - timedelta(days=2)
        else:
            check_date = None

        if check_date:
            for i in range(len(unique_dates) - 2, -1, -1):
                if unique_dates[i] == check_date:
                    current_streak += 1
                    check_date -= timedelta(days=1)
                else:
                    break

        for i in range(1, len(unique_dates)):
            if unique_dates[i] - unique_dates[i - 1] == timedelta(days=1):
                temp_streak += 1
            else:
                best_streak = max(best_streak, temp_streak)
                temp_streak = 1
        best_streak = max(best_streak, temp_streak)

        return current_streak, best_streak

    def get_streak(self) -> dict:
        stats = self.get_stats()
        return {
            "current_streak": stats.get("current_streak", 0),
            "best_streak": stats.get("best_streak", 0),
            "total_days": stats.get("total_days_practiced", 0)
        }

    def generate_insights(self) -> list:
        journal = self._load_entries()

        if len(journal) < 3:
            return ["记录太少，无法生成有意义的洞察。继续记录以获取个性化建议。"]

        insights = []
        stats = self.get_stats()

        techniques_by_situation = defaultdict(list)
        for entry in journal:
            situation = entry.get("situation", "")
            technique = entry.get("techniques", "")
            effectiveness = entry.get("effectiveness", 0)
            if situation and technique:
                techniques_by_situation[situation].append((technique, effectiveness))

        for situation, entries in techniques_by_situation.items():
            if len(entries) >= 2:
                tech_counter = Counter(e[0] for e in entries)
                most_common_tech = tech_counter.most_common(1)[0]
                insights.append(
                    f"你在「{situation}」场景最常用{most_common_tech[0]}，"
                    f"共使用{most_common_tech[1]}次"
                )

        all_situations = [e.get("situation", "") for e in journal]
        situation_counter = Counter(all_situations)
        if situation_counter:
            most_common_situation = situation_counter.most_common(1)[0]
            least_common = situation_counter.most_common()[-1]

            if len(situation_counter) >= 2:
                insights.append(
                    f"建议尝试在「{least_common[0]}」场景应用你擅长的技巧，"
                    f"目前主要在「{most_common_situation[0]}」场景练习"
                )

        recent_effectiveness = [e.get("effectiveness", 0) for e in journal[-5:]]
        if recent_effectiveness:
            avg_recent = sum(recent_effectiveness) / len(recent_effectiveness)
            if avg_recent >= 4:
                insights.append("近期效果评分很高！继续保持当前的方法。")
            elif avg_recent >= 3:
                insights.append("近期效果评分稳定，可以尝试突破更高难度的场景。")
            else:
                insights.append("近期效果有提升空间，建议回顾笔记，思考哪些场景最有效。")

        tag_dist = stats.get("tag_distribution", {})
        if tag_dist:
            top_tags = list(tag_dist.keys())[:3]
            if top_tags:
                insights.append(f"你最关注的领域是：{', '.join(top_tags)}")

        return insights

    def get_ai_feedback(self) -> str:
        stats = self.get_stats()
        insights = self.generate_insights()

        if stats["total_entries"] == 0:
            return (
                "欢迎开始你的命书之旅！"
                "记录你第一次使用易命术的情境，我会根据你的实践提供个性化反馈。\n"
                "使用示例：\n"
                '  python3 tools/journal_manager.py add --situation "工作汇报" '
                '--techniques "第五术" --effectiveness 4'
            )

        feedback_parts = []

        current_streak = stats["current_streak"]
        if current_streak >= 7:
            feedback_parts.append(f"太棒了！你已经连续练习{current_streak}天，习惯正在养成。")
        elif current_streak >= 3:
            feedback_parts.append(f"不错的开始！你已连续练习{current_streak}天。")
        elif current_streak > 0:
            feedback_parts.append(f"你当前连续练习{current_streak}天，继续保持！")
        else:
            feedback_parts.append("今天是你重新开始的好日子！")

        total = stats["total_entries"]
        total_days = stats["total_days_practiced"]
        avg_eff = stats["average_effectiveness"]

        feedback_parts.append(
            f"你共记录了{total}次练习，涵盖{total_days}天，"
            f"平均效果评分{avg_eff}分。"
        )

        top_tech = stats.get("most_used_techniques", [])
        if top_tech:
            top_tech_str = "、".join([f"{t[0]}({t[1]}次)" for t in top_tech[:3]])
            feedback_parts.append(f"你最常用的是：{top_tech_str}。")

        if insights:
            feedback_parts.append("\n个性化洞察：")
            for insight in insights[:3]:
                feedback_parts.append(f"  • {insight}")

        suggestions = []
        if avg_eff < 3:
            suggestions.append("尝试在更有把握的情境中先练习，提升信心。")
        if current_streak < 3 and total > 5:
            suggestions.append("建议每天记录，形成习惯后更容易看到进步。")
        if len(stats.get("situation_distribution", {})) < 3:
            suggestions.append("尝试在不同场景应用技巧，比如人际沟通、决策判断等。")

        if suggestions:
            feedback_parts.append("\n建议：")
            for s in suggestions:
                feedback_parts.append(f"  • {s}")

        feedback_parts.append(
            "\n记住，命书智慧是工具，真正改变来自你的实践与领悟。"
        )

        return "\n".join(feedback_parts)


def main():
    parser = argparse.ArgumentParser(
        description="命书 journal manager - 管理你的易命术练习记录"
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    add_parser = subparsers.add_parser("add", help="添加新记录")
    add_parser.add_argument("--situation", required=True, help="情境描述")
    add_parser.add_argument("--techniques", required=True, help="使用的技术")
    add_parser.add_argument("--effectiveness", type=int, required=True,
                           help="效果评分(1-5)")
    add_parser.add_argument("--tags", help="标签(逗号分隔)", default="")
    add_parser.add_argument("--notes", help="备注", default="")

    list_parser = subparsers.add_parser("list", help="查看记录")
    list_parser.add_argument("--limit", type=int, default=10, help="显示数量")

    stats_parser = subparsers.add_parser("stats", help="查看统计")

    streak_parser = subparsers.add_parser("streak", help="查看连续天数")

    feedback_parser = subparsers.add_parser("feedback", help="获取AI反馈")

    insights_parser = subparsers.add_parser("insights", help="查看洞察")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = JournalManager()

    if args.command == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        entry = manager.add_entry(
            situation=args.situation,
            techniques=args.techniques,
            effectiveness=args.effectiveness,
            tags=tags,
            notes=args.notes if args.notes else None
        )
        print(f"✅ 记录已添加 (ID: {entry['id']})")
        print(f"   时间: {entry['timestamp']}")
        print(f"   情境: {entry['situation']}")
        print(f"   技术: {entry['techniques']}")
        print(f"   效果: {entry['effectiveness']}/5")

    elif args.command == "list":
        entries = manager.get_entries(args.limit)
        if not entries:
            print("暂无记录")
            return
        print(f"📖 最近{len(entries)}条记录：\n")
        for entry in entries:
            dt = datetime.fromisoformat(entry["timestamp"])
            print(f"[{dt.strftime('%Y-%m-%d %H:%M')}] {entry['situation']}")
            print(f"   技术: {entry['techniques']} | 效果: {entry['effectiveness']}/5")
            if entry.get("tags"):
                print(f"   标签: {', '.join(entry['tags'])}")
            print()

    elif args.command == "stats":
        stats = manager.get_stats()
        print("📊 统计数据：\n")
        print(f"  总记录数: {stats['total_entries']}")
        print(f"  练习天数: {stats['total_days_practiced']}")
        print(f"  当前连续: {stats['current_streak']}天")
        print(f"  最佳连续: {stats['best_streak']}天")
        print(f"  平均效果: {stats['average_effectiveness']}分")

        if stats["most_used_techniques"]:
            print(f"\n  最常用技术:")
            for tech, count in stats["most_used_techniques"]:
                print(f"    - {tech}: {count}次")

        if stats["tag_distribution"]:
            print(f"\n  标签分布:")
            for tag, count in list(stats["tag_distribution"].items())[:5]:
                print(f"    - {tag}: {count}次")

    elif args.command == "streak":
        streak = manager.get_streak()
        print("🔥 连续练习统计：\n")
        print(f"  当前连续: {streak['current_streak']}天")
        print(f"  最佳连续: {streak['best_streak']}天")
        print(f"  总天数: {streak['total_days']}天")

    elif args.command == "feedback":
        feedback = manager.get_ai_feedback()
        print("💬 AI反馈：\n")
        print(feedback)

    elif args.command == "insights":
        insights = manager.generate_insights()
        print("💡 个性化洞察：\n")
        for insight in insights:
            print(f"  • {insight}")


if __name__ == "__main__":
    main()
