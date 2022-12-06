import os
import threading

if __name__ == "__main__":
    for i in ['A', 'B', 'C']:
        config_name = "config{}.yaml".format(i)
        t = threading.Thread(target=os.system, args=("python main.py {}".format(config_name),))
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

