"""
Module for colors functionalities.

All colors in collection are divided into 64 groups* by splitting up RGB values into 4 ranges: 
{
    "0-63": 0, 
    "64-127": 64, 
    "128-191": 128, 
    "192-255": 192
}

*4 ranges x 3 (R, G, B) = 64 color groups
"""

import math
import colorsys
import re

from unsigned_bot.utility.files_util import load_json
from unsigned_bot import ROOT_DIR

# calculations based on pixel count
TOTAL_PIXELS = 16384

# cumulative pixel amount in entire collection
PIXELS_COLORS = {
    (0, 0, 0): 30733152,
    (0, 0, 64): 11027495,
    (0, 0, 128): 6924735,
    (0, 0, 192): 27156755,
    (0, 64, 0): 11013810,
    (0, 64, 64): 8847167,
    (0, 64, 128): 6338027,
    (0, 64, 192): 8507705,
    (0, 128, 0): 6936964,
    (0, 128, 64): 6342332,
    (0, 128, 128): 4134258,
    (0, 128, 192): 4638028,
    (0, 192, 0): 27125076,
    (0, 192, 64): 8499094,
    (0, 192, 128): 4639235,
    (0, 192, 192): 18066128,
    (64, 0, 0): 10981883,
    (64, 0, 64): 8836531,
    (64, 0, 128): 6341185,
    (64, 0, 192): 8571245,
    (64, 64, 0): 8819809,
    (64, 64, 64): 9795114,
    (64, 64, 128): 7142948,
    (64, 64, 192): 6149683,
    (64, 128, 0): 6348108,
    (64, 128, 64): 7150363,
    (64, 128, 128): 4864719,
    (64, 128, 192): 4063175,
    (64, 192, 0): 8559726,
    (64, 192, 64): 6145819,
    (64, 192, 128): 4056261,
    (64, 192, 192): 5443380,
    (128, 0, 0): 6957201,
    (128, 0, 64): 6344203,
    (128, 0, 128): 4157997,
    (128, 0, 192): 4661192,
    (128, 64, 0): 6351863,
    (128, 64, 64): 7138033,
    (128, 64, 128): 4878471,
    (128, 64, 192): 4062180,
    (128, 128, 0): 4162628,
    (128, 128, 64): 4872188,
    (128, 128, 128): 3088013,
    (128, 128, 192): 2440186,
    (128, 192, 0): 4672436,
    (128, 192, 64): 4055608,
    (128, 192, 128): 2444511,
    (128, 192, 192): 2704459,
    (192, 0, 0): 27031542,
    (192, 0, 64): 8478252,
    (192, 0, 128): 4657920,
    (192, 0, 192): 18163490,
    (192, 64, 0): 8531671,
    (192, 64, 64): 6121071,
    (192, 64, 128): 4056579,
    (192, 64, 192): 5422424,
    (192, 128, 0): 4662234,
    (192, 128, 64): 4052847,
    (192, 128, 128): 2443360,
    (192, 128, 192): 2731807,
    (192, 192, 0): 18196368,
    (192, 192, 64): 5411563,
    (192, 192, 128): 2741118,
    (192, 192, 192): 9960371
}

# shares of colors related to cumulative pixel amounts
PIXEL_PERCENTAGES = {
    (0, 0, 0): 0.060278374445676276,
    (0, 0, 64): 0.02162874386616195,
    (0, 0, 128): 0.013581807985952111,
    (0, 0, 192): 0.05326381903878559,
    (0, 64, 0): 0.021601902832925624,
    (0, 64, 64): 0.017352364157422917,
    (0, 64, 128): 0.01243107002994051,
    (0, 64, 192): 0.016686561393486496,
    (0, 128, 0): 0.013605793298005238,
    (0, 128, 64): 0.012439513628631223,
    (0, 128, 128): 0.008108714386960137,
    (0, 128, 192): 0.00909678214826553,
    (0, 192, 0): 0.05320168552823436,
    (0, 192, 64): 0.016669672234758105,
    (0, 192, 128): 0.009099149494054075,
    (0, 192, 192): 0.0354339453489026,
    (64, 0, 0): 0.021539282908326705,
    (64, 0, 64): 0.017331503271087397,
    (64, 0, 128): 0.012437263963660666,
    (64, 0, 192): 0.016811185379736856,
    (64, 64, 0): 0.017298705627113862,
    (64, 64, 64): 0.01921161713026005,
    (64, 64, 128): 0.014009799391549374,
    (64, 64, 192): 0.012061662096885143,
    (64, 128, 0): 0.01245084236870963,
    (64, 128, 64): 0.01402434277930585,
    (64, 128, 128): 0.00954140185344464,
    (64, 128, 192): 0.00796929596054159,
    (64, 192, 0): 0.016788592624029933,
    (64, 192, 64): 0.01205408345220665,
    (64, 192, 128): 0.007955735207615323,
    (64, 192, 192): 0.010676356850416948,
    (128, 0, 0): 0.013645485076565964,
    (128, 0, 64): 0.012443183308805512,
    (128, 0, 128): 0.008155274802597489,
    (128, 0, 192): 0.009142214789397153,
    (128, 64, 0): 0.012458207226568777,
    (128, 64, 64): 0.014000159371209108,
    (128, 64, 128): 0.009568374296927721,
    (128, 64, 192): 0.007967344420309939,
    (128, 128, 0): 0.008164357800399273,
    (128, 128, 64): 0.009556051153937305,
    (128, 128, 128): 0.006056664930011608,
    (128, 128, 192): 0.004786051408755503,
    (128, 192, 0): 0.009164268174688293,
    (128, 192, 64): 0.00795445444804621,
    (128, 192, 128): 0.004794534234385544,
    (128, 192, 192): 0.005304382455628997,
    (192, 0, 0): 0.05301823290107129,
    (192, 0, 64): 0.016628793841282657,
    (192, 0, 128): 0.00913579726212282,
    (192, 0, 192): 0.03562490601225336,
    (192, 64, 0): 0.01673356703488524,
    (192, 64, 64): 0.012005544037480116,
    (192, 64, 128): 0.007956358915950664,
    (192, 64, 192): 0.01063525486338732,
    (192, 128, 0): 0.009144258512936229,
    (192, 128, 64): 0.00794903916907175,
    (192, 128, 128): 0.004792276724027122,
    (192, 128, 192): 0.005358021372468388,
    (192, 192, 0): 0.03568939117781741,
    (192, 192, 64): 0.010613952673984342,
    (192, 192, 128): 0.005376283474073315,
    (192, 192, 192): 0.019535743445900214
}

