# Langdet language detection / classification.
# Jonathan Koren <jonathan@jonathankoren.com>
#
# MIT License
#
# Copyright (c) 2018 Jonathan Koren
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import math
import operator
import sys

def unicodePlane(c):
    '''Takes a single character, and returns a string identifing the UNICODE
    code plane.'''
    if 0x0000 <= ord(c) and ord(c) <= 0x007F: return 'Basic Latin (ASCII)'
    if 0x0080 <= ord(c) and ord(c) <= 0x00FF: return 'Latin-1 Supplement (Extended ASCII)'
    if 0x0100 <= ord(c) and ord(c) <= 0x017F: return 'Latin Extended-A'
    if 0x0180 <= ord(c) and ord(c) <= 0x024F: return 'Latin Extended-B'
    if 0x0250 <= ord(c) and ord(c) <= 0x02AF: return 'IPA Extensions'
    if 0x02B0 <= ord(c) and ord(c) <= 0x02FF: return 'Spacing Modifier Letters'
    if 0x0300 <= ord(c) and ord(c) <= 0x036F: return 'Combining Diacritical Marks'
    if 0x0370 <= ord(c) and ord(c) <= 0x03FF: return 'Greek and Coptic'
    if 0x0400 <= ord(c) and ord(c) <= 0x04FF: return 'Cyrillic'
    if 0x0500 <= ord(c) and ord(c) <= 0x052F: return 'Cyrillic Supplement'
    if 0x0530 <= ord(c) and ord(c) <= 0x058F: return 'Armenian'
    if 0x0590 <= ord(c) and ord(c) <= 0x05FF: return 'Hebrew'
    if 0x0600 <= ord(c) and ord(c) <= 0x06FF: return 'Arabic'
    if 0x0700 <= ord(c) and ord(c) <= 0x074F: return 'Syriac'
    if 0x0750 <= ord(c) and ord(c) <= 0x077F: return 'Arabic Supplement'
    if 0x0780 <= ord(c) and ord(c) <= 0x07BF: return 'Thaana'
    if 0x07C0 <= ord(c) and ord(c) <= 0x07FF: return 'N\'Ko'
    if 0x0800 <= ord(c) and ord(c) <= 0x083F: return 'Samaritan'
    if 0x0840 <= ord(c) and ord(c) <= 0x085F: return 'Mandaic'
    if 0x0860 <= ord(c) and ord(c) <= 0x086F: return 'Syriac Supplement'
    if 0x08A0 <= ord(c) and ord(c) <= 0x08FF: return 'Arabic Extended-A'
    if 0x0900 <= ord(c) and ord(c) <= 0x097F: return 'Devanagari'
    if 0x0980 <= ord(c) and ord(c) <= 0x09FF: return 'Bengali'
    if 0x0A00 <= ord(c) and ord(c) <= 0x0A7F: return 'Gurmukhi'
    if 0x0A80 <= ord(c) and ord(c) <= 0x0AFF: return 'Gujarati'
    if 0x0B00 <= ord(c) and ord(c) <= 0x0B7F: return 'Oriya'
    if 0x0B80 <= ord(c) and ord(c) <= 0x0BFF: return 'Tamil'
    if 0x0C00 <= ord(c) and ord(c) <= 0x0C7F: return 'Telugu'
    if 0x0C80 <= ord(c) and ord(c) <= 0x0CFF: return 'Kannada'
    if 0x0D00 <= ord(c) and ord(c) <= 0x0D7F: return 'Malayalam'
    if 0x0D80 <= ord(c) and ord(c) <= 0x0DFF: return 'Sinhala'
    if 0x0E00 <= ord(c) and ord(c) <= 0x0E7F: return 'Thai'
    if 0x0E80 <= ord(c) and ord(c) <= 0x0EFF: return 'Lao'
    if 0x0F00 <= ord(c) and ord(c) <= 0x0FFF: return 'Tibetan'
    if 0x1000 <= ord(c) and ord(c) <= 0x109F: return 'Myanmar'
    if 0x10A0 <= ord(c) and ord(c) <= 0x10FF: return 'Georgian'
    if 0x1100 <= ord(c) and ord(c) <= 0x11FF: return 'Hangul Jamo'
    if 0x1200 <= ord(c) and ord(c) <= 0x137F: return 'Ethiopic'
    if 0x1380 <= ord(c) and ord(c) <= 0x139F: return 'Ethiopic Supplement'
    if 0x13A0 <= ord(c) and ord(c) <= 0x13FF: return 'Cherokee'
    if 0x1400 <= ord(c) and ord(c) <= 0x167F: return 'Unified Canadian Aboriginal Syllabics'
    if 0x1680 <= ord(c) and ord(c) <= 0x169F: return 'Ogham'
    if 0x16A0 <= ord(c) and ord(c) <= 0x16FF: return 'Runic'
    if 0x1700 <= ord(c) and ord(c) <= 0x171F: return 'Tagalog'
    if 0x1720 <= ord(c) and ord(c) <= 0x173F: return 'Hanunoo'
    if 0x1740 <= ord(c) and ord(c) <= 0x175F: return 'Buhid'
    if 0x1760 <= ord(c) and ord(c) <= 0x177F: return 'Tagbanwa'
    if 0x1780 <= ord(c) and ord(c) <= 0x17FF: return 'Khmer'
    if 0x1800 <= ord(c) and ord(c) <= 0x18AF: return 'Mongolian'
    if 0x18B0 <= ord(c) and ord(c) <= 0x18FF: return 'Unified Canadian Aboriginal Syllabics Extended'
    if 0x1900 <= ord(c) and ord(c) <= 0x194F: return 'Limbu'
    if 0x1950 <= ord(c) and ord(c) <= 0x197F: return 'Tai Le'
    if 0x1980 <= ord(c) and ord(c) <= 0x19DF: return 'New Tai Lue'
    if 0x19E0 <= ord(c) and ord(c) <= 0x19FF: return 'Khmer Symbols'
    if 0x1A00 <= ord(c) and ord(c) <= 0x1A1F: return 'Buginese'
    if 0x1A20 <= ord(c) and ord(c) <= 0x1AAF: return 'Tai Tham'
    if 0x1AB0 <= ord(c) and ord(c) <= 0x1AFF: return 'Combining Diacritical Marks Extended'
    if 0x1B00 <= ord(c) and ord(c) <= 0x1B7F: return 'Balinese'
    if 0x1B80 <= ord(c) and ord(c) <= 0x1BBF: return 'Sundanese'
    if 0x1BC0 <= ord(c) and ord(c) <= 0x1BFF: return 'Batak'
    if 0x1C00 <= ord(c) and ord(c) <= 0x1C4F: return 'Lepcha'
    if 0x1C50 <= ord(c) and ord(c) <= 0x1C7F: return 'Ol Chiki'
    if 0x1C80 <= ord(c) and ord(c) <= 0x1C8F: return 'Cyrillic Extended-C'
    if 0x1CC0 <= ord(c) and ord(c) <= 0x1CCF: return 'Sundanese Supplement'
    if 0x1CD0 <= ord(c) and ord(c) <= 0x1CFF: return 'Vedic Extensions'
    if 0x1D00 <= ord(c) and ord(c) <= 0x1D7F: return 'Phonetic Extensions'
    if 0x1D80 <= ord(c) and ord(c) <= 0x1DBF: return 'Phonetic Extensions Supplement'
    if 0x1DC0 <= ord(c) and ord(c) <= 0x1DFF: return 'Combining Diacritical Marks Supplement'
    if 0x1E00 <= ord(c) and ord(c) <= 0x1EFF: return 'Latin Extended Additional'
    if 0x1F00 <= ord(c) and ord(c) <= 0x1FFF: return 'Greek Extended'
    if 0x2000 <= ord(c) and ord(c) <= 0x206F: return 'General Punctuation'
    if 0x2070 <= ord(c) and ord(c) <= 0x209F: return 'Superscripts and Subscripts'
    if 0x20A0 <= ord(c) and ord(c) <= 0x20CF: return 'Currency Symbols'
    if 0x20D0 <= ord(c) and ord(c) <= 0x20FF: return 'Combining Diacritical Marks for Symbols'
    if 0x2100 <= ord(c) and ord(c) <= 0x214F: return 'Letterlike Symbols'
    if 0x2150 <= ord(c) and ord(c) <= 0x218F: return 'Number Forms'
    if 0x2190 <= ord(c) and ord(c) <= 0x21FF: return 'Arrows'
    if 0x2200 <= ord(c) and ord(c) <= 0x22FF: return 'Mathematical Operators'
    if 0x2300 <= ord(c) and ord(c) <= 0x23FF: return 'Miscellaneous Technical'
    if 0x2400 <= ord(c) and ord(c) <= 0x243F: return 'Control Pictures'
    if 0x2440 <= ord(c) and ord(c) <= 0x245F: return 'Optical Character Recognition'
    if 0x2460 <= ord(c) and ord(c) <= 0x24FF: return 'Enclosed Alphanumerics'
    if 0x2500 <= ord(c) and ord(c) <= 0x257F: return 'Box Drawing'
    if 0x2580 <= ord(c) and ord(c) <= 0x259F: return 'Block Elements'
    if 0x25A0 <= ord(c) and ord(c) <= 0x25FF: return 'Geometric Shapes'
    if 0x2600 <= ord(c) and ord(c) <= 0x26FF: return 'Miscellaneous Symbols'
    if 0x2700 <= ord(c) and ord(c) <= 0x27BF: return 'Dingbats'
    if 0x27C0 <= ord(c) and ord(c) <= 0x27EF: return 'Miscellaneous Mathematical Symbols-A'
    if 0x27F0 <= ord(c) and ord(c) <= 0x27FF: return 'Supplemental Arrows-A'
    if 0x2800 <= ord(c) and ord(c) <= 0x28FF: return 'Braille Patterns'
    if 0x2900 <= ord(c) and ord(c) <= 0x297F: return 'Supplemental Arrows-B'
    if 0x2980 <= ord(c) and ord(c) <= 0x29FF: return 'Miscellaneous Mathematical Symbols-B'
    if 0x2A00 <= ord(c) and ord(c) <= 0x2AFF: return 'Supplemental Mathematical Operators'
    if 0x2B00 <= ord(c) and ord(c) <= 0x2BFF: return 'Miscellaneous Symbols and Arrows'
    if 0x2C00 <= ord(c) and ord(c) <= 0x2C5F: return 'Glagolitic'
    if 0x2C60 <= ord(c) and ord(c) <= 0x2C7F: return 'Latin Extended-C'
    if 0x2C80 <= ord(c) and ord(c) <= 0x2CFF: return 'Coptic'
    if 0x2D00 <= ord(c) and ord(c) <= 0x2D2F: return 'Georgian Supplement'
    if 0x2D30 <= ord(c) and ord(c) <= 0x2D7F: return 'Tifinagh'
    if 0x2D80 <= ord(c) and ord(c) <= 0x2DDF: return 'Ethiopic Extended'
    if 0x2DE0 <= ord(c) and ord(c) <= 0x2DFF: return 'Cyrillic Extended-A'
    if 0x2E00 <= ord(c) and ord(c) <= 0x2E7F: return 'Supplemental Punctuation'
    if 0x2E80 <= ord(c) and ord(c) <= 0x2EFF: return 'CJK Radicals Supplement'
    if 0x2F00 <= ord(c) and ord(c) <= 0x2FDF: return 'Kangxi Radicals'
    if 0x2FF0 <= ord(c) and ord(c) <= 0x2FFF: return 'Ideographic Description Characters'
    if 0x3000 <= ord(c) and ord(c) <= 0x303F: return 'CJK Symbols and Punctuation'
    if 0x3040 <= ord(c) and ord(c) <= 0x309F: return 'Hiragana'
    if 0x30A0 <= ord(c) and ord(c) <= 0x30FF: return 'Katakana'
    if 0x3100 <= ord(c) and ord(c) <= 0x312F: return 'Bopomofo'
    if 0x3130 <= ord(c) and ord(c) <= 0x318F: return 'Hangul Compatibility Jamo'
    if 0x3190 <= ord(c) and ord(c) <= 0x319F: return 'Kanbun'
    if 0x31A0 <= ord(c) and ord(c) <= 0x31BF: return 'Bopomofo Extended'
    if 0x31C0 <= ord(c) and ord(c) <= 0x31EF: return 'CJK Strokes'
    if 0x31F0 <= ord(c) and ord(c) <= 0x31FF: return 'Katakana Phonetic Extensions'
    if 0x3200 <= ord(c) and ord(c) <= 0x32FF: return 'Enclosed CJK Letters and Months'
    if 0x3300 <= ord(c) and ord(c) <= 0x33FF: return 'CJK Compatibility'
    if 0x3400 <= ord(c) and ord(c) <= 0x4DBF: return 'CJK Unified Ideographs Extension A'
    if 0x4DC0 <= ord(c) and ord(c) <= 0x4DFF: return 'Yijing Hexagram Symbols'
    if 0x4E00 <= ord(c) and ord(c) <= 0x9FFF: return 'CJK Unified Ideographs'
    if 0xA000 <= ord(c) and ord(c) <= 0xA48F: return 'Yi Syllables'
    if 0xA490 <= ord(c) and ord(c) <= 0xA4CF: return 'Yi Radicals'
    if 0xA4D0 <= ord(c) and ord(c) <= 0xA4FF: return 'Lisu'
    if 0xA500 <= ord(c) and ord(c) <= 0xA63F: return 'Vai'
    if 0xA640 <= ord(c) and ord(c) <= 0xA69F: return 'Cyrillic Extended-B'
    if 0xA6A0 <= ord(c) and ord(c) <= 0xA6FF: return 'Bamum'
    if 0xA700 <= ord(c) and ord(c) <= 0xA71F: return 'Modifier Tone Letters'
    if 0xA720 <= ord(c) and ord(c) <= 0xA7FF: return 'Latin Extended-D'
    if 0xA800 <= ord(c) and ord(c) <= 0xA82F: return 'Syloti Nagri'
    if 0xA830 <= ord(c) and ord(c) <= 0xA83F: return 'Common Indic Number Forms'
    if 0xA840 <= ord(c) and ord(c) <= 0xA87F: return 'Phags-pa'
    if 0xA880 <= ord(c) and ord(c) <= 0xA8DF: return 'Saurashtra'
    if 0xA8E0 <= ord(c) and ord(c) <= 0xA8FF: return 'Devanagari Extended'
    if 0xA900 <= ord(c) and ord(c) <= 0xA92F: return 'Kayah Li'
    if 0xA930 <= ord(c) and ord(c) <= 0xA95F: return 'Rejang'
    if 0xA960 <= ord(c) and ord(c) <= 0xA97F: return 'Hangul Jamo Extended-A'
    if 0xA980 <= ord(c) and ord(c) <= 0xA9DF: return 'Javanese'
    if 0xA9E0 <= ord(c) and ord(c) <= 0xA9FF: return 'Myanmar Extended-B'
    if 0xAA00 <= ord(c) and ord(c) <= 0xAA5F: return 'Cham'
    if 0xAA60 <= ord(c) and ord(c) <= 0xAA7F: return 'Myanmar Extended-A'
    if 0xAA80 <= ord(c) and ord(c) <= 0xAADF: return 'Tai Viet'
    if 0xAAE0 <= ord(c) and ord(c) <= 0xAAFF: return 'Meetei Mayek Extensions'
    if 0xAB00 <= ord(c) and ord(c) <= 0xAB2F: return 'Ethiopic Extended-A'
    if 0xAB30 <= ord(c) and ord(c) <= 0xAB6F: return 'Latin Extended-E'
    if 0xAB70 <= ord(c) and ord(c) <= 0xABBF: return 'Cherokee Supplement'
    if 0xABC0 <= ord(c) and ord(c) <= 0xABFF: return 'Meetei Mayek'
    if 0xAC00 <= ord(c) and ord(c) <= 0xD7AF: return 'Hangul Syllables'
    if 0xD7B0 <= ord(c) and ord(c) <= 0xD7FF: return 'Hangul Jamo Extended-B'
    if 0xD800 <= ord(c) and ord(c) <= 0xDB7F: return 'High Surrogates'
    if 0xDB80 <= ord(c) and ord(c) <= 0xDBFF: return 'High Private Use Surrogates'
    if 0xDC00 <= ord(c) and ord(c) <= 0xDFFF: return 'Low Surrogates'
    if 0xE000 <= ord(c) and ord(c) <= 0xF8FF: return 'Private Use Area'
    if 0xF900 <= ord(c) and ord(c) <= 0xFAFF: return 'CJK Compatibility Ideographs'
    if 0xFB00 <= ord(c) and ord(c) <= 0xFB4F: return 'Alphabetic Presentation Forms'
    if 0xFB50 <= ord(c) and ord(c) <= 0xFDFF: return 'Arabic Presentation Forms-A'
    if 0xFE00 <= ord(c) and ord(c) <= 0xFE0F: return 'Variation Selectors'
    if 0xFE10 <= ord(c) and ord(c) <= 0xFE1F: return 'Vertical Forms'
    if 0xFE20 <= ord(c) and ord(c) <= 0xFE2F: return 'Combining Half Marks'
    if 0xFE30 <= ord(c) and ord(c) <= 0xFE4F: return 'CJK Compatibility Forms'
    if 0xFE50 <= ord(c) and ord(c) <= 0xFE6F: return 'Small Form Variants'
    if 0xFE70 <= ord(c) and ord(c) <= 0xFEFF: return 'Arabic Presentation Forms-B'
    if 0xFF00 <= ord(c) and ord(c) <= 0xFFEF: return 'Halfwidth and Fullwidth Forms'
    if 0xFFF0 <= ord(c) and ord(c) <= 0xFFFF: return 'Specials'
    if 0x10000 <= ord(c) and ord(c) <= 0x1007F: return 'Linear B Syllabary'
    if 0x10080 <= ord(c) and ord(c) <= 0x100FF: return 'Linear B Ideograms'
    if 0x10100 <= ord(c) and ord(c) <= 0x1013F: return 'Aegean Numbers'
    if 0x10140 <= ord(c) and ord(c) <= 0x1018F: return 'Ancient Greek Numbers'
    if 0x10190 <= ord(c) and ord(c) <= 0x101CF: return 'Ancient Symbols'
    if 0x101D0 <= ord(c) and ord(c) <= 0x101FF: return 'Phaistos Disc'
    if 0x10280 <= ord(c) and ord(c) <= 0x1029F: return 'Lycian'
    if 0x102A0 <= ord(c) and ord(c) <= 0x102DF: return 'Carian'
    if 0x102E0 <= ord(c) and ord(c) <= 0x102FF: return 'Coptic Epact Numbers'
    if 0x10300 <= ord(c) and ord(c) <= 0x1032F: return 'Old Italic'
    if 0x10330 <= ord(c) and ord(c) <= 0x1034F: return 'Gothic'
    if 0x10350 <= ord(c) and ord(c) <= 0x1037F: return 'Old Permic'
    if 0x10380 <= ord(c) and ord(c) <= 0x1039F: return 'Ugaritic'
    if 0x103A0 <= ord(c) and ord(c) <= 0x103DF: return 'Old Persian'
    if 0x10400 <= ord(c) and ord(c) <= 0x1044F: return 'Deseret'
    if 0x10450 <= ord(c) and ord(c) <= 0x1047F: return 'Shavian'
    if 0x10480 <= ord(c) and ord(c) <= 0x104AF: return 'Osmanya'
    if 0x104B0 <= ord(c) and ord(c) <= 0x104FF: return 'Osage'
    if 0x10500 <= ord(c) and ord(c) <= 0x1052F: return 'Elbasan'
    if 0x10530 <= ord(c) and ord(c) <= 0x1056F: return 'Caucasian Albanian'
    if 0x10600 <= ord(c) and ord(c) <= 0x1077F: return 'Linear A'
    if 0x10800 <= ord(c) and ord(c) <= 0x1083F: return 'Cypriot Syllabary'
    if 0x10840 <= ord(c) and ord(c) <= 0x1085F: return 'Imperial Aramaic'
    if 0x10860 <= ord(c) and ord(c) <= 0x1087F: return 'Palmyrene'
    if 0x10880 <= ord(c) and ord(c) <= 0x108AF: return 'Nabataean'
    if 0x108E0 <= ord(c) and ord(c) <= 0x108FF: return 'Hatran'
    if 0x10900 <= ord(c) and ord(c) <= 0x1091F: return 'Phoenician'
    if 0x10920 <= ord(c) and ord(c) <= 0x1093F: return 'Lydian'
    if 0x10980 <= ord(c) and ord(c) <= 0x1099F: return 'Meroitic Hieroglyphs'
    if 0x109A0 <= ord(c) and ord(c) <= 0x109FF: return 'Meroitic Cursive'
    if 0x10A00 <= ord(c) and ord(c) <= 0x10A5F: return 'Kharoshthi'
    if 0x10A60 <= ord(c) and ord(c) <= 0x10A7F: return 'Old South Arabian'
    if 0x10A80 <= ord(c) and ord(c) <= 0x10A9F: return 'Old North Arabian'
    if 0x10AC0 <= ord(c) and ord(c) <= 0x10AFF: return 'Manichaean'
    if 0x10B00 <= ord(c) and ord(c) <= 0x10B3F: return 'Avestan'
    if 0x10B40 <= ord(c) and ord(c) <= 0x10B5F: return 'Inscriptional Parthian'
    if 0x10B60 <= ord(c) and ord(c) <= 0x10B7F: return 'Inscriptional Pahlavi'
    if 0x10B80 <= ord(c) and ord(c) <= 0x10BAF: return 'Psalter Pahlavi'
    if 0x10C00 <= ord(c) and ord(c) <= 0x10C4F: return 'Old Turkic'
    if 0x10C80 <= ord(c) and ord(c) <= 0x10CFF: return 'Old Hungarian'
    if 0x10E60 <= ord(c) and ord(c) <= 0x10E7F: return 'Rumi Numeral Symbols'
    if 0x11000 <= ord(c) and ord(c) <= 0x1107F: return 'Brahmi'
    if 0x11080 <= ord(c) and ord(c) <= 0x110CF: return 'Kaithi'
    if 0x110D0 <= ord(c) and ord(c) <= 0x110FF: return 'Sora Sompeng'
    if 0x11100 <= ord(c) and ord(c) <= 0x1114F: return 'Chakma'
    if 0x11150 <= ord(c) and ord(c) <= 0x1117F: return 'Mahajani'
    if 0x11180 <= ord(c) and ord(c) <= 0x111DF: return 'Sharada'
    if 0x111E0 <= ord(c) and ord(c) <= 0x111FF: return 'Sinhala Archaic Numbers'
    if 0x11200 <= ord(c) and ord(c) <= 0x1124F: return 'Khojki'
    if 0x11280 <= ord(c) and ord(c) <= 0x112AF: return 'Multani'
    if 0x112B0 <= ord(c) and ord(c) <= 0x112FF: return 'Khudawadi'
    if 0x11300 <= ord(c) and ord(c) <= 0x1137F: return 'Grantha'
    if 0x11400 <= ord(c) and ord(c) <= 0x1147F: return 'Newa'
    if 0x11480 <= ord(c) and ord(c) <= 0x114DF: return 'Tirhuta'
    if 0x11580 <= ord(c) and ord(c) <= 0x115FF: return 'Siddham'
    if 0x11600 <= ord(c) and ord(c) <= 0x1165F: return 'Modi'
    if 0x11660 <= ord(c) and ord(c) <= 0x1167F: return 'Mongolian Supplement'
    if 0x11680 <= ord(c) and ord(c) <= 0x116CF: return 'Takri'
    if 0x11700 <= ord(c) and ord(c) <= 0x1173F: return 'Ahom'
    if 0x118A0 <= ord(c) and ord(c) <= 0x118FF: return 'Warang Citi'
    if 0x11A00 <= ord(c) and ord(c) <= 0x11A4F: return 'Zanabazar Square'
    if 0x11A50 <= ord(c) and ord(c) <= 0x11AAF: return 'Soyombo'
    if 0x11AC0 <= ord(c) and ord(c) <= 0x11AFF: return 'Pau Cin Hau'
    if 0x11C00 <= ord(c) and ord(c) <= 0x11C6F: return 'Bhaiksuki'
    if 0x11C70 <= ord(c) and ord(c) <= 0x11CBF: return 'Marchen'
    if 0x11D00 <= ord(c) and ord(c) <= 0x11D5F: return 'Masaram Gondi'
    if 0x12000 <= ord(c) and ord(c) <= 0x123FF: return 'Cuneiform'
    if 0x12400 <= ord(c) and ord(c) <= 0x1247F: return 'Cuneiform Numbers and Punctuation'
    if 0x12480 <= ord(c) and ord(c) <= 0x1254F: return 'Early Dynastic Cuneiform'
    if 0x13000 <= ord(c) and ord(c) <= 0x1342F: return 'Egyptian Hieroglyphs'
    if 0x14400 <= ord(c) and ord(c) <= 0x1467F: return 'Anatolian Hieroglyphs'
    if 0x16800 <= ord(c) and ord(c) <= 0x16A3F: return 'Bamum Supplement'
    if 0x16A40 <= ord(c) and ord(c) <= 0x16A6F: return 'Mro'
    if 0x16AD0 <= ord(c) and ord(c) <= 0x16AFF: return 'Bassa Vah'
    if 0x16B00 <= ord(c) and ord(c) <= 0x16B8F: return 'Pahawh Hmong'
    if 0x16F00 <= ord(c) and ord(c) <= 0x16F9F: return 'Miao'
    if 0x16FE0 <= ord(c) and ord(c) <= 0x16FFF: return 'Ideographic Symbols and Punctuation'
    if 0x17000 <= ord(c) and ord(c) <= 0x187FF: return 'Tangut'
    if 0x18800 <= ord(c) and ord(c) <= 0x18AFF: return 'Tangut Components'
    if 0x1B000 <= ord(c) and ord(c) <= 0x1B0FF: return 'Kana Supplement'
    if 0x1B100 <= ord(c) and ord(c) <= 0x1B12F: return 'Kana Extended-A'
    if 0x1B170 <= ord(c) and ord(c) <= 0x1B2FF: return 'Nushu'
    if 0x1BC00 <= ord(c) and ord(c) <= 0x1BC9F: return 'Duployan'
    if 0x1BCA0 <= ord(c) and ord(c) <= 0x1BCAF: return 'Shorthand Format Controls'
    if 0x1D000 <= ord(c) and ord(c) <= 0x1D0FF: return 'Byzantine Musical Symbols'
    if 0x1D100 <= ord(c) and ord(c) <= 0x1D1FF: return 'Musical Symbols'
    if 0x1D200 <= ord(c) and ord(c) <= 0x1D24F: return 'Ancient Greek Musical Notation'
    if 0x1D300 <= ord(c) and ord(c) <= 0x1D35F: return 'Tai Xuan Jing Symbols'
    if 0x1D360 <= ord(c) and ord(c) <= 0x1D37F: return 'Counting Rod Numerals'
    if 0x1D400 <= ord(c) and ord(c) <= 0x1D7FF: return 'Mathematical Alphanumeric Symbols'
    if 0x1D800 <= ord(c) and ord(c) <= 0x1DAAF: return 'Sutton SignWriting'
    if 0x1E000 <= ord(c) and ord(c) <= 0x1E02F: return 'Glagolitic Supplement'
    if 0x1E800 <= ord(c) and ord(c) <= 0x1E8DF: return 'Mende Kikakui'
    if 0x1E900 <= ord(c) and ord(c) <= 0x1E95F: return 'Adlam'
    if 0x1EE00 <= ord(c) and ord(c) <= 0x1EEFF: return 'Arabic Mathematical Alphabetic Symbols'
    if 0x1F000 <= ord(c) and ord(c) <= 0x1F02F: return 'Mahjong Tiles'
    if 0x1F030 <= ord(c) and ord(c) <= 0x1F09F: return 'Domino Tiles'
    if 0x1F0A0 <= ord(c) and ord(c) <= 0x1F0FF: return 'Playing Cards'
    if 0x1F100 <= ord(c) and ord(c) <= 0x1F1FF: return 'Enclosed Alphanumeric Supplement'
    if 0x1F200 <= ord(c) and ord(c) <= 0x1F2FF: return 'Enclosed Ideographic Supplement'
    if 0x1F300 <= ord(c) and ord(c) <= 0x1F5FF: return 'Miscellaneous Symbols and Pictographs'
    if 0x1F600 <= ord(c) and ord(c) <= 0x1F64F: return 'Emoticons'
    if 0x1F650 <= ord(c) and ord(c) <= 0x1F67F: return 'Ornamental Dingbats'
    if 0x1F680 <= ord(c) and ord(c) <= 0x1F6FF: return 'Transport and Map Symbols'
    if 0x1F700 <= ord(c) and ord(c) <= 0x1F77F: return 'Alchemical Symbols'
    if 0x1F780 <= ord(c) and ord(c) <= 0x1F7FF: return 'Geometric Shapes Extended'
    if 0x1F800 <= ord(c) and ord(c) <= 0x1F8FF: return 'Supplemental Arrows-C'
    if 0x1F900 <= ord(c) and ord(c) <= 0x1F9FF: return 'Supplemental Symbols and Pictographs'
    if 0x20000 <= ord(c) and ord(c) <= 0x2A6DF: return 'CJK Unified Ideographs Extension B'
    if 0x2A700 <= ord(c) and ord(c) <= 0x2B73F: return 'CJK Unified Ideographs Extension C'
    if 0x2B740 <= ord(c) and ord(c) <= 0x2B81F: return 'CJK Unified Ideographs Extension D'
    if 0x2B820 <= ord(c) and ord(c) <= 0x2CEAF: return 'CJK Unified Ideographs Extension E'
    if 0x2CEB0 <= ord(c) and ord(c) <= 0x2EBEF: return 'CJK Unified Ideographs Extension F'
    if 0x2F800 <= ord(c) and ord(c) <= 0x2FA1F: return 'CJK Compatibility Ideographs Supplement'
    if 0xE0000 <= ord(c) and ord(c) <= 0xE007F: return 'Tags'
    if 0xE0100 <= ord(c) and ord(c) <= 0xE01EF: return 'Variation Selectors Supplement'
    if 0xF0000 <= ord(c) and ord(c) <= 0xFFFFF: return 'Supplementary Private Use Area-A'
    if 0x100000 <= ord(c) and ord(c) <= 0x10FFFF: return 'Supplementary Private Use Area-B'

