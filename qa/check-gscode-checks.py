# Copyright 2025 Google Sans Code Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fontbakery.prelude import check, PASS, FAIL


# GS Code uses 2000 UPM as opposed to the 1000 UPM these checks were based on
# originally
UPM_FACTOR = 2
# The custom checks below will check each of these attributes
ATTRIBUTES = {
    "hhea_ascent": 966
    * UPM_FACTOR,  # set to match typo metrics values, matches Google Sans
    "hhea_descent": -286 * UPM_FACTOR,
    "os2_fsselection_bit7": 1,
    "os2_typoascender": 966
    * UPM_FACTOR,  # set to match hhea metrics values, matches Google Sans
    "os2_typodescender": -286 * UPM_FACTOR,
    "os2_y_strikeout_position": 306 * UPM_FACTOR,
    "os2_y_strikeout_size": 84 * UPM_FACTOR,
    "post_underline_position": -160 * UPM_FACTOR,
    "post_underline_thickness": 84 * UPM_FACTOR,
}


# ================================================
#
# Conditions
#
# ================================================


# @condition
# def is_italic(ttFont):
#     return "Italic" in ttFont.reader.file.name


# @condition
# def is_not_italic(ttFont):
#     return "Italic" not in ttFont.reader.file.name


# @condition
# def is_not_variable_font(ttFont):
#     return "fvar" not in ttFont.keys()


# ================================================
#
# Begin check definitions
#
# ================================================


# ================================================
# OpenType table attribute checks
# ================================================

# ::::::::::::::::::::::::::::::::::::::::::::::::
# Vertical metrics
# ::::::::::::::::::::::::::::::::::::::::::::::::