# shares normalized to most occuring color (0, 0, 0)
PERCENTAGES_NORMALIZED = {
    (0, 0, 0): 1.0,
    (0, 0, 64): 0.35881431881767284,
    (0, 0, 128): 0.22531808647547769,
    (0, 0, 192): 0.8836306474519763,
    (0, 64, 0): 0.35836903419473537,
    (0, 64, 64): 0.28787047290170564,
    (0, 64, 128): 0.20622769184234666,
    (0, 64, 192): 0.276825006429539,
    (0, 128, 0): 0.22571599554773947,
    (0, 128, 64): 0.20636776859073877,
    (0, 128, 128): 0.13452111908339243,
    (0, 128, 192): 0.15091286438826712,
    (0, 192, 0): 0.8825998713050974,
    (0, 192, 64): 0.2765448203946019,
    (0, 192, 128): 0.15095213793886159,
    (0, 192, 192): 0.5878384358363242,
    (64, 0, 0): 0.3573301885859283,
    (64, 0, 64): 0.28752439710707184,
    (64, 0, 128): 0.20633044732932046,
    (64, 0, 192): 0.278892480667131,
    (64, 64, 0): 0.28698029411366593,
    (64, 64, 64): 0.3187149173635037,
    (64, 64, 128): 0.23241833444223356,
    (64, 64, 192): 0.2000993259656543,
    (64, 128, 0): 0.2065557089621006,
    (64, 128, 64): 0.2326596048462585,
    (64, 128, 128): 0.15828897081561955,
    (64, 128, 192): 0.13220820955819956,
    (64, 192, 0): 0.27851767368345426,
    (64, 192, 64): 0.19997359854270724,
    (64, 192, 128): 0.13198324076879583,
    (64, 192, 192): 0.17711753093206972,
    (128, 0, 0): 0.22637447014871756,
    (128, 0, 64): 0.20642864747488315,
    (128, 0, 128): 0.13529354229595456,
    (128, 0, 192): 0.15166657816289067,
    (128, 64, 0): 0.20667788972637757,
    (128, 64, 64): 0.23225840942055015,
    (128, 64, 128): 0.1587364354948038,
    (128, 64, 192): 0.13217583409602762,
    (128, 128, 0): 0.13544422648220397,
    (128, 128, 64): 0.15853199827990308,
    (128, 128, 128): 0.10047823926423166,
    (128, 128, 192): 0.07939914526176814,
    (128, 192, 0): 0.1520324371545099,
    (128, 192, 64): 0.13196199335492825,
    (128, 192, 128): 0.07953987277321897,
    (128, 192, 192): 0.08799810055278418,
    (192, 0, 0): 0.8795564477083249,
    (192, 0, 64): 0.2758666602110971,
    (192, 0, 128): 0.15156011332648212,
    (192, 0, 192): 0.5910064154825382,
    (192, 64, 0): 0.27760481580281776,
    (192, 64, 64): 0.19916834433383207,
    (192, 64, 128): 0.13199358790142968,
    (192, 64, 192): 0.17643566139913017,
    (192, 128, 0): 0.1517004829182506,
    (192, 128, 64): 0.1318721555146703,
    (192, 128, 128): 0.07950242135918893,
    (192, 128, 192): 0.08888795395929451,
    (192, 192, 0): 0.592076204874788,
    (192, 192, 64): 0.17608226452008566,
    (192, 192, 128): 0.08919091670128726,
    (192, 192, 192): 0.3240920749033487
}

