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
    "-w",
    "--warning",
    dest="warning",
    type=int,
    default=86400,
    help="minimum modification time in seconds to raise a warning",
)
parser.add_argument(
    "-c",
    "--critical",
    dest="critical",
    type=int,
    default=86400 * 2,
    help="minimum modification time in seconds to raise a critical",
)

parser.add_argument(
    "-a",
    "--all",
    dest="all",
    action="store_true",
    help="All files found must match minimal modification time",
)

current_time = time.time()


def check_all(age_path_tuple_list):
    # Need to check for a critical then we can test warnings.
    for age, path in age_path_tuple_list:
        if age > args.critical:
            # f-string not possible because of compatibility versions
            print(
                path
                + " modified "
                + str(datetime.timedelta(seconds=int(age)))
                + " ago."
            )
            sys.exit(2)
    for age, path in age_path_tuple_list:
        if age > args.warning:
            # f-string not possible because of compatibility versions
            print(
                path
                + " modified "
                + str(datetime.timedelta(seconds=int(age)))
                + " ago."
            )
            sys.exit(1)
    print("All files are recent enough")
    sys.exit(0)


def check_min(age_path_tuple_list):
    min_path_age = min(age_path_tuple_list, key=lambda age: age[0])
    # f-string not possible because of compatibility versions
    print(
        "Most recent file is "
        + min_path_age[1]
        + " modified "
        + str(datetime.timedelta(seconds=int(min_path_age[0])))
        + " ago."
    )

    if min_path_age[0] > args.critical:
        sys.exit(2)
    if min_path_age[0] > args.warning:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    try:
        args = parser.parse_args()
        globs = [glob.glob(pattern) for pattern in args.files]
        age_path_tuple_list = [
            (current_time - os.path.getmtime(path), path)
            for path in chain.from_iterable(globs)
        ]
        if not age_path_tuple_list:
            print("No file found in specified path(s)")
            sys.exit(3)
        if args.all:
            check_all(age_path_tuple_list)
        else:
            check_min(age_path_tuple_list)
    except Exception as e:
        print(e)
        sys.exit(3)