def topNValues(x, topN, thresh, minPercent):
    '''Given a dictionary containing keys and counts, returns the subset
    of keys that are:
        - are the topN most frequent keys
        - have a frequency in excess of `thresh`
        - account for more than `minPercent` of all values'''
    totalNum = float(sumValues(x))
    sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    if len(sorted_x) > topN:
        sorted_x = sorted_x[:topN]
    z = {}
    for kvp in sorted_x:
        if kvp[1] > thresh and float(kvp[1]) / totalNum > minPercent:
            z[kvp[0]] = kvp[1]
    return z

def normalize(d):
    '''Takes a dictionary of keys to numeric values, and then rescales all the
    values by the L2 norm (i.e. euclidian distance) of the dictionary.'''
    norm = 0.0
    for kvp in d.items():
        norm += kvp[1] * kvp[1]
    norm = math.sqrt(norm)
    n = {}
    for k in d:
        n[k] = d[k] / norm
    return n

def sumValues(x):
    '''Given a dictionary of keys to numbers, returns the sum of all the
    values in the dictionary.'''
    s = 0
    for (k,v) in x.items():
        s += v
    return s

def processStream(inStream, ngramSize):
    singleCharCounts = {}
    ngramCounts = {}
    unicodePlaneCounts = {}

    for line in inStream:
        if line == '':
            continue
        length = len(line)
        for i in range(0, length):
            c = line[i]
            plane = unicodePlane(c)
            if ngramSize > 0:
                if i + ngramSize < length:
                    ngram = line[i:i+ngramSize]
                    if ngram not in ngramCounts:
                        ngramCounts[ngram] = 1
                    else:
                        ngramCounts[ngram] = ngramCounts[ngram] + 1
            if c not in singleCharCounts:
                singleCharCounts[c] = 1
            else:
                singleCharCounts[c] = singleCharCounts[c] + 1
            if plane not in unicodePlaneCounts:
                unicodePlaneCounts[plane] = 1
            else:
                unicodePlaneCounts[plane] = unicodePlaneCounts[plane] + 1

    return (singleCharCounts, ngramCounts, unicodePlaneCounts)

