# app.py
from config import gui, my_theme, my_stylekit

name = "Energy WOM"
if __name__ == "__main__":
    
    gui.run(run_browser=False, title=name,use_reloader=True, light_theme=True, host="0.0.0.0", port=5001, theme=my_theme, stylekit=my_stylekit, dark_mode=False)