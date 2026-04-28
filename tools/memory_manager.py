#!/usr/bin/env python3
"""
Memory Manager for ming-shu skill.
Handles user memory storage for conversation history and bookmarked techniques.
Data stored in local JSON files - one per user.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class UserMemory:
    """Handles read/write operations for user memory storage."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize UserMemory with data directory.

        Args:
            data_dir: Directory for storing memory files.
                     Defaults to ~/.ming-shu-memory/ or ./memory/ for portability.
        """
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            # Try ~/.ming-shu-memory/ first, fall back to ./memory/
            home_dir = Path.home()
            default_dir = home_dir / ".ming-shu-memory"
            if home_dir.exists() and os.access(home_dir, os.W_OK):
                self.data_dir = default_dir
            else:
                self.data_dir = Path("./memory/")

        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_user_file(self, user_id: str) -> Path:
        """Get the file path for a user's data."""
        # Sanitize user_id to prevent path traversal
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
            raise ValueError(f"Invalid user_id: {user_id}")
        return self.data_dir / f"{user_id}.json"

    def _load_user_data(self, user_id: str) -> dict:
        """Load user data from JSON file, returns empty structure if not found."""
        user_file = self._get_user_file(user_id)
        if user_file.exists():
            with open(user_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "conversations": [],
            "bookmarks": []
        }

    def _save_user_data(self, user_id: str, data: dict) -> None:
        """Save user data to JSON file."""
        data["updated_at"] = datetime.utcnow().isoformat()
        user_file = self._get_user_file(user_id)
        with open(user_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_conversation(self, user_id: str, difficulty: str,
                          matched_techniques: list, bookmarked: bool = False) -> dict:
        """
        Save a conversation entry for a user.

        Args:
            user_id: Unique user identifier.
            difficulty: Difficulty level of the conversation.
            matched_techniques: List of technique IDs matched.
            bookmarked: Whether this conversation is bookmarked.

        Returns:
            The saved conversation entry.
        """
        data = self._load_user_data(user_id)

        conversation_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "difficulty": difficulty,
            "matched_techniques": matched_techniques,
            "bookmarked": bookmarked
        }

        data["conversations"].append(conversation_entry)
        self._save_user_data(user_id, data)

        return conversation_entry

    def load_conversation(self, user_id: str) -> dict:
        """
        Load all conversation data for a user.

        Args:
            user_id: Unique user identifier.

        Returns:
            User data dict with conversations and bookmarks.
        """
        return self._load_user_data(user_id)

    def add_bookmark(self, user_id: str, technique_id: str, note: str = "") -> dict:
        """
        Add a bookmark for a technique.

        Args:
            user_id: Unique user identifier.
            technique_id: ID of the technique to bookmark.
            note: Optional note about the bookmark.

        Returns:
            The saved bookmark entry.
        """
        data = self._load_user_data(user_id)

        # Check if technique already bookmarked
        for bookmark in data["bookmarks"]:
            if bookmark["technique_id"] == technique_id:
                bookmark["note"] = note
                self._save_user_data(user_id, data)
                return bookmark

        bookmark_entry = {
            "technique_id": technique_id,
            "bookmarked_at": datetime.utcnow().isoformat(),
            "note": note
        }

        data["bookmarks"].append(bookmark_entry)
        self._save_user_data(user_id, data)

        return bookmark_entry

    def get_bookmarks(self, user_id: str) -> list:
        """
        Get all bookmarks for a user.

        Args:
            user_id: Unique user identifier.

        Returns:
            List of bookmark entries.
        """
        data = self._load_user_data(user_id)
        return data.get("bookmarks", [])

    def list_users(self) -> list:
        """
        List all users with memory files.

        Returns:
            List of user IDs.
        """
        users = []
        if self.data_dir.exists():
            for file in self.data_dir.iterdir():
                if file.suffix == ".json" and file.is_file():
                    users.append(file.stem)
        return sorted(users)


def main():
    """CLI interface for memory manager."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 memory_manager.py write <user_id> <json_data>")
        print("  python3 memory_manager.py read <user_id>")
        print("  python3 memory_manager.py bookmark <user_id> <technique_id> [note]")
        print("  python3 memory_manager.py list")
        sys.exit(1)

    memory = UserMemory()
    command = sys.argv[1]

    if command == "list":
        users = memory.list_users()
        if users:
            print("Users:", ", ".join(users))
        else:
            print("No users found.")
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Error: Missing required arguments")
        sys.exit(1)

    user_id = sys.argv[2]

    if command == "write":
        if len(sys.argv) < 4:
            print("Error: Missing JSON data")
            sys.exit(1)
        try:
            json_data = json.loads(sys.argv[3])
            difficulty = json_data.get("difficulty", "unknown")
            matched_techniques = json_data.get("matched_techniques", [])
            bookmarked = json_data.get("bookmarked", False)
            result = memory.save_conversation(user_id, difficulty, matched_techniques, bookmarked)
            print(f"Conversation saved: {result}")
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON - {e}")
            sys.exit(1)

    elif command == "read":
        data = memory.load_conversation(user_id)
        print(json.dumps(data, indent=2, ensure_ascii=False))

    elif command == "bookmark":
        if len(sys.argv) < 4:
            print("Error: Missing technique_id")
            sys.exit(1)
        technique_id = sys.argv[3]
        note = sys.argv[4] if len(sys.argv) > 4 else ""
        result = memory.add_bookmark(user_id, technique_id, note)
        print(f"Bookmark added: {result}")

    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
