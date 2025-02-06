'''
    Tile loader from the PYR_PG Project
    Copyright (C) 2024-2025 Spyro24

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import pygame as p

def load_tiles(folder, config, *font, mode="new"):
    '''
        To use the font you have to make a Text obj from the pyr_pg libary
        The modes are "new" for tile tables and "legacy" if you have
    '''
    tmp = config["size"].split("x")
    tmx = int(tmp[0])
    tmy = int(tmp[1])
    draw_font = False
    tile_maps = []
    tiles = []
    if len(font) > 0:
        draw_font = True
    try:
        n = 0
        if mode == "new":
            while True:
                if draw_font:
                    pass # ("Loading Tilemap str(n))
                    p.display.flip()
                tile_maps.append(p.image.load(folder + "/" + str(n) + ".png"))
                n += 1
        elif mode == "single":
            tile_maps.append(p.image.load(folder))
    
    except:
        pass
    
    max_tile_maps = len(tile_maps)
    
    for tmap in range(max_tile_maps):
        cur_tmap = tile_maps[tmap]
        tw, th = cur_tmap.get_size()
        sx, sy = tw / tmx, th / tmy
        for h in range(tmy):
            for w in range(tmx):
                tmp = p.Surface((sy, sy), flags=p.SRCALPHA)
                tmp.blit(cur_tmap,(0,0),(sx * w, sy * h, sx, sy))
                tiles.append(tmp)
    
    return tiles