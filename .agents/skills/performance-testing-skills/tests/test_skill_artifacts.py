#!/usr/bin/env python3
"""Static regression checks for reusable performance-testing skill artifacts."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillArtifactTests(unittest.TestCase):
    def test_jmeter_reference_uses_valid_assertion_and_gaussian_examples(self):
        reference = (ROOT / "references" / "jmeter-plan-template.md").read_text(encoding="utf-8")
        self.assertIn('<stringProp name="Assertion.test_field">Assertion.response_code</stringProp>', reference)
        self.assertIn('<stringProp name="ConstantTimer.delay">2000</stringProp>', reference)
        self.assertIn('<stringProp name="RandomTimer.range">333</stringProp>', reference)

    def test_skill_explains_gaussian_timer_is_not_bounded(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("not a hard bound", skill)

    def test_skill_ships_analysis_and_endurance_automation(self):
        self.assertTrue((ROOT / "scripts" / "analyze_jtl.py").exists())
        self.assertTrue((ROOT / "scripts" / "run_endurance_template.sh").exists())


if __name__ == "__main__":
    unittest.main()
