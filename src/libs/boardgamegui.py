#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

    
from libs.boardgame import BoardGame
from libs.g2d import *

W, H = 40, 40
BLACK, GRAY, WHITE, RED = (0, 0, 0), (127, 127, 127), (255, 255, 255), (255, 0, 0)

class BoardGameGui:
    def __init__(self, game: BoardGame,
                 actions={"LeftButton": "", "RightButton": "flag"},
                 annots={"#": (0, GRAY), "!": (2, GRAY)}):
        self._game = game
        self._actions = actions
        self._annots = annots
        self.update_buttons()

    def tick(self):
        game = self._game
        mouse_x, mouse_y = mouse_pos()
        x, y = mouse_x // W, mouse_y // H
        released = set(previous_keys()) - set(current_keys())
        
        print(game.finished())
        
        if game.finished():
            
            clear_canvas((255, 255, 255))
            
            draw_text("YOU WON", ((mouse_x), (mouse_y)), 50)
            
            if "Escape" in released:  # "Escape" key released
                close_canvas()
                return
        
        else:
            
            
            if "Escape" in released:  # "Escape" key released
                close_canvas()
                return
            for k, v in self._actions.items():
                if k in released and y < game.rows():
                    game.play(x, y, v)
                    self.update_buttons((x, y))

    def update_buttons(self, last_move=None):
        cols, rows = self._game.cols(), self._game.rows()
        clear_canvas(BLACK)
        for y in range(rows):
            for x in range(cols):
                text = self._game.read(x, y)
                self.write(text, (x, y))
        status = self._game.status()
        self.write(status, (0, rows), cols)
        
    def write(self, text, pos, cols=1):
        x, y = pos        
        set_color(WHITE)
        draw_rect((x * W + 1, y * H + 1), (cols * W - 2, H - 2))
        
        last = text[-1:]
        if cols == 1 and last in self._annots:
            stroke, color = self._annots[last]
            set_stroke(stroke)
            set_color(color)
            draw_circle((x * W + W / 2, y * H + W / 2), min(W, H) / 2 - 2)
            set_stroke()
            text = text[:-1]
        
        chars = max(1, len(text))
        fsize = min(0.75 * H, 1.5 * cols * W / chars)
        center = (x * W + cols * W/2, y * H + H/2)
        set_color(BLACK)
        draw_text(text, center, fsize)

def gui_play(game: BoardGame):
    init_canvas((game.cols() * W, game.rows() * H + H))
    ui = BoardGameGui(game)
    main_loop(ui.tick)

