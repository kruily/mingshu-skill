#!/usr/bin/env python3
"""
Memory Sync Module for ming-shu skill.
Syncs journal data with Hermes/OpenClaw memory systems via CLI commands.

This module provides integration between ming-shu's local journal storage
and external memory systems (Hermes, OpenClaw) for cross-session memory persistence.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Import from existing modules
try:
    from .journal_manager import JournalManager
    from .memory_manager import UserMemory
except ImportError:
    # Allow standalone execution
    from journal_manager import JournalManager
    from memory_manager import UserMemory


class MemorySyncError(Exception):
    """Raised when memory sync operations fail."""
    pass


class HermesMemoryCLI:
    """Generates Hermes CLI commands for memory operations."""

    @staticmethod
    def build_store_command(key: str, value: str, profile: Optional[str] = None) -> List[str]:
        """
        Build hermes memory store command.

        Args:
            key: Memory key/identifier
            value: Memory value to store
            profile: Optional profile name

        Returns:
            Command list for subprocess
        """
        cmd = ["hermes", "memory", "store"]
        if profile:
            cmd.extend(["--profile", profile])
        cmd.extend([key, value])
        return cmd

    @staticmethod
    def build_search_command(query: str, profile: Optional[str] = None,
                            limit: int = 5) -> List[str]:
        """
        Build hermes memory search command.

        Args:
            query: Search query string
            profile: Optional profile name
            limit: Max results to return

        Returns:
            Command list for subprocess
        """
        cmd = ["hermes", "memory", "search"]
        if profile:
            cmd.extend(["--profile", profile])
        cmd.extend(["--limit", str(limit), query])
        return cmd

    @staticmethod
    def build_retrieve_command(key: str, profile: Optional[str] = None) -> List[str]:
        """
        Build hermes memory retrieve command.

        Args:
            key: Memory key to retrieve
            profile: Optional profile name

        Returns:
            Command list for subprocess
        """
        cmd = ["hermes", "memory", "retrieve"]
        if profile:
            cmd.extend(["--profile", profile])
        cmd.append(key)
        return cmd


class OpenClawMemoryCLI:
    """Generates OpenClaw CLI commands for memory operations."""

    @staticmethod
    def build_store_command(key: str, value: str, namespace: Optional[str] = None) -> List[str]:
        """
        Build openclaw memory store command.

        Args:
            key: Memory key/identifier
            value: Memory value to store
            namespace: Optional namespace

        Returns:
            Command list for subprocess
        """
        cmd = ["openclaw", "memory", "set"]
        if namespace:
            cmd.extend(["--namespace", namespace])
        cmd.extend([key, value])
        return cmd

    @staticmethod
    def build_search_command(query: str, namespace: Optional[str] = None,
                            limit: int = 5) -> List[str]:
        """
        Build openclaw memory search command.

        Args:
            query: Search query string
            namespace: Optional namespace
            limit: Max results to return

        Returns:
            Command list for subprocess
        """
        cmd = ["openclaw", "memory", "search"]
        if namespace:
            cmd.extend(["--namespace", namespace])
        cmd.extend(["--limit", str(limit), "--", query])
        return cmd

    @staticmethod
    def build_retrieve_command(key: str, namespace: Optional[str] = None) -> List[str]:
        """
        Build openclaw memory retrieve command.

        Args:
            key: Memory key to retrieve
            namespace: Optional namespace

        Returns:
            Command list for subprocess
        """
        cmd = ["openclaw", "memory", "get"]
        if namespace:
            cmd.extend(["--namespace", namespace])
        cmd.append(key)
        return cmd


class MemorySync:
    """
    Synchronizes ming-shu journal data with Hermes/OpenClaw memory systems.

    Provides graceful degradation - if memory system is unavailable,
    operations fail silently and return appropriate defaults.
    """

    def __init__(self, profile: Optional[str] = None, namespace: Optional[str] = None):
        """
        Initialize MemorySync.

        Args:
            profile: Hermes profile name (optional)
            namespace: OpenClaw namespace (optional)
        """
        self.profile = profile
        self.namespace = namespace
        self.journal_mgr = JournalManager()
        self.local_memory = UserMemory()
        self.hermes = HermesMemoryCLI()
        self.openclaw = OpenClawMemoryCLI()
        self._hermes_available = self._check_hermes()
        self._openclaw_available = self._check_openclaw()

    def _check_hermes(self) -> bool:
        """Check if hermes CLI is available."""
        try:
            result = subprocess.run(
                ["hermes", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _check_openclaw(self) -> bool:
        """Check if openclaw CLI is available."""
        try:
            result = subprocess.run(
                ["openclaw", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _execute_cli(self, cmd: List[str]) -> tuple[bool, str]:
        """
        Execute a CLI command and return success status and output.

        Args:
            cmd: Command list to execute

        Returns:
            Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return (result.returncode == 0, result.stdout + result.stderr)
        except subprocess.SubprocessError as e:
            return (False, str(e))

    def _serialize_journal_entry(self, entry: dict) -> str:
        """Serialize journal entry for memory storage."""
        return json.dumps(entry, ensure_ascii=False)

    def _deserialize_journal_entry(self, data: str) -> dict:
        """Deserialize journal entry from memory storage."""
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {}

    # === Hermes Integration ===

    def sync_to_hermes(self, user_id: str) -> Dict[str, Any]:
        """
        Sync all journal data for a user to Hermes memory.

        Args:
            user_id: User identifier

        Returns:
            Sync result with status and details
        """
        if not self._hermes_available:
            return {
                "success": False,
                "error": "Hermes CLI not available",
                "synced_count": 0
            }

        result = {
            "success": True,
            "synced_count": 0,
            "errors": []
        }

        # Sync journal entries
        entries = self.journal_mgr.get_entries(user_id, limit=0)
        for entry in entries:
            key = f"ming-shu:journal:{user_id}:{entry['id']}"
            value = self._serialize_journal_entry(entry)
            cmd = self.hermes.build_store_command(key, value, self.profile)
            success, output = self._execute_cli(cmd)
            if success:
                result["synced_count"] += 1
            else:
                result["errors"].append(output)

        # Sync stats
        stats = self.journal_mgr.get_stats(user_id)
        key = f"ming-shu:stats:{user_id}"
        value = json.dumps(stats, ensure_ascii=False)
        cmd = self.hermes.build_store_command(key, value, self.profile)
        success, output = self._execute_cli(cmd)
        if not success:
            result["errors"].append(f"Stats sync failed: {output}")

        # Sync insights
        insights = self.journal_mgr.generate_insights(user_id)
        if insights:
            key = f"ming-shu:insights:{user_id}"
            value = json.dumps(insights, ensure_ascii=False)
            cmd = self.hermes.build_store_command(key, value, self.profile)
            success, output = self._execute_cli(cmd)
            if not success:
                result["errors"].append(f"Insights sync failed: {output}")

        return result

    def load_from_hermes(self, user_id: str) -> Dict[str, Any]:
        """
        Load journal data for a user from Hermes memory.

        Args:
            user_id: User identifier

        Returns:
            Dictionary with journal entries, stats, and insights
        """
        if not self._hermes_available:
            return {
                "success": False,
                "error": "Hermes CLI not available",
                "entries": [],
                "stats": {},
                "insights": []
            }

        result = {
            "success": True,
            "entries": [],
            "stats": {},
            "insights": []
        }

        # Load stats
        key = f"ming-shu:stats:{user_id}"
        cmd = self.hermes.build_retrieve_command(key, self.profile)
        success, output = self._execute_cli(cmd)
        if success and output.strip():
            try:
                result["stats"] = json.loads(output.strip())
            except json.JSONDecodeError:
                pass

        # Load insights
        key = f"ming-shu:insights:{user_id}"
        cmd = self.hermes.build_retrieve_command(key, self.profile)
        success, output = self._execute_cli(cmd)
        if success and output.strip():
            try:
                result["insights"] = json.loads(output.strip())
            except json.JSONDecodeError:
                pass

        return result

    def search_hermes(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search Hermes memory for past insights.

        Args:
            query: Search query
            limit: Max results

        Returns:
            Search results
        """
        if not self._hermes_available:
            return {
                "success": False,
                "error": "Hermes CLI not available",
                "results": []
            }

        cmd = self.hermes.build_search_command(query, self.profile, limit)
        success, output = self._execute_cli(cmd)

        return {
            "success": success,
            "results": output.strip().split("\n") if success else [],
            "raw_output": output if not success else None
        }

    # === OpenClaw Integration ===

    def sync_to_openclaw(self, user_id: str) -> Dict[str, Any]:
        """
        Sync all journal data for a user to OpenClaw memory.

        Args:
            user_id: User identifier

        Returns:
            Sync result with status and details
        """
        if not self._openclaw_available:
            return {
                "success": False,
                "error": "OpenClaw CLI not available",
                "synced_count": 0
            }

        result = {
            "success": True,
            "synced_count": 0,
            "errors": []
        }

        # Sync journal entries
        entries = self.journal_mgr.get_entries(user_id, limit=0)
        for entry in entries:
            key = f"ming-shu:journal:{user_id}:{entry['id']}"
            value = self._serialize_journal_entry(entry)
            cmd = self.openclaw.build_store_command(key, value, self.namespace)
            success, output = self._execute_cli(cmd)
            if success:
                result["synced_count"] += 1
            else:
                result["errors"].append(output)

        # Sync stats
        stats = self.journal_mgr.get_stats(user_id)
        key = f"ming-shu:stats:{user_id}"
        value = json.dumps(stats, ensure_ascii=False)
        cmd = self.openclaw.build_store_command(key, value, self.namespace)
        success, output = self._execute_cli(cmd)
        if not success:
            result["errors"].append(f"Stats sync failed: {output}")

        # Sync insights
        insights = self.journal_mgr.generate_insights(user_id)
        if insights:
            key = f"ming-shu:insights:{user_id}"
            value = json.dumps(insights, ensure_ascii=False)
            cmd = self.openclaw.build_store_command(key, value, self.namespace)
            success, output = self._execute_cli(cmd)
            if not success:
                result["errors"].append(f"Insights sync failed: {output}")

        return result

    def load_from_openclaw(self, user_id: str) -> Dict[str, Any]:
        """
        Load journal data for a user from OpenClaw memory.

        Args:
            user_id: User identifier

        Returns:
            Dictionary with journal entries, stats, and insights
        """
        if not self._openclaw_available:
            return {
                "success": False,
                "error": "OpenClaw CLI not available",
                "entries": [],
                "stats": {},
                "insights": []
            }

        result = {
            "success": True,
            "entries": [],
            "stats": {},
            "insights": []
        }

        # Load stats
        key = f"ming-shu:stats:{user_id}"
        cmd = self.openclaw.build_retrieve_command(key, self.namespace)
        success, output = self._execute_cli(cmd)
        if success and output.strip():
            try:
                result["stats"] = json.loads(output.strip())
            except json.JSONDecodeError:
                pass

        # Load insights
        key = f"ming-shu:insights:{user_id}"
        cmd = self.openclaw.build_retrieve_command(key, self.namespace)
        success, output = self._execute_cli(cmd)
        if success and output.strip():
            try:
                result["insights"] = json.loads(output.strip())
            except json.JSONDecodeError:
                pass

        return result

    def search_openclaw(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search OpenClaw memory for past insights.

        Args:
            query: Search query
            limit: Max results

        Returns:
            Search results
        """
        if not self._openclaw_available:
            return {
                "success": False,
                "error": "OpenClaw CLI not available",
                "results": []
            }

        cmd = self.openclaw.build_search_command(query, self.namespace, limit)
        success, output = self._execute_cli(cmd)

        return {
            "success": success,
            "results": output.strip().split("\n") if success else [],
            "raw_output": output if not success else None
        }

    # === Unified Interface ===

    def sync_all(self, user_id: str) -> Dict[str, Any]:
        """
        Sync journal data to both available memory systems.

        Args:
            user_id: User identifier

        Returns:
            Combined sync results
        """
        results = {
            "hermes": None,
            "openclaw": None,
            "local": "ok"
        }

        if self._hermes_available:
            results["hermes"] = self.sync_to_hermes(user_id)

        if self._openclaw_available:
            results["openclaw"] = self.sync_to_openclaw(user_id)

        return results

    def search_all(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search all available memory systems.

        Args:
            query: Search query
            limit: Max results per system

        Returns:
            Combined search results
        """
        results = {
            "query": query,
            "hermes": None,
            "openclaw": None
        }

        if self._hermes_available:
            results["hermes"] = self.search_hermes(query, limit)

        if self._openclaw_available:
            results["openclaw"] = self.search_openclaw(query, limit)

        return results

    def get_status(self) -> Dict[str, Any]:
        """
        Get status of memory sync system.

        Returns:
            Status information for all memory systems
        """
        return {
            "hermes_available": self._hermes_available,
            "openclaw_available": self._openclaw_available,
            "profile": self.profile,
            "namespace": self.namespace
        }


def main():
    """CLI interface for memory sync."""
    import argparse

    parser = argparse.ArgumentParser(
        description="命书 memory sync - 同步命书数据到Hermes/OpenClaw记忆系统"
    )
    parser.add_argument("--profile", help="Hermes profile name")
    parser.add_argument("--namespace", help="OpenClaw namespace")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # Status command
    subparsers.add_parser("status", help="查看记忆系统状态")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="同步数据到记忆系统")
    sync_parser.add_argument("--user", required=True, help="用户ID")

    # Search command
    search_parser = subparsers.add_parser("search", help="搜索记忆")
    search_parser.add_argument("--query", required=True, help="搜索查询")
    search_parser.add_argument("--limit", type=int, default=5, help="结果数量限制")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    sync = MemorySync(profile=args.profile, namespace=args.namespace)

    if args.command == "status":
        status = sync.get_status()
        print("📊 记忆系统状态：\n")
        print(f"  Hermes:  {'✅ 可用' if status['hermes_available'] else '❌ 不可用'}")
        print(f"  OpenClaw: {'✅ 可用' if status['openclaw_available'] else '❌ 不可用'}")
        if status['profile']:
            print(f"  Profile: {status['profile']}")
        if status['namespace']:
            print(f"  Namespace: {status['namespace']}")

    elif args.command == "sync":
        results = sync.sync_all(args.user)
        print("🔄 同步结果：\n")

        if results["hermes"]:
            h = results["hermes"]
            if h["success"]:
                print(f"  Hermes: ✅ 同步成功 ({h.get('synced_count', 0)} 条记录)")
            else:
                print(f"  Hermes: ❌ {h.get('error', '同步失败')}")

        if results["openclaw"]:
            o = results["openclaw"]
            if o["success"]:
                print(f"  OpenClaw: ✅ 同步成功 ({o.get('synced_count', 0)} 条记录)")
            else:
                print(f"  OpenClaw: ❌ {o.get('error', '同步失败')}")

        if not results["hermes"] and not results["openclaw"]:
            print("  ❌ 没有可用的记忆系统")
            sys.exit(1)

    elif args.command == "search":
        results = sync.search_all(args.query, args.limit)
        print(f"🔍 搜索结果 for '{args.query}':\n")

        if results["hermes"] and results["hermes"]["success"]:
            print("  Hermes 结果:")
            for r in results["hermes"]["results"]:
                print(f"    - {r}")
        elif results["hermes"]:
            print(f"  Hermes: ❌ {results['hermes'].get('error', '搜索失败')}")

        if results["openclaw"] and results["openclaw"]["success"]:
            print("\n  OpenClaw 结果:")
            for r in results["openclaw"]["results"]:
                print(f"    - {r}")
        elif results["openclaw"]:
            print(f"\n  OpenClaw: ❌ {results['openclaw'].get('error', '搜索失败')}")

        if not results["hermes"] and not results["openclaw"]:
            print("  ❌ 没有可用的记忆系统")
            sys.exit(1)


if __name__ == "__main__":
    main()