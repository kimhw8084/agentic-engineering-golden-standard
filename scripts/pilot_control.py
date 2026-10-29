"""Separate-process operator control. No HTTP admin endpoint or model access."""
import argparse
import json
from pathlib import Path
from golden.pilot_control import ControlStore


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['stop','inventory','reconcile','resume'])
    parser.add_argument('--db', type=Path, default=Path('workspace/pilot.sqlite'))
    parser.add_argument('--key-file', type=Path, default=Path('workspace/pilot-operator.key'))
    parser.add_argument('--reason', default='')
    parser.add_argument('--operation')
    parser.add_argument('--epoch', type=int)
    args = parser.parse_args()
    token = args.key_file.read_text(encoding='utf-8').strip()
    store = ControlStore(args.db)
    if args.action == 'stop': store.stop(token,args.reason)
    if args.action == 'reconcile': store.reconcile(token,args.operation,args.reason)
    if args.action == 'resume': store.resume(token,args.epoch,args.reason)
    print(json.dumps(store.inventory(token),indent=2))


if __name__ == '__main__':
    main()
