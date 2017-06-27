# Web Corpus Construction
This repository contains code and documentation for supporting the web corpus construction session at the UCREL NLP summer school 2016.

## Slides that support the code
### [Introduction slides](slides/UCREL_NLP_S1_Web_Scraping_Intro.pdf)

### [Main presentation slides](https://docs.google.com/presentation/d/1hT0rGlYWcMuR_9qKYucGHn8mLuJPZLdSkLbqoCI9D38/edit?usp=sharing)

## Setup guide
1. Insert UCREL memory stick into the computer.
2. Go to Removable Disk E in the file explorer.
3. __Shift and right click__ on a blank part of the file explorer and from the menu click open command window here.
4. Python is within the python folder under python.exe.


## Use
Run `./spider.py -h` to see the help text:

    usage: spider.py [-h] [-seeds LIST] [-db DBDIR] [-loglevel LOGLEVEL]

    A web crawler demo for the UCREL Summer School 2016

    optional arguments:
      -h, --help          show this help message and exit
      -seeds LIST
      -db DBDIR
      -loglevel LOGLEVEL

First run, you'll need to provide a one-url-per-line list using the `-seeds` argument:

    ./spider.py -seeds seed_urls/twitter.txt -db output -loglevel DEBUG

After that, you can resume a crawl by simply running it on the same database:

    ./spider.py -db output -loglevel DEBUG

Available log levels are:

 * DEBUG
 * WARNING
 * INFO
 * ERROR
 * FATAL


## Dependencies
The tools here require a number of python libraries to run. We maintain a list in the conventional [requirements.txt](requirements.txt).  To install these, run:

    pip3 install --user -r requirements.txt

In addition to those requirements mentioned above, we also inlined the code to [url\_normalize](https://github.com/niksite/url-normalize) in the interests of clarity.
