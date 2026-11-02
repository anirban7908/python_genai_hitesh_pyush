import threading
import time
from datetime import datetime

def take_orders():
    for i in range(1, 4):
        print(f"Taking order for #{i}")
        time.sleep(2)

def brew_chai():
    for i in range(1, 4):
        print(f"Brewing chai for #{i}")
        time.sleep(3)

print(f"start: {datetime.now()}")
# create threads
order_thread = threading.Thread(target=take_orders)
brew_thread = threading.Thread(target=brew_chai)

order_thread.start()
brew_thread.start()

# wait for both to finish
order_thread.join()
brew_thread.join()

print(f"All orders taken and chai brewed:  {datetime.now()}")
# print(f"start: {datetime.now()}")
# take_orders()
# brew_chai()
# print(f"Finished: {datetime.now()}")