def train(inStream, config):
    '''Processes characters from inStream and returns a dictionary that
    represents the language detection model. The model is defined the `config`
    argument. All keys in the config are optional, but at least one key needs
    to be defined in order to build a model. Config parameters are:
    - ngrams
        - ngramSize         -- size in characters of the ngram
        - maxValues         -- maximum number of ngrams to consider
        - freqThresh        -- consider only ngrams that occur more than this number of times
        - percentThresh     -- consider only ngrams that account for more than this percentage of all ngrams
    - characters
        - maxValues         -- maximum number of characters to consider
        - freqThresh        -- consider only characters that occur more than this number of times
        - percentThresh     -- consider only characters that account for more than this percentage of all ngrams
    - codeplanes
        - maxValues         -- maximum number of unicode codeplanes to consider
        - freqThresh        -- consider only unicode codeplanes that occur more than this number of times
        - percentThresh     -- consider only unicode codeplanes that account for more than this percentage of all ngrams
    '''

    # setup ngram features
    ngramSize = config.get('ngrams', {}).get('ngramSize', 0)
    useNgrams = ngramSize > 0
    maxNgrams = config.get('ngrams', {}).get('maxValues', sys.maxsize)
    threshNgrams = config.get('ngrams', {}).get('freqThresh', 0)
    percentNgrams = config.get('ngrams', {}).get('percentThresh', 0.0)

    # setup single character features
    useSingleChars = 'characters' in config
    maxCharacters = config.get('characters', {}).get('maxValues', sys.maxsize)
    threshCharacters = config.get('characters', {}).get('freqThresh', 0)
    percentCharacters = config.get('characters', {}).get('percentThresh', 0.0)

    # setup codeplane features
    useCodeplanes = 'codeplanes' in config
    maxCodePlanes = config.get('codeplanes', {}).get('maxValues', sys.maxsize)
    threshCodePlanes = config.get('codeplanes', {}).get('freqThresh', 0)
    percentCodePlanes = config.get('codeplanes', {}).get('percentThresh', 0.0)

    (singleCharCounts, ngramCounts, unicodePlaneCounts) = processStream(inStream, ngramSize)

    numNgrams = sumValues(ngramCounts)
    numSingleChars = sumValues(singleCharCounts)
    numCodePlanes = sumValues(unicodePlaneCounts)
    model = {}
    if useNgrams:
        model['ngramSize'] = ngramSize
        model['ngrams'] = normalize(topNValues(ngramCounts, maxNgrams, threshNgrams, percentNgrams))
    if useSingleChars:
        model['singleChars'] = normalize(topNValues(singleCharCounts, maxCharacters, threshCharacters, percentCharacters))
    if useCodeplanes:
        model['unicodePlanes'] = normalize(topNValues(unicodePlaneCounts, maxCodePlanes, threshCodePlanes, percentCodePlanes))

    return model

def classify(inStream, modelMap):
    '''Takes an input stream and a map of language codes to models, and returns
    the language code that best describes the input stream.

    IMPORTANT: All models must have the same ngramSize.
    IMPORTANT: Only ngrams are used. `singleChars` and `unicodePlanes` features
               ignored'''
    ngramSize = list(modelMap.items())[0][1].get('ngramSize', 0)

    (singleCharCounts, ngramCounts, unicodePlaneCounts) = processStream(inStream, ngramSize)
    itemVector = {
        'ngrams': normalize(ngramCounts),
        'singleChars': normalize(singleCharCounts),
        'unicodePlanes': normalize(unicodePlaneCounts),
    }

    bestLang = None
    bestSim = 0.0
    for (lang, model) in modelMap.items():
        sim = 0.0
        for (ngram, score) in model['ngrams'].items():
            try:
                sim += itemVector['ngrams'][ngram] * score
            except KeyError:
                pass
        if sim > bestSim:
            bestSim = sim
            bestLang = lang
    return (bestLang, bestSim)
