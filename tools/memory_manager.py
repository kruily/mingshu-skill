#!/usr/bin/env python3
"""
Memory Manager for ming-shu skill.
Handles memory storage for conversation history and bookmarked techniques.
Data stored in {skill_dir}/data/memory.json (single-user, skill directory based)
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class UserMemory:
    """Handles read/write operations for memory storage (single-user)."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize UserMemory with data directory.

        Args:
            data_dir: Directory for storing memory files.
                     Defaults to {skill_dir}/data/
        """
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            # Use skill directory based storage
            skill_dir = Path(__file__).parent.parent
            self.data_dir = skill_dir / "data"

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "memory.jsonl"

    def _load_all_records(self) -> list:
        records = []
        if self.data_file.exists():
            with open(self.data_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
        return records

    def _load_data(self) -> dict:
        records = self._load_all_records()
        conversations = [r for r in records if r.get("type") == "conversation"]
        bookmarks = [r for r in records if r.get("type") == "bookmark"]
        return {
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "conversations": conversations,
            "bookmarks": bookmarks
        }

    def _save_data(self, data: dict) -> None:
        pass

    def save_conversation(self, difficulty: str,
                          matched_techniques: list, bookmarked: bool = False) -> dict:
        conversation_entry = {
            "type": "conversation",
            "timestamp": datetime.utcnow().isoformat(),
            "difficulty": difficulty,
            "matched_techniques": matched_techniques,
            "bookmarked": bookmarked
        }

        with open(self.data_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(conversation_entry, ensure_ascii=False) + "\n")

        return conversation_entry

    def load_conversation(self) -> dict:
        """
        Load all conversation data.

        Returns:
            Data dict with conversations and bookmarks.
        """
        return self._load_data()

    def add_bookmark(self, technique_id: str, note: str = "") -> dict:
        bookmark_entry = {
            "type": "bookmark",
            "technique_id": technique_id,
            "bookmarked_at": datetime.utcnow().isoformat(),
            "note": note
        }

        with open(self.data_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(bookmark_entry, ensure_ascii=False) + "\n")

        return bookmark_entry

    def get_bookmarks(self) -> list:
        """
        Get all bookmarks.

        Returns:
            List of bookmark entries.
        """
        data = self._load_data()
        return data.get("bookmarks", [])


def main():
    """CLI interface for memory manager (single-user)."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 memory_manager.py write <json_data>")
        print("  python3 memory_manager.py read")
        print("  python3 memory_manager.py bookmark <technique_id> [note]")
        print("  python3 memory_manager.py bookmarks")
        sys.exit(1)

    memory = UserMemory()
    command = sys.argv[1]

    if command == "write":
        if len(sys.argv) < 3:
            print("Error: Missing JSON data")
            sys.exit(1)
        try:
            json_data = json.loads(sys.argv[2])
            difficulty = json_data.get("difficulty", "unknown")
            matched_techniques = json_data.get("matched_techniques", [])
            bookmarked = json_data.get("bookmarked", False)
            result = memory.save_conversation(difficulty, matched_techniques, bookmarked)
            print(f"Conversation saved: {result}")
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON - {e}")
            sys.exit(1)

    elif command == "read":
        data = memory.load_conversation()
        print(json.dumps(data, indent=2, ensure_ascii=False))

    elif command == "bookmark":
        if len(sys.argv) < 3:
            print("Error: Missing technique_id")
            sys.exit(1)
        technique_id = sys.argv[2]
        note = sys.argv[3] if len(sys.argv) > 3 else ""
        result = memory.add_bookmark(technique_id, note)
        print(f"Bookmark added: {result}")

    elif command == "bookmarks":
        bookmarks = memory.get_bookmarks()
        print(json.dumps(bookmarks, indent=2, ensure_ascii=False))

    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