# OS/2.fsSelection bit 7 (USE_TYPO_METRICS) is set in all fonts
@check(
    id="googlesans/opentype/os2/fsselectionbit7",
    rationale="""Confirms that fonts have OS/2.fsSelection bit 7 (USE_TYPO_METRICS) set \
    for typo vertical metrics (instead of win vertical metrics)
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_fsselectionbit7(ttFonts):
    """OS/2.fsSelection bit 7 (USE_TYPO_METRICS) is set in all fonts"""
    os2_fsselection_bit7_isset = ATTRIBUTES["os2_fsselection_bit7"] == 1

    found_fail = False
    fail_list = []
    for tt in ttFonts:
        fsselection_int = tt["OS/2"].fsSelection
        fsselection_bit_is_set_test = (fsselection_int & (1 << 7)) != 0
        if fsselection_bit_is_set_test is os2_fsselection_bit7_isset:
            pass
        else:
            found_fail = True
            fail_list.append(tt.reader.file.name)

    if found_fail:
        yield (
            FAIL,
            f"The OS/2.fsSelection bit 7 (USE_TYPO_METRICS) was NOT set "
            f"in the following fonts: {fail_list}.",
        )
    else:
        yield (
            PASS,
            "The OS/2.fsSelection bit 7 (USE_TYPO_METRICS) was set in all fonts.",
        )


# hhea.Ascent check
@check(
    id="googlesans/opentype/hhea/ascent",
    rationale="""Confirms that the hhea.ascent value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_hhea_ascent(ttFont):
    """hhea.ascent is defined as expected"""
    if ttFont["hhea"].ascent != ATTRIBUTES["hhea_ascent"]:
        yield (
            FAIL,
            f"The hhea.ascent value {ttFont['hhea'].ascent} does not "
            f"match the required value {ATTRIBUTES['hhea_ascent']}",
        )
    else:
        yield PASS, "The hhea.ascent value matches the required value."


# hhea.Descent check
@check(
    id="googlesans/opentype/hhea/descent",
    rationale="""Confirms that the hhea.descent value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_hhea_descent(ttFont):
    """hhea.descent is defined as expected"""
    if ttFont["hhea"].descent != ATTRIBUTES["hhea_descent"]:
        yield (
            FAIL,
            f"The hhea.descent value {ttFont['hhea'].descent} does not "
            f"match the required value {ATTRIBUTES['hhea_descent']}",
        )
    else:
        yield PASS, "The hhea.descent value matches the required value."


# OS/2.typoDescender check
@check(
    id="googlesans/opentype/os2/typodescender",
    rationale="""Confirms that the OS/2.typoDescender value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_typodescender(ttFont):
    """OS/2.typoDescender is defined as expected"""
    if ttFont["OS/2"].sTypoDescender != ATTRIBUTES["os2_typodescender"]:
        yield (
            FAIL,
            f"The OS/2.typoDescender value {ttFont['OS/2'].sTypoDescender} does not "
            f"match the required value {ATTRIBUTES['os2_typodescender']}",
        )
    else:
        yield PASS, "The OS/2.typoDescender value matches the required value."


# OS/2.typoAscender check
@check(
    id="googlesans/opentype/os2/typoascender",
    rationale="""Confirms that the OS/2.typoAscender value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_typoascender(ttFont):
    """OS/2.typoAscender is defined as expected"""
    if ttFont["OS/2"].sTypoAscender != ATTRIBUTES["os2_typoascender"]:
        yield (
            FAIL,
            f"The OS/2.typoAscender value {ttFont['OS/2'].sTypoAscender} does not "
            f"match the required value {ATTRIBUTES['os2_typoascender']}",
        )
    else:
        yield PASS, "The OS/2.typoAscender value matches the required value."


# ::::::::::::::::::::::::::::::::::::::::::::::::
# Consistency with prior release(s)
# ::::::::::::::::::::::::::::::::::::::::::::::::


@check(
    id="googlesans/opentype/post/underline_position",
    rationale="""Confirms that fonts have post.underlinePosition set to expected value.
    """,
)
def com_google_fonts_check_googlesans_opentype_post_underline_position(ttFonts):
    """post.underlinePosition is set to expected value from GS Mono v1.002"""
    expected = ATTRIBUTES["post_underline_position"]
    for tt in ttFonts:
        actual = tt["post"].underlinePosition
        if actual != expected:
            yield (
                FAIL,
                f"{tt.reader.file.name} does not have post.underlinePosition set to "
                f"{expected}.  Observed value = {actual}",
            )

    yield (
        PASS,
        f"All fonts have post.underlinePosition value set to {expected}",
    )


@check(
    id="googlesans/opentype/post/underline_thickness",
    rationale="""Confirms that fonts have post.underlineThickness set to expected value.
    """,
)
def com_google_fonts_check_googlesans_opentype_post_underline_thickness(ttFonts):
    """post.underlineThickness is set to expected value from GS Mono v1.002"""
    expected = ATTRIBUTES["post_underline_thickness"]
    for tt in ttFonts:
        actual = tt["post"].underlineThickness
        if actual != expected:
            yield (
                FAIL,
                f"{tt.reader.file.name} does not have post.underlineThickness set to "
                f"{expected}.  Observed value = {actual}",
            )

    yield (
        PASS,
        f"All fonts have post.underlineThickness value set to {expected}",
    )


@check(
    id="googlesans/opentype/os2/y_strikeout_position",
    rationale="""Confirms that fonts have OS/2.yStrikeoutPosition set to expected value.
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_y_strikeout_position(ttFonts):
    """OS/2.yStrikeoutPosition is set to expected value from GS Mono v1.002"""
    expected = ATTRIBUTES["os2_y_strikeout_position"]
    for tt in ttFonts:
        actual = tt["OS/2"].yStrikeoutPosition
        if actual != expected:
            yield (
                FAIL,
                f"{tt.reader.file.name} does not have OS/2.yStrikeoutPosition set to "
                f"{expected}.  Observed value = {actual}",
            )

    yield (
        PASS,
        f"All fonts have OS/2.yStrikeoutPosition value set to {expected}",
    )


@check(
    id="googlesans/opentype/os2/y_strikeout_size",
    rationale="""Confirms that fonts have OS/2.yStrikeoutSize set to expected value.
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_y_strikeout_size(ttFonts):
    """OS/2.yStrikeoutSize is set to expected value from GS Mono v1.002"""
    expected = ATTRIBUTES["os2_y_strikeout_size"]
    for tt in ttFonts:
        actual = tt["OS/2"].yStrikeoutSize
        if actual != expected:
            yield (
                FAIL,
                f"{tt.reader.file.name} does not have OS/2.yStrikeoutSize set to "
                f"{expected}.  Observed value = {actual}",
            )

    yield (
        PASS,
        f"All fonts have OS/2.yStrikeoutSize value set to {expected}",
    )


# ================================================
#
# End check definitions
#
# ================================================
