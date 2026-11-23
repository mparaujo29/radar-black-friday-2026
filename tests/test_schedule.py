import os
import json
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch
from sys import path
path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import should_run

class ScheduleTests(unittest.TestCase):
    def test_missing_status_runs(self):
        with patch.object(should_run, "STATUS", Path("/path/that/does/not/exist.json")), patch.dict(os.environ, {"RUN_EVENT": "schedule"}):
            self.assertTrue(should_run.should_run()[0])

    def test_recent_check_skips_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "status.json"
            p.write_text(json.dumps({"last_execution_at": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()}))
            with patch.object(should_run, "STATUS", p), patch.dict(os.environ, {"RUN_EVENT": "schedule"}):
                self.assertFalse(should_run.should_run()[0])

    def test_manual_always_runs(self):
        with patch.dict(os.environ, {"RUN_EVENT": "workflow_dispatch"}):
            self.assertTrue(should_run.should_run()[0])

if __name__ == "__main__":
    unittest.main()
