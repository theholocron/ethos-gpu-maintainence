import os
import json
import requests


def load_envvars():
    folder = __file__.split('/')[0]

    with open(os.path.join(folder, 'config.json'), 'rb') as f:
        env_vars = json.loads(f.read())

    for k, v in env_vars.iteritems():
        os.environ[str(k)] = str(v)


def main():
    load_envvars()
    import ipdb; ipdb.set_trace()

    CUSTOM_PANEL_URL = os.getenv('CUSTOM_PANEL_URL')
    ETHOS_MINERNAME = os.getenv('ETHOS_MINERNAME')

    response = requests.get(CUSTOM_PANEL_URL)
    if response.status_code != 200:
        return

    rig_status = response.json()['rigs'][ETHOS_MINERNAME]
    rig_hashrates = rig_status['miner_hashes'].split(' ')

    is_gpu_crashed = [int(float(hash_rate)) == 0 for hash_rate in rig_hashrates]

    if any(is_gpu_crashed):
        os.system("r")


main()
