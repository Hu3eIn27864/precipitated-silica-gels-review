import argparse
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from run_dlca_size_series import nonnegative_int, positive_int, scaled_box_length


class SizeSeriesRunnerTests(unittest.TestCase):
    def test_box_scaling_preserves_number_density(self):
        reference = scaled_box_length(32, 32, 15.0)
        doubled = scaled_box_length(64, 32, 15.0)
        self.assertAlmostEqual(reference, 15.0)
        self.assertAlmostEqual(doubled / reference, 2.0 ** (1.0 / 3.0))
        self.assertAlmostEqual(64 / doubled**3, 32 / reference**3)

    def test_seed_start_can_be_zero(self):
        self.assertEqual(nonnegative_int("0"), 0)

    def test_sizes_must_be_positive(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            positive_int("0")

    def test_cli_invokes_each_size_with_scaled_box_and_seed_range(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / "calls.txt"
            fake = root / "fake_mc3d.py"
            fake.write_text(
                "#!/usr/bin/env python3\n"
                "import sys\n"
                "with open(" + repr(str(log)) + ", 'a', encoding='utf-8') as f: "
                "f.write(' '.join(sys.argv[1:]) + '\\n')\n",
                encoding="utf-8",
            )
            fake.chmod(0o755)
            output_dir = root / "out"
            script = Path(__file__).with_name("run_dlca_size_series.py")
            subprocess.run(
                [sys.executable, str(script), "--executable", str(fake),
                 "--output-dir", str(output_dir), "--sizes", "32", "64",
                 "--seed-start", "0", "--seed-count", "2", "--max-attempts", "50"],
                check=True, capture_output=True, text=True,
            )
            calls = log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(calls), 2)
            first = calls[0].split()
            second = calls[1].split()
            self.assertEqual(first[0:1], ["32"])
            self.assertEqual(second[0:1], ["64"])
            self.assertAlmostEqual(float(first[1]), 15.0)
            self.assertAlmostEqual(float(second[1]), 15.0 * 2 ** (1 / 3))
            self.assertEqual(first[2:5], ["0", "2", "50"])
            self.assertEqual(second[2:5], ["2", "2", "50"])


if __name__ == "__main__":
    unittest.main()
