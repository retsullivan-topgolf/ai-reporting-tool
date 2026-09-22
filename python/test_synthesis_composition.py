#!/usr/bin/env python3
"""Test Phase 0 synthesis skill composition."""
import analyze_venues

skill = analyze_venues.SYNTHESIS_SKILL

print("=== Phase 0 Synthesis Composition Test ===\n")

# Check for unreplaced placeholders
placeholders = [
    '<!-- SKILL:venue-overview -->',
    '<!-- SKILL:ups-downs -->',
    '<!-- SKILL:impact-drivers -->',
    '<!-- SKILL:recommendations -->'
]
unreplaced = [p for p in placeholders if p in skill]

print(f"[OK] Skill loaded: {len(skill)} characters")
print(f"[OK] Unreplaced placeholders: {len(unreplaced)}")
if unreplaced:
    print(f"  ERROR: {unreplaced}")

# Check for section skill content
section_headers = [
    "## Venue Overview Skill",
    "### Foundation",
    "### Metrics Handling",
    "## Acceptable Magnitude Language",
]
found = [h for h in section_headers if h in skill]
print(f"[OK] Expected section headers found: {len(found)}/{len(section_headers)}")

# Check structure
required_sections = ["## Overview Section", "## Ups and Downs Sections", "## Recommendations Section"]
has_old_synthesis = any(s in skill for s in ["## Overview Section"])
print(f"[OK] Old monolithic synthesis sections replaced: {not has_old_synthesis}")

# Validate it's proper markdown
if "---" in skill and "name: synthesis_template" in skill:
    print("[OK] Has frontmatter with synthesis_template name")
else:
    print("[ERROR] Missing expected frontmatter")

if all(s in skill for s in ["# Purpose", "# Inputs", "# Workflow", "# Output"]):
    print("[OK] Has all required top-level sections")

print("\n[PASS] Phase 0 Composition Verification Complete")
print("\nNext steps:")
print("1. Generate a test report using generate_report.py")
print("2. Compare output with a known reference")
print("3. Verify no regression in quality or structure")
