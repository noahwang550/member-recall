#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Structural validation tests for the member-recall skill.
Can be run as:
    pytest tests/test_structure.py
or:
    python tests/test_structure.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
FAILURES = []


def check(cond, msg):
    """Assert-like check that accumulates failures."""
    if not cond:
        FAILURES.append(msg)
        print(f"  FAIL: {msg}")
    else:
        print(f"  PASS: {msg}")


def test_skill_md_exists():
    """SKILL.md exists and has valid frontmatter with name/description."""
    skill_path = SKILL_DIR / "SKILL.md"
    check(skill_path.is_file(), f"SKILL.md exists at {skill_path}")

    content = skill_path.read_text(encoding="utf-8")

    # Frontmatter check
    check(content.startswith("---"), "SKILL.md starts with frontmatter ---")
    check("name: member-recall" in content, "SKILL.md frontmatter contains name: member-recall")
    check("description:" in content, "SKILL.md frontmatter contains description:")

    # Description must contain step1.7
    # Extract frontmatter
    second_dash = content.find("---", 3)
    frontmatter = content[3:second_dash] if second_dash > 0 else ""
    check(
        "步骤1.7" in frontmatter,
        "SKILL.md frontmatter description contains '步骤1.7'"
    )

    # Heading for step 1.7
    check(
        "### 步骤1.7：联网调研" in content,
        "SKILL.md contains heading '### 步骤1.7：联网调研'"
    )

    # Reference to research_guide.md
    check(
        "references/research_guide.md" in content,
        "SKILL.md references 'references/research_guide.md'"
    )


def test_reference_docs_exist():
    """All files listed in the reference docs table exist."""
    expected_refs = [
        "references/motivation_guide.md",
        "references/copywriting_guide.md",
        "references/research_guide.md",
    ]
    for ref in expected_refs:
        ref_path = SKILL_DIR / ref
        check(ref_path.is_file(), f"Reference doc exists: {ref}")


def test_evals_json_valid():
    """evals/evals.json is valid JSON with unique integer ids."""
    evals_path = SKILL_DIR / "evals" / "evals.json"
    check(evals_path.is_file(), f"evals.json exists at {evals_path}")

    content = evals_path.read_text(encoding="utf-8")
    try:
        data = json.loads(content)
        check(isinstance(data, dict), "evals.json root is a dict")
        check("skill_name" in data, "evals.json has 'skill_name' key")
        check("evals" in data, "evals.json has 'evals' key")
        evals = data["evals"]
        check(isinstance(evals, list), "evals.json 'evals' is a list")

        ids = []
        for i, case in enumerate(evals):
            check(isinstance(case, dict), f"eval[{i}] is a dict")
            check("id" in case, f"eval[{i}] has 'id'")
            check("prompt" in case, f"eval[{i}] has 'prompt'")
            check("expected_output" in case, f"eval[{i}] has 'expected_output'")
            eid = case.get("id")
            check(isinstance(eid, int), f"eval[{i}] id is integer, got {type(eid).__name__}")
            ids.append(eid)

        check(len(ids) == len(set(ids)), "All eval ids are unique")
        check(6 in ids, "evals.json contains case id 6 (happy path research)")
        check(7 in ids, "evals.json contains case id 7 (degradation research)")
    except json.JSONDecodeError as e:
        check(False, f"evals.json is valid JSON: {e}")


def test_data_utils_imports():
    """scripts/data_utils.py imports cleanly."""
    script_dir = str(SKILL_DIR / "scripts")
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONPATH"] = env.get("PYTHONPATH", "") + os.pathsep + script_dir
        result = subprocess.run(
            [sys.executable, "-c", "import data_utils"],
            capture_output=True, text=True, timeout=30, env=env
        )
        check(result.returncode == 0, f"data_utils.py imports cleanly (stderr: {result.stderr.strip()})")
    except Exception as e:
        check(False, f"data_utils.py import subprocess error: {e}")


def test_data_utils_generate_test():
    """data_utils.py --action generate-test produces a CSV with 7 required columns."""
    required_cols = [
        "member_id", "last_purchase_days", "total_purchase_count",
        "total_spend", "coupon_usage_rate", "avg_order_value",
        "days_since_register"
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        output_csv = os.path.join(tmpdir, "test_output.csv")
        script = str(SKILL_DIR / "scripts" / "data_utils.py")
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(
                [sys.executable, script, "--action", "generate-test", "--output", output_csv, "--num", "100"],
                capture_output=True, text=True, timeout=60, env=env
            )
            check(
                result.returncode == 0,
                f"generate-test returns 0 (stderr: {result.stderr.strip()})"
            )
            check(
                os.path.exists(output_csv),
                f"generate-test creates output CSV at {output_csv}"
            )
            if os.path.exists(output_csv):
                with open(output_csv, "r", encoding="utf-8-sig") as f:
                    header = f.readline().strip()
                cols = [c.strip() for c in header.split(",")]
                for rc in required_cols:
                    check(rc in cols, f"generate-test CSV has column '{rc}'")
                check(
                    len(cols) >= 7,
                    f"generate-test CSV has at least 7 columns (got {len(cols)})"
                )
        except Exception as e:
            check(False, f"generate-test subprocess error: {e}")


def main():
    print("=" * 60)
    print("Member-Recall Skill Structural Validation Tests")
    print("=" * 60)

    print("\n[1] SKILL.md structure...")
    test_skill_md_exists()

    print("\n[2] Reference docs...")
    test_reference_docs_exist()

    print("\n[3] evals.json...")
    test_evals_json_valid()

    print("\n[4] data_utils.py import...")
    test_data_utils_imports()

    print("\n[5] data_utils.py generate-test...")
    test_data_utils_generate_test()

    print("\n" + "=" * 60)
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s) failed")
        for f in FAILURES:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("ALL TESTS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()