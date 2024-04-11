import bittensor as bt
import requests
 
import time
burn_map = {} 
 
def run_script(): 
    subtensor = bt.subtensor() 
    subnets = subtensor.get_all_subnets_info() 
 
    html = 'dậy đi' 
    for subnet in subnets: 
        burn = float(subnet.burn)
        emission = subnet.emission_value / bt.utils.RAOPERTAO * 100
        if burn_map.get(subnet.netuid) is not None and burn_map[subnet.netuid] != burn and burn < 0.4 and subnet.netuid.isin([5,24,25,26,27,28,29,30,31,32]):
            html += f'Subnet {subnet.netuid} emission {emission:0.2f}%. From {burn_map[subnet.netuid]:0.5f} to {burn:0.5f}\n'
            burn_map[subnet.netuid] = burn 
        elif burn_map.get(subnet.netuid) is None: 
            burn_map[subnet.netuid] = burn 
    if html != '':
        data = { 
            "chat_id": "-4190620407", 
            "text": 'Burn change\n' + html, 
            "parse_mode": "HTML" 
        } 
        requests.post('https://api.telegram.org/bot6882833557:AAHT0H0WeS6Z-VR0vF2PSwwYoWrXgjqfd7Q/sendMessage', json=data) 
 
 
# def main(): 
#     while True: 
#         run_script() 
#         time.sleep(20) 
 
if __name__ == '__main__':
    while True: 
        run_script() 
        time.sleep(2) 