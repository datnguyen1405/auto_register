import os
import time
import subprocess
import datetime
import os
import re

def get_last_prediction_time(log_file):
    last_prediction_time = None
    with open(log_file, 'r') as file:
        for line in file:
            # if "Amount of texts recieved" in line:
            if "Amount of texts recieved" in line:
                timestamp_str = line.split("|")[0].strip()
                clean_timestamp_str = re.sub(r'\x1b\[\d+m', '', timestamp_str)
                last_prediction_time = datetime.datetime.strptime(clean_timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    return last_prediction_time


def restart_process_if_needed(log_file, process_name):
    last_prediction_time = get_last_prediction_time(log_file)
    if last_prediction_time:
        current_datetime = datetime.datetime.now()
        minutes_from_last_predict=(current_datetime - last_prediction_time).total_seconds() / 60
        print(f'NOW IS: {current_datetime} & LAST REQUEST IS: {last_prediction_time}. Minutes from the last request: {minutes_from_last_predict}')
        if minutes_from_last_predict > 10:  # 10 minutes in seconds
            # Restart process
             os.system(f"pm2 restart {process_name}")
        else:
            print("Still get request")
    else:
        print("Do not get last request time")


if __name__ == "__main__":
    while True:
        # os.system('pwd')
        os.chdir("/root/.pm2/logs")
        list_process_to_check = ["hk1","hk2","hk3"]  # Add more log files if needed
        for pre_process_name in list_process_to_check:
            process_name = pre_process_name +"_new_trick"
            # os.system(f"pm2 log {process_name}")
            process_log_file = pre_process_name + "-new-trick" + "-out.log"
            print(f"Process log file: {process_log_file}")
            restart_process_if_needed(process_log_file, process_name)
        time.sleep(60)