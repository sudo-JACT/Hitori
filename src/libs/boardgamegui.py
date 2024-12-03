#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

#try:
    
#    from __main__ import g2d
        
#except:
    
#    import libs.g2d

from libs.boardgame import BoardGame
from libs.g2d import *

W, H = 40, 40

class BoardGameGui:
    def __init__(self, game: BoardGame):
        self._game = game
        self.update_buttons()

    def tick(self):
        game = self._game
        x, y = mouse_pos()
        bx, by = x // W, y // H
        released = set(previous_keys()) - set(current_keys())
        if game.finished():
            alert(game.status())
            close_canvas()
        elif "Escape" in released:  # "Escape" key released
            close_canvas()
        elif "LeftButton" in released and by < game.rows():
            game.play(bx, by, "")
            self.update_buttons()
        elif "RightButton" in released and by < game.rows():
            game.play(bx, by, "flag")
            self.update_buttons()

    def update_buttons(self):
        cols, rows = self._game.cols(), self._game.rows()
        clear_canvas()
        set_color((0, 0, 0))
        for y in range(1, rows + 1):
            draw_line((0, y * H), (cols * W, y * H))
        for x in range(1, cols):
            draw_line((x * W, 0), (x * W, rows * H))
        for y in range(rows):
            for x in range(cols):
                _write(self._game.read(x, y), x * W, y * H, W, H)
        status = self._game.status()
        _write(status, 0, rows * H, cols * W, H)

def _write(text, x, y, w, h):
    fsize = 0.75 * min(h, 2 * w / len(text or " "))
    draw_text(text, (x + w // 2, y + h // 2), fsize)

def gui_play(game: BoardGame):
    init_canvas((game.cols() * W, game.rows() * H + H))
    ui = BoardGameGui(game)
    main_loop(ui.tick)
