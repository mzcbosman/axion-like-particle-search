from pathlib import Path
import sys

REPO_ROOT = None
for candidate in Path(__file__).resolve().parents:
    if (candidate / ".git").exists():
        REPO_ROOT = candidate
        break

if REPO_ROOT is None:
    raise RuntimeError("Could not locate repository root.")

sys.path.insert(0, str(REPO_ROOT))
from common.tree_utils import TreeMaker

__all__ = ["TreeMaker"]
