import time
import core.gui_tools as gt
import core.recongnize_process as rp

def eat_bread():
    time.sleep(0.8)
    rp.operate("confirm", "c", try_times=6)
    time.sleep(1)
    rp.operate("bag_enter", "c", try_times=6)
    time.sleep(1)
    rp.operate("item_can_use", "c", try_times=6)
    time.sleep(1)
    if rp.operate("bread", "c", try_times=6):
        time.sleep(1)
        rp.operate("use", "c", try_times=6)
        time.sleep(1)
        rp.operate("confirm2", "c", try_times=6)
        time.sleep(1)
        rp.operate("get_item", "c", try_times=6)
        time.sleep(1)
        rp.operate("return", "c", try_times=6)
        time.sleep(1)
        return 1
    else:
        gt.show_message("你没有面包了", join=True)
        return 0
