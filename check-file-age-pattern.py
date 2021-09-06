#!/usr/bin/env python3
import argparse
import datetime
import glob
from itertools import chain
import os
import sys
import time


parser = argparse.ArgumentParser(description="OK if ")
parser.add_argument(
    "files",
    metavar="PathPattern",
    type=str,
    nargs="+",
    help="files pattern (give them between '' if you use *",
)
parser.add_argument(
    "-w", "--warning", dest="warning", type=int, default=86400, help="TODO"
)
parser.add_argument(
    "-c", "--critical", dest="critical", type=int, default=86400 * 2, help="TODO"
)
current_time = time.time()


if __name__ == "__main__":
    try:
        args = parser.parse_args()
        globs = [glob.glob(pattern) for pattern in args.files]
        age_path_tuple_list = [
            (current_time - os.path.getmtime(path), path)
            for path in chain.from_iterable(globs)
        ]
        min_path_age = min(age_path_tuple_list, key=lambda age: age[0])
        # f-string not possible because of compatibility versions
        print(
            "Most recent file is "
            + min_path_age[1]
            + " modified "
            + str(datetime.timedelta(seconds=int(min_path_age[0])))
            + " ago."
        )
        if not age_path_tuple_list:
            print("No file found in specified path(s)")
            sys.exit(3)
        if min_path_age[0] > args.critical:
            sys.exit(2)
        if min_path_age[0] > args.warning:
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(3)
