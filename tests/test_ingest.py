from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from scripts.ingest import condition_for_well, load_condition_by_row


ROOT = Path(__file__).resolve().parents[1]


class IngestConfigTests(unittest.TestCase):
    def test_gr2_condition_by_row_is_applied(self) -> None:
        mapping = load_condition_by_row(ROOT / "config/gr2_sitedirected.yaml")
        self.assertEqual("gr2", condition_for_well("A1", mapping))
        self.assertEqual("gr2", condition_for_well("H12", mapping))

    def test_gr7_condition_by_row_is_applied(self) -> None:
        mapping = load_condition_by_row(ROOT / "config/gr7_sitedirected.yaml")
        self.assertEqual("gr7", condition_for_well("B2", mapping))
        self.assertEqual("gr7", condition_for_well("G11", mapping))

    def test_gr14_condition_by_row_is_applied(self) -> None:
        mapping = load_condition_by_row(ROOT / "config/gr14_sitedirected.yaml")
        self.assertEqual("gr14", condition_for_well("C3", mapping))
        self.assertEqual("gr14", condition_for_well("F10", mapping))

    def test_yaml_parser_rejects_indented_line_without_parent(self) -> None:
        with NamedTemporaryFile("w", suffix=".yaml", delete=False) as config_file:
            config_file.write("  A: orphan\n")
            config_path = Path(config_file.name)
        try:
            with self.assertRaisesRegex(ValueError, "indented line without a parent key"):
                load_condition_by_row(config_path)
        finally:
            config_path.unlink()

    def test_yaml_parser_rejects_missing_colon_in_nested_entry(self) -> None:
        with NamedTemporaryFile("w", suffix=".yaml", delete=False) as config_file:
            config_file.write("condition_by_row:\n  A gr2\n")
            config_path = Path(config_file.name)
        try:
            with self.assertRaisesRegex(ValueError, "nested YAML entry missing colon separator"):
                load_condition_by_row(config_path)
        finally:
            config_path.unlink()


if __name__ == "__main__":
    unittest.main()
