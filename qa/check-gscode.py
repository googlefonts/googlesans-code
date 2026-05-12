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

from pathlib import Path

PROFILE = {
    "include_profiles": ["googlefonts"],
    # The checks are in a separate file, because Simon says that eventually this
    # file will become pure data.
    "check_definitions": [Path(__file__).parent / "check-gscode-checks.py"],
    "sections": {
        "Google Sans Code Custom Checks": [
            "googlesans/opentype/hhea/ascent",
            "googlesans/opentype/hhea/descent",
            "googlesans/opentype/os2/fsselectionbit7",
            "googlesans/opentype/os2/typoascender",
            "googlesans/opentype/os2/typodescender",
            "googlesans/opentype/os2/y_strikeout_position",
            "googlesans/opentype/os2/y_strikeout_size",
            "googlesans/opentype/post/underline_position",
            "googlesans/opentype/post/underline_thickness",
        ]
    },
    "exclude_checks": [
        # positive findings in monospaced is bug
        "gpos_kerning_info",
        # We do our own shaperglot checks
        # Requested to be disabled by Kalapi: https://github.com/googlefonts/googlesans-code/issues/17#issuecomment-2442567685
        "googlefonts/glyphsets/shape_languages",
        "googlefonts/glyph_coverage",
        "googlefonts/article/images",
        "googlefonts/metadata/unreachable_subsetting",
        "googlefonts/meta/script_lang_tags",
        # Our typoAscender is fixed to that of Google Sans
        "typoascender_exceeds_Agrave",
        # temporary deactivation of the 32 char length check
        "name/family_and_style_max_length",
        # we intentionally include a RFN in this project
        "googlefonts/font_copyright",
        "googlefonts/license/OFL_copyright",
        # We won't rename the font as Monospaced, and that's why we added a
        # customised version of this check
        "googlefonts/font_names",
        # We don't set post.isFixedPitch because we have an axis that lets us be
        # not-monospace
        "opentype/monospace",
        "mandatory_avar_table",
        # We don't want to add a prep table:
        # https://github.com/googlefonts/googlesans-code/issues/12
        "smart_dropout",
        # We're not overly concerned about being able to make statics from the
        # VF
        "googlefonts/varfont/generate_static",
    ],
    "overrides": {
        "googlefonts/STAT/axisregistry": [
            {
                "code": "bad-coordinate",
                "status": "INFO",
                "reason": "expected & approved for GS Code to have Monospaced @ 0 "
                "and Proportional @ 1 (the inverse to the axis registry's expectation)",
            },
        ],
        "fontdata_namecheck": [
            {
                "code": "namecheck-service",
                "status": "WARN",
                "reason": "we know Google Sans Code is okay, "
                "so it doesn't matter if the service is offline for a bit",
            }
        ],
    },
}
