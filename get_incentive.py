import bittensor as bt
import requests
import time
from io import StringIO
from prettytable import PrettyTable
import pandas as pd

burn_map = {}
my_netuids = [3, 5, 7, 11, 20, 24, 26, 27, 28, 29, 30, 31, 32]
cold_keys = [
    '5DwAELY8mf1Sb6ZFqcumDCvxKcLakqHrVf2tPaGzQVxA1jzS',
    '5Hj9CS67VpVLL4prMRGGXSBB4uY8ZBHPriMyPveUoxdSX9ZR',
]
tele_chat_id = "-4206695854"
tele_report_token = "6882833557:AAHT0H0WeS6Z-VR0vF2PSwwYoWrXgjqfd7Q"
reward_map = {}

hotkeys = {
            # "5FWr1PnUHszMLcYBxMFaV73ZFyBy4vZqnUgRNakuEBaEWS39",
            # "5EuzFvNmxt8Z7XCVbmKWzbUYKJkgZawVTVeyacj6tZQf3y1H",
            # "5FCZ4FbxNwzHfmvjVwqunfJ5wKGw6Ds3r7dPJoyXJVsf5Snm"
        }

def get_subnet_reward(netuid, cold_keys, rewards):
    x = PrettyTable()
    x.field_names = ["HOT", "INCENTIVE", "REWARDS", "RANK"]
    url = 'https://taostats.io/wp-admin/admin-ajax.php'
    data = {
        'action': 'metagraph_table',
        'this_netuid': netuid
    }

    response = requests.post(url, data=data)

    tables = pd.read_html(StringIO(response.text))
    df = tables[0].sort_values(by='INCENTIVE', ascending=True)
    incentives = df['INCENTIVE']

    has_change = False
    df = df[df['COLDKEY'].isin(cold_keys)]
    if df.empty:
        return '', has_change

    incentives = incentives[incentives > 0]

    for index, row in df.iterrows():
        key = f'{netuid}_{row["UID"]}'
        arrow = ''
        if key in reward_map:
            if reward_map[key] > row['DAILY REWARDS']:
                arrow = '↓'
                has_change = True
            elif reward_map[key] < row['DAILY REWARDS']:
                arrow = '↑'
                has_change = True
        else:
            has_change = True

        reward_map[key] = row['DAILY REWARDS']
        hot_name = hotkeys.get(row['HOTKEY'], '')
        x.add_row([hot_name, row['INCENTIVE'],
                   '{0:.3f}'.format(row['DAILY REWARDS']) + arrow,
                   incentives[incentives < row['INCENTIVE']].count() + 1])
        rewards.append(row['DAILY REWARDS'])

    return x.get_string(), has_change

def send_report():
    text = ''
    rewards = []
    need_send = False
    for netuid in my_netuids:
        string, has_change = get_subnet_reward(netuid, cold_keys, rewards)
        if has_change:
            need_send = True
        if string != '':
            text += f'\nNetuid: {netuid} <pre>{string}</pre>'
    text += f'\nTotal: {sum(rewards)}'

    if not need_send:
        return

    data = {
        "chat_id": tele_chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    requests.post(
        f'https://api.telegram.org/bot{tele_report_token}/sendMessage',
        json=data)


def main():
    while True:
        send_report()
        print("DONEEEEE")
        time.sleep(1)
  


if __name__ == "__main__":
    main()
