#!/usr/bin/env python3
import json
import os
from datetime import date

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")

entries = []
for namespace in sorted(os.listdir(SKILLS_DIR)):
    ns_dir = os.path.join(SKILLS_DIR, namespace)
    if not os.path.isdir(ns_dir):
        continue
    for name in sorted(os.listdir(ns_dir)):
        skill_dir = os.path.join(ns_dir, name)
        if not os.path.isdir(skill_dir):
            continue
        entries.append({
            "flattened_name": name,
            "source_path": f"skills/{namespace}/{name}",
        })

version = os.environ.get("RELEASE_VERSION") or date.today().strftime("%Y.%m.%d")

manifest = {
    "name": "flow-ai-skills",
    "version": version,
    "updated_at": date.today().isoformat(),
    "source": "repo",
    "skills": entries,
}

out_path = os.path.join(SKILLS_DIR, "manifest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(out_path)
print(f"skills: {len(entries)}")
