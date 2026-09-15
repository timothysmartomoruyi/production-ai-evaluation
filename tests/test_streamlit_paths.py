import os
import tempfile
import unittest
from pathlib import Path

from observability.metrics import load_logs


class StreamlitCloudPathTests(unittest.TestCase):
    def test_load_logs_works_outside_repo_root(self):
        repo_root = Path(__file__).resolve().parents[1]
        original_cwd = os.getcwd()

        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                os.chdir(tmp_dir)
                logs = load_logs()
                self.assertTrue(isinstance(logs, list))
                self.assertTrue(len(logs) > 0)
                self.assertTrue(all("status" in log for log in logs))
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
