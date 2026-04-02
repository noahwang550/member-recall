#!/usr/bin/env python3
"""
Direct package_skill wrapper
"""
import sys
import os
import fnmatch
import zipfile
from pathlib import Path

# Add skill-creator to path
CREATOR_PATH = r"C:\Users\noah.wang\.claude\skills\skill-creator"
sys.path.insert(0, CREATOR_PATH)

# Exclude patterns
EXCLUDE_DIRS = {"__pycache__", "node_modules"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}
ROOT_EXCLUDE_DIRS = {"evals"}

def should_exclude(rel_path):
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)

def package_skill(skill_path, output_dir=None):
    skill_path = Path(skill_path).resolve()
    if output_dir:
        output_dir = Path(output_dir).resolve()
    else:
        output_dir = Path.cwd()

    if not skill_path.exists():
        return f"Error: {skill_path} does not exist"

    skill_name = skill_path.name
    output_file = output_dir / f"{skill_name}.skill"

    print(f"Packaging {skill_name}...")

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob('*'):
            rel_path = file_path.relative_to(skill_path.parent)
            if should_exclude(rel_path):
                continue
            arc_path = rel_path
            zf.write(file_path, arc_path)
            print(f"  Added: {arc_path}")

    print(f"Created: {output_file}")
    return str(output_file)

if __name__ == "__main__":
    result = package_skill(r"D:\XD\ClaudeCode\myskill\skills\member-recall", r"D:\XD\ClaudeCode\myskill")
    print(f"\nResult: {result}")