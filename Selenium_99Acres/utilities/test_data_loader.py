from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from typing import Any

from config.settings import ROOT_DIR


DEFAULT_TEST_DATA_PATH = ROOT_DIR / "test_data" / "test_data.json"


class TestDataLoader:
    @staticmethod
    def load(path: str | Path | None = None) -> dict[str, Any]:
        data_path = Path(path) if path else DEFAULT_TEST_DATA_PATH
        if not data_path.is_absolute():
            data_path = ROOT_DIR / data_path

        if not data_path.exists():
            raise FileNotFoundError(f"Test data file was not found: {data_path}")

        with data_path.open(encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError(f"Test data file must contain a JSON object: {data_path}")

        return TestDataLoader._with_secret_overrides(data)

    @staticmethod
    def _with_secret_overrides(data: dict[str, Any]) -> dict[str, Any]:
        merged_data = copy.deepcopy(data)
        login_data = merged_data.setdefault("login", {})

        username = os.getenv("ACRES_USERNAME")
        password = os.getenv("ACRES_PASSWORD")
        if username:
            login_data["username"] = username
            login_data["mobile_number"] = username
        if password:
            login_data["password"] = password

        return merged_data
