# Copyright 2025 Google Sans Flex authors
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

"""Remove the HVAR table from the TTF, and make no other changes.

This is used for the Android build, where it results in a smaller file, and
better performance."""

from argparse import ArgumentParser
from fontTools.ttLib import TTFont
from pathlib import Path


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.description = __doc__
    parser.add_argument("ttf", type=Path)
    args = parser.parse_args()

    ttf = TTFont(args.ttf, recalcBBoxes=False)
    del ttf["HVAR"]
    ttf.save(args.ttf)
    # That's it!