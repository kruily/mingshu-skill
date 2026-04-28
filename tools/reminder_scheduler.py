#!/usr/bin/env python3
"""
Reminder Scheduler for Ming Shu - Schedules morning and evening reminders.
Generates commands for Hermes/OpenClaw platforms (no actual cron jobs).
Stores schedule data in ~/.ming-shu/schedules/{user_id}.json
"""

import json
import argparse
from datetime import datetime, time
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


import sys
sys.path.insert(0, str(Path(__file__).parent))
try:
    from journal_manager import JournalManager
except ImportError:
    JournalManager = None

DEFAULT_TIMEZONE = "Asia/Shanghai"
MORNING_HOUR, MORNING_MINUTE = 7, 0
EVENING_HOUR, EVENING_MINUTE = 21, 0

SCHEDULE_DIR = Path.home() / ".ming-shu" / "schedules"


class ReminderScheduler:

    def __init__(
        self,
        schedule_dir: Optional[Path] = None,
        timezone: Optional[str] = None
    ):
        self.schedule_dir = Path(schedule_dir) if schedule_dir else SCHEDULE_DIR
        self.schedule_dir.mkdir(parents=True, exist_ok=True)
        self.timezone = ZoneInfo(timezone) if timezone else ZoneInfo(DEFAULT_TIMEZONE)
        self.journal_manager = JournalManager() if JournalManager else None

    def _get_schedule_path(self, user_id: str) -> Path:
        return self.schedule_dir / f"{user_id}.json"

    def _load_schedule(self, user_id: str) -> dict:
        path = self._get_schedule_path(user_id)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "user_id": user_id,
            "morning": None,
            "evening": None,
            "platform": "hermes",
            "created_at": datetime.now(self.timezone).isoformat()
        }

    def _save_schedule(self, user_id: str, data: dict) -> None:
        path = self._get_schedule_path(user_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _format_time(self, hour: int, minute: int) -> str:
        return f"{hour:02d}:{minute:02d}"

    def _parse_time(self, time_str: str) -> tuple:
        """Parse HH:MM format to (hour, minute)"""
        parts = time_str.split(":")
        return int(parts[0]), int(parts[1])

    def _generate_hermes_command(
        self,
        user_id: str,
        reminder_type: str,
        hour: int,
        minute: int,
        dry_run: bool = False
    ) -> str:
        """Generate Hermes scheduler command"""
        time_str = self._format_time(hour, minute)
        base_cmd = (
            f"hermes schedule add --user {user_id} "
            f"--type {reminder_type} "
            f"--time {time_str} "
            f"--timezone {self.timezone.key}"
        )
        if dry_run:
            base_cmd += " --dry-run"
        return base_cmd

    def _generate_openclaw_command(
        self,
        user_id: str,
        reminder_type: str,
        hour: int,
        minute: int,
        dry_run: bool = False
    ) -> str:
        """Generate OpenClaw scheduler command"""
        time_str = self._format_time(hour, minute)
        base_cmd = (
            f"openclaw reminder create "
            f"--user {user_id} "
            f"--reminder-type {reminder_type} "
            f"--at {time_str} "
            f"--timezone {self.timezone.key}"
        )
        if dry_run:
            base_cmd += " --dry-run"
        return base_cmd

    def schedule_reminder(
        self,
        user_id: str,
        reminder_type: str,
        hour: int,
        minute: int,
        platform: str = "hermes",
        dry_run: bool = False
    ) -> dict:
        """
        Schedule a reminder (generates command, doesn't create actual cron job).
        reminder_type: 'morning' or 'evening'
        """
        if reminder_type not in ("morning", "evening"):
            raise ValueError("reminder_type must be 'morning' or 'evening'")

        if platform == "openclaw":
            command = self._generate_openclaw_command(
                user_id, reminder_type, hour, minute, dry_run
            )
        else:
            command = self._generate_hermes_command(
                user_id, reminder_type, hour, minute, dry_run
            )

        if dry_run:
            return {
                "dry_run": True,
                "command": command,
                "user_id": user_id,
                "reminder_type": reminder_type,
                "time": self._format_time(hour, minute),
                "timezone": self.timezone.key
            }


        data = self._load_schedule(user_id)
        data["platform"] = platform
        schedule_key = reminder_type
        data[schedule_key] = {
            "hour": hour,
            "minute": minute,
            "timezone": self.timezone.key,
            "enabled": True,
            "updated_at": datetime.now(self.timezone).isoformat()
        }
        self._save_schedule(user_id, data)

        return {
            "scheduled": True,
            "command": command,
            "user_id": user_id,
            "reminder_type": reminder_type,
            "time": self._format_time(hour, minute),
            "timezone": self.timezone.key
        }

    def list_schedules(self, user_id: str) -> dict:
        """List all scheduled reminders for a user"""
        data = self._load_schedule(user_id)

        result = {
            "user_id": user_id,
            "platform": data.get("platform", "hermes"),
            "morning": None,
            "evening": None
        }

        if data.get("morning"):
            m = data["morning"]
            result["morning"] = {
                "time": self._format_time(m["hour"], m["minute"]),
                "timezone": m.get("timezone", DEFAULT_TIMEZONE),
                "enabled": m.get("enabled", True)
            }

        if data.get("evening"):
            e = data["evening"]
            result["evening"] = {
                "time": self._format_time(e["hour"], e["minute"]),
                "timezone": e.get("timezone", DEFAULT_TIMEZONE),
                "enabled": e.get("enabled", True)
            }

        return result

    def remove_reminder(
        self,
        user_id: str,
        reminder_type: str,
        platform: str = "hermes",
        dry_run: bool = False
    ) -> dict:
        """Remove a scheduled reminder"""
        if reminder_type not in ("morning", "evening"):
            raise ValueError("reminder_type must be 'morning' or 'evening'")

        if platform == "openclaw":
            command = f"openclaw reminder delete --user {user_id} --reminder-type {reminder_type}"
        else:
            command = f"hermes schedule remove --user {user_id} --type {reminder_type}"

        if dry_run:
            return {
                "dry_run": True,
                "command": command,
                "user_id": user_id,
                "reminder_type": reminder_type
            }

        data = self._load_schedule(user_id)
        if data.get(reminder_type):
            data[reminder_type] = None
            self._save_schedule(user_id, data)

        return {
            "removed": True,
            "command": command,
            "user_id": user_id,
            "reminder_type": reminder_type
        }

    def send_now(
        self,
        user_id: str,
        reminder_type: str = "morning",
        dry_run: bool = False
    ) -> dict:
        """Send a reminder immediately (for testing)"""
        if reminder_type not in ("morning", "evening"):
            raise ValueError("reminder_type must be 'morning' or 'evening'")

        streak_data = {"current_streak": 0, "best_streak": 0}
        if self.journal_manager:
            try:
                streak_data = self.journal_manager.get_streak(user_id)
            except Exception:
                pass

        template_key = "晨间提醒" if reminder_type == "morning" else "晚间提醒"
        now = datetime.now(self.timezone)

        content = self._generate_reminder_content(
            reminder_type, user_id, streak_data, now
        )

        if dry_run:
            return {
                "dry_run": True,
                "content": content,
                "user_id": user_id,
                "reminder_type": reminder_type,
                "generated_at": now.isoformat()
            }


        return {
            "sent": True,
            "content": content,
            "user_id": user_id,
            "reminder_type": reminder_type,
            "sent_at": now.isoformat()
        }

    def _generate_reminder_content(
        self,
        reminder_type: str,
        user_id: str,
        streak_data: dict,
        dt: datetime
    ) -> str:
        """Generate reminder content based on template"""
        streak = streak_data.get("current_streak", 0)
        best_streak = streak_data.get("best_streak", 0)

        if reminder_type == "morning":
            streak_indicator = "🔥" if streak >= 7 else "✨" if streak >= 3 else ""

            streak_msg = f"你已经连续修行 {streak} 天了 {streak_indicator}"
            if streak == 1:
                motivation = "新的一天，新的开始"
            elif streak <= 3:
                motivation = "习惯在萌芽，继续浇水"
            elif streak <= 6:
                motivation = "你已经走了一段路，继续"
            elif streak <= 14:
                motivation = "一周的修行，力量在累积"
            elif streak <= 29:
                motivation = "内在的变化在悄然发生"
            else:
                motivation = "修行已成为你的一部分"

            return (
                f"☀️ 早安，{user_id}\n\n"
                f"今天是 {dt.strftime('%Y-%m-%d')}。\n"
                f"{streak_msg}\n\n"
                f"最佳记录：{best_streak} 天\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"今日推荐修行：\n\n"
                f"【第X术 · 顺势而为】\n\n"
                f"（使用 /ming-shu 获取今日技术）\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"今日提示：\n\n"
                f'"{motivation}"\n\n'
                f"有什么想在今天特别留意的吗？"
            )
        else:
            if streak <= 2:
                ending = "每一天都是新的开始，明天见"
            elif streak <= 6:
                ending = "坚持的你在发光，明天见"
            elif streak <= 13:
                ending = "修行路上，你不孤独，明天见"
            elif streak <= 29:
                ending = "内在的力量在增长，明天见"
            else:
                ending = "修行已成为你的习惯，明天继续"

            return (
                f"🌙 晚安，{user_id}\n\n"
                f"今天 {dt.strftime('%Y-%m-%d')} 的修行记录，等你来整理。\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 今日数据回顾：\n\n"
                f"| 指标 | 数值 |\n"
                f"|------|------|\n"
                f"| 连续修行 | {streak} 天 |\n"
                f"| 今日评分 | /5 |\n"
                f"| 今日心情 | — |\n"
                f"| 应用技术 | — |\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"💭 今日反思问题：\n\n"
                f"1. 今天最让你感到挑战的是什么？\n\n"
                f"2. 命书智慧如何帮助你应对？\n\n"
                f"3. 明天你想要什么不同的结果？\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"✨ 今日亮点：\n\n"
                f"（使用 journal_manager 记录今日修行）\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🌅 明日预告：\n\n"
                f"明日推荐技术：【第X术 · 待时而动】\n\n"
                f"（使用 /ming-shu 获取明日技术）\n\n"
                f"{ending}"
            )


def main():
    parser = argparse.ArgumentParser(
        description="命书 reminder scheduler - 管理晨间和晚间提醒"
    )
    parser.add_argument(
        "--platform",
        choices=["hermes", "openclaw"],
        default="hermes",
        help="目标平台 (default: hermes)"
    )
    parser.add_argument(
        "--timezone",
        default=DEFAULT_TIMEZONE,
        help=f"时区 (default: {DEFAULT_TIMEZONE})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅生成命令，不实际执行"
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")


    schedule_parser = subparsers.add_parser(
        "schedule",
        help="设置提醒"
    )
    schedule_parser.add_argument(
        "--user", required=True, help="用户ID"
    )
    schedule_parser.add_argument(
        "--type",
        required=True,
        choices=["morning", "evening"],
        help="提醒类型"
    )
    schedule_parser.add_argument(
        "--time",
        default=None,
        help="时间 (HH:MM格式, 晨间默认07:00, 晚间默认21:00)"
    )


    list_parser = subparsers.add_parser(
        "list",
        help="查看已设置的提醒"
    )
    list_parser.add_argument(
        "--user", required=True, help="用户ID"
    )


    remove_parser = subparsers.add_parser(
        "remove",
        help="移除提醒"
    )
    remove_parser.add_argument(
        "--user", required=True, help="用户ID"
    )
    remove_parser.add_argument(
        "--type",
        required=True,
        choices=["morning", "evening"],
        help="提醒类型"
    )


    send_parser = subparsers.add_parser(
        "send-now",
        help="立即发送提醒 (用于测试)"
    )
    send_parser.add_argument(
        "--user", required=True, help="用户ID"
    )
    send_parser.add_argument(
        "--type",
        choices=["morning", "evening"],
        default="morning",
        help="提醒类型 (default: morning)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    scheduler = ReminderScheduler(timezone=args.timezone)
    platform = args.platform
    dry_run = args.dry_run

    if args.command == "schedule":
        reminder_type = args.type
        hour, minute = None, None

        if args.time:
            hour, minute = scheduler._parse_time(args.time)
        elif reminder_type == "morning":
            hour, minute = MORNING_HOUR, MORNING_MINUTE
        else:
            hour, minute = EVENING_HOUR, EVENING_MINUTE

        result = scheduler.schedule_reminder(
            user_id=args.user,
            reminder_type=reminder_type,
            hour=hour,
            minute=minute,
            platform=platform,
            dry_run=dry_run
        )

        if dry_run:
            print(f"🔎 [Dry Run] 生成的命令：")
            print(f"   {result['command']}")
        else:
            print(f"✅ 已设置 {reminder_type} 提醒")
            print(f"   时间: {result['time']}")
            print(f"   时区: {result['timezone']}")
            print(f"   平台: {platform}")
            print(f"\n📋 执行以下命令启用：")
            print(f"   {result['command']}")

    elif args.command == "list":
        schedules = scheduler.list_schedules(args.user)

        print(f"📅 提醒列表 - 用户: {args.user}")
        print(f"   平台: {schedules['platform']}\n")

        if schedules.get("morning"):
            m = schedules["morning"]
            status = "✓" if m["enabled"] else "✗"
            print(f"   🌅 晨间提醒: {m['time']} ({m['timezone']}) {status}")
        else:
            print("   🌅 晨间提醒: 未设置")

        if schedules.get("evening"):
            e = schedules["evening"]
            status = "✓" if e["enabled"] else "✗"
            print(f"   🌙 晚间提醒: {e['time']} ({e['timezone']}) {status}")
        else:
            print("   🌙 晚间提醒: 未设置")

    elif args.command == "remove":
        result = scheduler.remove_reminder(
            user_id=args.user,
            reminder_type=args.type,
            platform=platform,
            dry_run=dry_run
        )

        if dry_run:
            print(f"🔎 [Dry Run] 生成的命令：")
            print(f"   {result['command']}")
        else:
            print(f"✅ 已移除 {args.type} 提醒")
            print(f"\n📋 执行以下命令删除：")
            print(f"   {result['command']}")

    elif args.command == "send-now":
        result = scheduler.send_now(
            user_id=args.user,
            reminder_type=args.type,
            dry_run=dry_run
        )

        print(f"📤 {'[Dry Run] ' if dry_run else ''}{args.type} 提醒内容：\n")
        print(result.get("content", result.get("content", "")))

        if not dry_run:
            print(f"\n✅ 已发送 (实际发送需配置平台API)")


if __name__ == "__main__":
    main()
