# Copyright 2026 Google Sans Code authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Remove the BASE table from the TTF, and make no other changes.

This is a temporary workaround for the Android build.
"""

from argparse import ArgumentParser
from pathlib import Path

from fontTools.ttLib import TTFont

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.description = __doc__
    parser.add_argument("ttf", type=Path)
    args = parser.parse_args()

    ttf = TTFont(args.ttf, recalcBBoxes=False)
    del ttf["BASE"]
    ttf.save(args.ttf)
    # That's it!
