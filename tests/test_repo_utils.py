from __future__ import annotations

import unittest

from cli.repo import normalize_url


class RepoUtilsTests(unittest.TestCase):
    def test_normalize_url_strips_tracking_params_and_default_port(self) -> None:
        normalized = normalize_url("HTTPS://Example.com:443/path?utm_source=x&id=1&fbclid=abc")
        self.assertEqual(normalized, "https://example.com/path?id=1")

    def test_normalize_url_requires_absolute_url(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid absolute url"):
            normalize_url("/relative/path")


if __name__ == "__main__":
    unittest.main()
