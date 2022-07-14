from new_inventory import main
import schedule
import time



if __name__ == "__main__":
    schedule.every(30).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

