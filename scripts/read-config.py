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
import os
import re
import sys

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--sources", action="store_true")
group.add_argument("--family", action="store_true")
args = parser.parse_args()

with open(os.path.join("sources", "config.yaml")) as config:
    data = config.read()

if args.family:
    m = re.search(r"(?m)^familyName: (.*)", data)
    if m:
        print(m[1])
        sys.exit(0)
    else:
        print("Could not determine family name from config file!")
        sys.exit(1)

toggle = False
sources = []
for line in data.splitlines():
    if re.match("^sources:", line):
        toggle = True
        continue
    if toggle:
        m = re.match(r"^\s*-\s*(.*)", line)
        if m:
            sources.append("sources/" + m[1])
        else:
            toggle = False
if sources:
    print(" ".join(sources))
    sys.exit(0)
else:
    print("Could not determine sources from config file!")
    sys.exit(1)
