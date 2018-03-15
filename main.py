import os
import json
import requests
from datetime import datetime


def load_envvars():
    folder = __file__.split('/')[0]

    with open(os.path.join(folder, 'config.json'), 'rb') as f:
        env_vars = json.loads(f.read())

    for k, v in env_vars.iteritems():
        os.environ[str(k)] = str(v)


def main():
    load_envvars()

    CUSTOM_PANEL_URL = os.getenv('CUSTOM_PANEL_URL')
    ETHOS_MINERNAME = os.getenv('ETHOS_MINERNAME')
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
    SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

    response = requests.get(CUSTOM_PANEL_URL)
    if response.status_code != 200:
        return

    rig_status = response.json()['rigs'][ETHOS_MINERNAME]
    rig_hashrates = rig_status['miner_hashes'].split(' ')

    is_gpu_crashed = [int(float(hash_rate)) == 0 for hash_rate in rig_hashrates]

    if any(is_gpu_crashed):
        slack_payload = {'channel': slack_channel, 'text': 'Rig: {} restarted'.format(ETHOS_MINERNAME)}
        requests.post(SLACK_WEBHOOK_URL, json=slack_payload)
        os.system("r")


main()
