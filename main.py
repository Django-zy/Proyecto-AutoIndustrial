from taipy.gui import Gui,navigate
from pages.form_page import form_page_md
from pages.download_files import download_md
import taipy.gui.builder as tgb

advanced_properties = {
    "alpha_matting_foreground_threshold": 240,
    "alpha_matting_background_threshold": 10,
    "alpha_matting_erode_size": 10,
}


pages = {
    "/": "<|menu|lov={page_names}|class_name=custom-nav-button|on_action=menu_action|>",
    "form_page": form_page_md
    #"download_files" : download_md
}
page_names = [page for page in pages.keys() if page != "/"]

def menu_action(state, action, payload):
    page = payload["args"][0]
    navigate(state, page)



gui = Gui(pages=pages)
gui.run(run_browser=False, use_reloader=True, light_theme=True, host="0.0.0.0", port=5000)

