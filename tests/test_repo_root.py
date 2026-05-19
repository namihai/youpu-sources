from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.support import create_repo_skeleton
from youpu.infra.repo_root import find_repo_root
from youpu.infra.repo_root import is_repo_root
from youpu.infra.repo_root import resolve_repo_root


class RepoRootTests(unittest.TestCase):
    def test_is_repo_root_requires_expected_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertFalse(is_repo_root(root))
            create_repo_skeleton(root)
            self.assertTrue(is_repo_root(root))

    def test_find_repo_root_walks_up_from_nested_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            nested = repo_root / "staging" / "nested"
            nested.mkdir(parents=True, exist_ok=True)

            detected = find_repo_root(nested)

        self.assertEqual(detected.resolve(), repo_root.resolve())

    def test_resolve_repo_root_rejects_invalid_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            invalid_root = Path(tmp)

            with self.assertRaisesRegex(FileNotFoundError, "Provided --root is not a valid repository root"):
                resolve_repo_root(str(invalid_root))


if __name__ == "__main__":
    unittest.main()
