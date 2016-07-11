# Web Corpus Construction
This repository contains code and documentation for supporting the web corpus construction session at UCREL summer school 2016.

## Setup guide
1. Insert UCREL memory stick into the computer.
2. Go to Removable Disk E in the file explorer.
3. Go to web-corpus-construction folder.
4. __Shift and right click__ on a blank part of the file explorer and from the menu click open command window here.
5. Python is at the following: ..\..\python\python.exe


## Use
Run `python spider.py -h` to see the help text:

    usage: spider.py [-h] [-seeds LIST] [-db DBDIR] [-loglevel LOGLEVEL]

    A web crawler demo for the UCREL Summer School 2016

    optional arguments:
      -h, --help          show this help message and exit
      -seeds LIST
      -db DBDIR
      -loglevel LOGLEVEL

First run, you'll need to provide a one-url-per-line list using the `-seeds` argument:

    python spider.py -seeds seed_urls/twitter.txt -db /tmp/test -loglevel DEBUG

After that, you can resume a crawl by simply running it on the same database:

    python spider.py -db /tmp/test -loglevel DEBUG

Available log levels are:

 * DEBUG
 * WARNING
 * INFO
 * ERROR
 * FATAL


## Dependencies
The tools here require a number of python libraries to run.  Whereever possible we have included these in the repository in a virtualenv directory.  We also maintain a list at [dependencies.md](dependencies.md).
