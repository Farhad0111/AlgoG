# levels.py
# All maps use a 25x25 grid (25 rows, exactly 25 chars per row).
# Legend:
#   '.' = empty passable cell
#   'W' = wall (impassable)
#   'S' = start node (player begins here)
#   'E' = end node   (player must reach here)

# ---------------------------------------------------------------------------
# Maps dictionary â€” add or edit levels here without touching load_level()
# ---------------------------------------------------------------------------

MAPS = {
    "Easy": [
        # Simple open field with one vertical wall barrier.
        ".........................",
        ".........................",
        "..S......................",
        ".........................",
        ".........................",
        "..........W..............",
        "..........W..............",
        "..........W..............",
        "..........W..............",
        "..........W..............",
        "..........W..............",
        "..........W..............",
        "..........W..............",
        "..........W..............",
        "..........W..............",
        ".........................",
        ".........................",
        ".........................",
        ".........................",
        ".........................",
        ".........................",
        ".........................",
        ".....................E...",
        ".........................",
        ".........................",
    ],

    "Medium": [
        # Two crossing walls create a bottleneck.
        ".........................",
        ".........................",
        "..S......................",
        "........WWWWWWWWWWWWWWWW.",
        "........W................",
        "........W................",
        "........W................",
        "........W................",
        "........W................",
        "........W................",
        "........W................",
        "........WWWWWWWWWWWWWWWW.",
        ".........................",
        ".WWWWWWWWWWWWWWWW........",
        ".W.......................",
        ".W.......................",
        ".W.......................",
        ".WWWWWWWWWWWWWWWW........",
        ".........................",
        ".........................",
        ".........................",
        ".........................",
        ".....................E...",
        ".........................",
        ".........................",
    ],

    "Hard": [
        # Organic corridors â€” all regions connected, no isolated pockets.
        "......W..................",  # row 0  open top row
        "....W.W..................",  # row 1  double-wall column starts
        "....W.W..............E...",  # row 2  E at col 21
        "....W.W...........W......",  # row 3
        "....W.W...........WW.....",  # row 4
        "....W.W........WWW.......",  # row 5
        "..S.W.WWWW...WWW.........",  # row 6  S at col 2
        "....W.......W............",  # row 7
        ".........................",  # row 8
        "............WWWW.........",  # row 9  walls cols 12-15
        ".......WWWW....W.........",  # row 10 walls cols 7-10, col 15
        ".......W.......W.........",  # row 11 FIXED: removed col 10 wall & orphan WWW â€” pocket now open
        ".......W.......W.........",  # row 12 FIXED: removed col 10 wall
        "....WW.W.......W.........",  # row 13 FIXED: removed col 10 wall
        "...WW..WWWWWWWWW.........",  # row 14 extended wall rightward to seal properly
        "...W...........WWWWWW....",  # row 15 walls cols 15-20
        "....WW...................",  # row 16
        ".....WW........W.........",  # row 17
        "...WW.......W..WW........",  # row 18
        "...W........W...WW.......",  # row 19
        "............W............",  # row 20
        "...........WW............",  # row 21
        "...........W.............",  # row 22
        ".........................",  # row 23
        ".........................",  # row 24
    ],


    "Spiral": [
        # 3 routes: Gap-A top (row1 col12-13), Gap-B right (row12), Gap-C bottom (row23 col12-13)
        ".........................",
        ".WWWWWWWWWWWW..WWWWWWWWWW",
        ".W..........W.W........W.",
        ".W.WWWWWWWW.W.W.WWWWWWW..",
        ".W.W......W.W.W.W.....W..",
        ".W.W.WWWW.W.W.W.W.WWW.W..",
        ".W.W.W..W.W.W.W.W.W.W.W..",
        ".W.W.W.WW.W.W.W.W.W.W.W..",
        ".W.W.W....W.W.W.W.W...W..",
        ".W.W.WWWWWW.W.W.W.WWWWW..",
        ".W.W........W.W.W.......W",
        ".W.WWWWWWWWWW.W.WWWWWWWWW",
        "S...........W.W........W.",
        ".W.WWWWWWWWWW.WWWWWWWWW.W",
        ".W..........W...........W",
        "WWWWWWWW.WWWWWWWWWWWWWWWW",
        ".W...................W...",
        ".W.WWWWWWWWWWWW.WWWWWWW.W",
        ".W...................W.W.",
        ".W.W.WWWWWWWWWW.WWWWW.W.W",
        ".W.W.W.............E.W.W.",
        ".W.W.WWWWWWWWWWWWWWWW.W..",
        ".W.WWWWWWWWWWWWWWWWWWWW..",
        ".WWWWWWWWWWWW..WWWWWWWWWW",
        ".........................",
    ],





    "Maze": [
        # Classic recursive-style maze with a single solution path.
        "S.WWWWW...WWWWW...WWWWWW.",
        "..W...W...W...W...W....W.",
        "W.W.W.W.W.W.W.W.W.W.W.W.W",
        "W...W...W...W...W...W....",
        "WWWWW.WWW.WWW.WWW.WWW.WWW",
        "......W...W...W...W......",
        ".WWWWWW.W.W.W.WWWWWWWWWW.",
        ".W......W.W.W..........W.",
        ".W.WWWWWW.W.WWWWWWWWWW.W.",
        ".W........W..........W.W.",
        ".WWWWWWWWWWWWWWWWWWW.W.W.",
        "...................W.W.W.",
        "WWWWWWWWWWWWWWWWWW.W.W.W.",
        "W................W.W.W.W.",
        "W.WWWWWWWWWWWWWW.W.W.W.W.",
        "W.W............W.W.W.W.W.",
        "W.W.WWWWWWWWWW.W.W.W.W.W.",
        "W.W.W..........W.W.W.W.W.",
        "W.W.W.WWWWWWWW.W.W.W.W.W.",
        "W.W.W.W........W.W.W.W.W.",
        "W.W.W.W.WWWWWWWW.W.W.W.W.",
        "W.W.W.W........W.W.W.W.W.",
        "W.W.W.WWWWWWWWWW.W.W.W.W.",
        "W.W..............W...W.E.",
        "W.WWWWWWWWWWWWWWWWWWWWWWW",
    ],

    "Blocks": [
        # Fix #13: grid of evenly spaced wall-blocks; multiple routes, no dead ends.
        ".........................",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".........................",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".........................",
        "..S.......................",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".........................",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".........................",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".........................",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".WWW..WWW..WWW..WWW..WWW.",
        ".....................E...",
        ".........................",
    ],

}


# ---------------------------------------------------------------------------
# Parser â€” reads any entry from MAPS and converts to node coords
# ---------------------------------------------------------------------------

def parse_string_map(map_layout, rows):
    walls = []
    start = None
    end = None

    for r, row_str in enumerate(map_layout):
        if r >= rows:
            break
        for c, char in enumerate(row_str):
            if c >= rows:
                break
            if char == 'S':
                start = (r, c)
            elif char == 'E':
                end = (r, c)
            elif char == 'W':
                walls.append((r, c))

    if not start:
        start = (1, 1)
    if not end:
        end = (rows - 2, rows - 2)
    return start, end, walls


# ---------------------------------------------------------------------------
# Public API â€” called by main.py
# ---------------------------------------------------------------------------

def load_level(level_name, rows):
    if level_name in MAPS:
        return parse_string_map(MAPS[level_name], rows)

    # Fallback empty level
    return (1, 1), (rows - 2, rows - 2), []
