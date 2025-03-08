import core.recongnize_process as rp
import core.main_enter

#基于opencv的图像识别，需要下载电脑模拟器并且将其置于屏幕才可以使用

def main():
    rp.recongnize_process()
    core.main_enter.main_enter()

if __name__ == "__main__":
    main()