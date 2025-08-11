#!/usr/bin/env python3

# Copyright 2025 Google Sans Code Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from pathlib import Path
import re
import sys


def read_config_file(path: Path) -> str:
    try:
        return path.read_text()
    except Exception as e:
        print(f"Error reading config file {path}: {e}", file=sys.stderr)
        sys.exit(1)

def extract_family_name(data: str) -> str | None:
    match = re.search(r"(?m)^familyName:\s*(.*)", data)
    return match.group(1).strip() if match else None

def extract_sources(data: str) -> list[str]:
    sources = []
    lines = data.splitlines()
    inside_sources = False

    for line in lines:
        if re.match(r"^sources:\s*$", line):
            inside_sources = True
            continue
        if inside_sources:
            match = re.match(r"^\s*-\s*(.+)", line)
            if match:
                sources.append(match.group(1).strip())
            else:
                break
    return sources

def main() -> None:
    parser = argparse.ArgumentParser(description="Parse config.yaml for family name or sources.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sources", action="store_true", help="Print sources list")
    group.add_argument("--family", action="store_true", help="Print family name")
    args = parser.parse_args()

    config_path = Path("sources") / "config.yaml"
    data = read_config_file(config_path)

    if args.family:
        family_name = extract_family_name(data)
        if family_name:
            print(family_name)
            return 0
        else:
            print("Could not determine family name from config file!", file=sys.stderr)
            return 1

    sources = extract_sources(data)
    if sources:
        sources_with_prefix = [str(Path("sources") / src) for src in sources]
        print(" ".join(sources_with_prefix))
        return 0
    else:
        print("Could not determine sources from config file!", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
