import json
import os

CONFIG_PATH = os.path.expanduser("~/.clerq/config.json")

DEFAULTS = {
    "api_key": "",
    "model": "claude-sonnet-4-6",
    "watched_folders": ["~/Downloads"],
    "max_file_size_mb": 50,
    "max_content_chars": 500,
    "name_length": "medium",
    "output_language": "English",
    "preserve_original": False,
    "skip_clean_names": True,
    "watch_subfolders": False,
    "auto_start": True,
    "notifications": True,
    "notification_duration": 5,
    "show_undo_in_toast": True,
    "toast_position": "bottom_right",
    "history_retention_days": 30,
    "blacklisted_folders": [],
    "blacklisted_patterns": [],
    "blacklisted_keywords": [],
    "enabled_extensions": [".pdf", ".docx", ".xlsx", ".csv", ".txt", ".jpg", ".png"],
    "use_local_model": False,
    "ollama_model": "llama3",
}


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULTS)
        return DEFAULTS.copy()

    with open(CONFIG_PATH, "r") as f:
        saved = json.load(f)

    
    config = DEFAULTS.copy()
    config.update(saved)
    return config


def save_config(config: dict):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
