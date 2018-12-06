import yaml
import os
import argparse
import logging
import datetime
from source.knn import create_knn
from source.cdp import cdp
from source.utils import log

def main():
    parser = argparse.ArgumentParser(description="CDP")
    parser.add_argument('--config', default='', type=str)
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.load(f)
    for k,v in config.items():
        setattr(args, k, v)

    log_path = "{}/output/log/log-{}{:02d}-{:02d}_{:02d}:{:02d}:{:02d}.txt".format(
        os.path.dirname(args.config), 
        datetime.today().year, datetime.today().month, datetime.today().day,
        datetime.today().hour, datetime.today().minute, datetime.today().second)
    if not os.path.isdir(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path))
    logging.basicConfig(filename=log_path, level=logging.INFO)

    with open(args.config, 'r') as f:
        config_str = f.read()
    log(config_str)

    assert isinstance(args.committee, list), "committee should be a list of strings"

    if args.strategy == "mediator":
        create_knn(args, args.mediator['train_data_name'])
    create_knn(args, args.data_name)
    cdp(args)

if __name__ == "__main__":
    main()
