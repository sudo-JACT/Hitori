from libs.boardgamegui import gui_play
from game.HitoriGame import *
from rich.console import Console
import subprocess

if __name__ == "__main__":
    
    try:
        import pygame as pg
    except:
        subprocess.call([sys.executable, "-m", "pip", "install", "pygame", "--break-system-packages"])
    import pygame as pg
    
    matrixs = {
        
        0: ((5, 5), "./tables/5-easy.csv"),
        1: ((6, 6), "./tables/6-medium.csv"),
        2: ((8, 8), "./tables/8-hard.csv"),
        3: ((9, 9), "./tables/9-veryhard.csv"),
        4: ((12, 12), "./tables/12-superhard.csv"),
        5: ((15, 15), "./tables/15-impossible.csv"),
        
    }
    
    console = Console()
    
    console.print(f"[bold green]Scegli una difficoltà[/bold green]\n[bold green]0) Easy[/bold green]\n[bold green]1) Medium[/bold green]\n[bold yellow]2) Hard[/bold yellow]\n[bold orange3]3) Very Hard[/bold orange3]\n[bold orange4]4) Super Hard[/bold orange4]\n[bold red]5) Impossible[/bold red]")
    
    s = int(console.input(f"[bold blue]>> [/bold blue]"))
    
    gui_play(HitoriGame(matrixs[s%6][0], matrixs[s%6][1]))