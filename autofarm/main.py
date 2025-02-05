import gui_enter
import mylib.process_manager as pm
import mylib.func as func

if __name__ == "__main__":
    print("start")
    scr_process = pm.create_process(func.scr_process)
    gui_enter.gui_enter()