# ranking based on normalized percentages
COLOR_RANKING = {
    (0, 0, 0): 64,
    (0, 0, 64): 57,
    (0, 0, 128): 38,
    (0, 0, 192): 63,
    (0, 64, 0): 56,
    (0, 64, 64): 52,
    (0, 64, 128): 32,
    (0, 64, 192): 46,
    (0, 128, 0): 39,
    (0, 128, 64): 34,
    (0, 128, 128): 14,
    (0, 128, 192): 17,
    (0, 192, 0): 62,
    (0, 192, 64): 45,
    (0, 192, 128): 18,
    (0, 192, 192): 58,
    (64, 0, 0): 55,
    (64, 0, 64): 51,
    (64, 0, 128): 33,
    (64, 0, 192): 49,
    (64, 64, 0): 50,
    (64, 64, 64): 53,
    (64, 64, 128): 42,
    (64, 64, 192): 31,
    (64, 128, 0): 36,
    (64, 128, 64): 43,
    (64, 128, 128): 23,
    (64, 128, 192): 13,
    (64, 192, 0): 48,
    (64, 192, 64): 30,
    (64, 192, 128): 10,
    (64, 192, 192): 28,
    (128, 0, 0): 40,
    (128, 0, 64): 35,
    (128, 0, 128): 15,
    (128, 0, 192): 20,
    (128, 64, 0): 37,
    (128, 64, 64): 41,
    (128, 64, 128): 25,
    (128, 64, 192): 12,
    (128, 128, 0): 16,
    (128, 128, 64): 24,
    (128, 128, 128): 7,
    (128, 128, 192): 1,
    (128, 192, 0): 22,
    (128, 192, 64): 9,
    (128, 192, 128): 3,
    (128, 192, 192): 4,
    (192, 0, 0): 61,
    (192, 0, 64): 44,
    (192, 0, 128): 19,
    (192, 0, 192): 59,
    (192, 64, 0): 47,
    (192, 64, 64): 29,
    (192, 64, 128): 11,
    (192, 64, 192): 27,
    (192, 128, 0): 21,
    (192, 128, 64): 8,
    (192, 128, 128): 2,
    (192, 128, 192): 5,
    (192, 192, 0): 60,
    (192, 192, 64): 26,
    (192, 192, 128): 6,
    (192, 192, 192): 54
}


red = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192]
green = [0,0,0,0,64,64,64,64,128,128,128,128,192,192,192,192,0,0,0,0,64,64,64,64,128,128,128,128,192,192,192,192,0,0,0,0,64,64,64,64,128,128,128,128,192,192,192,192,0,0,0,0,64,64,64,64,128,128,128,128,192,192,192,192]
blue = [0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192,0,64,128,192]

COLOR_KEYS = list(zip(red, green, blue)) 
COLOR_HEX_URL = "https://www.color-hex.com"


def step(r: int, g: int, b: int, repetitions=1) -> tuple:
    """
    Helper function to generate step sorted color diagram.
    Credits go to: https://www.alanzucconi.com/2015/09/30/colour-sorting/
    """

    lum = math.sqrt( .241 * r + .691 * g + .068 * b ) # weighting by luminosity
    h, s, v = colorsys.rgb_to_hsv(r,g,b)
    h2 = int(h * repetitions)
    v2 = int(v * repetitions)
    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum = repetitions - lum

    return (h2, lum, v2)

# calculate step sorted colours upfront
COLORS_SORTED = sorted(COLOR_KEYS, key=lambda rgb: step(rgb[0],rgb[1],rgb[2],8))


def rgb_2_hex(rgb: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def get_color_frequencies(idx: str) -> dict:
    """Load color frequency data from file and convert tuple strings to tuples"""
    unsigs_colors = load_json(f"{ROOT_DIR}/data/json/color_frequencies.json")
    color_frequencies = unsigs_colors.get(str(idx))
    return {tuple([int(n) for n in re.findall('[0-9]+', k)]): v for k,v in color_frequencies.items()}

def get_total_colors(color_frequencies: dict) -> int:
    """Count total amount of colors"""
    return len([p for p in color_frequencies.values() if p])

def get_top_colors(color_frequencies: dict, num_ranks=10) -> dict:
    """Return ranking of colors which occur most often in an unsig"""
    colors_sorted = sorted(color_frequencies.items(), key=lambda x: x[1], reverse=True)
    return {k: v/TOTAL_PIXELS for k,v in dict(colors_sorted[:num_ranks]).items() if v != 0}

def link_hex_color(color_hex: str) -> str:
    color_hex = color_hex.replace("#", "")
    return f"{COLOR_HEX_URL}/color/{color_hex}"

def calc_pixel_percentages(color_frequencies: dict) -> dict:
    return {k: v/TOTAL_PIXELS for k, v in color_frequencies.items()}

def get_max_percentage(percentages: dict) -> float:
    return max(percentages.values())

def calc_color_rarity(color_frequencies: dict) -> float:
    """
    Return rarity value normalized to 64.
    Value ascending from 0 (most rare) to 64 (most common).
    """
    percentages = calc_pixel_percentages(color_frequencies)
    weighted_rarity = [PERCENTAGES_NORMALIZED.get(k) * v * 64 for k,v in percentages.items()]
    return sum(weighted_rarity)