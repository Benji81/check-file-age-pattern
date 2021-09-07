# check-file-age-pattern

A Python2 & Python3 script to detect if files are recent enought. 2 modes are available
- default: at least one file is recent enough.
- all: all files must be recent enough

This project is designed to be a Nagios-NRPE probe to check if a periodic  backup has been done correctly.

## Installation

Download the .py file and put it anywhere you want.

### Example
```bash
./check-file-age-pattern.py --warning 84000 --critical 10000 '/backup/db*.tar'
```
- will return 0 if at least one file matching `/backup/db*.tar` in your filesystem has been modified in less that 86,400 seconds.
- if not, will return 1 if at least one file has been modified between 86,400 and 100,000
- will return 2 if no file have benn modified since 100,000 seconds
- will return 3 is something wrong or no file match patterns

### Note

File patterns should be given between simple quotes if they contain special characters like * to not being interpreted by your shell
