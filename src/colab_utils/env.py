import os
from typing import List


def check_required_env_vars(required_vars: List[str]) -> None:
    for var in required_vars:
        if os.getenv(var) is None:
            raise ValueError(f"Missing required environment variable: {var}")