# Web Corpus Construction
This repository contains code and documentation for supporting the web corpus construction session at UCREL summer school 2016.

## Setup guide
1. Insert UCREL memory stick into the computer.
2. Go to Removable Disk E in the file explorer.
3. Go to web-corpus-construction folder
4. __Shift and right click__ on a blank part of the file explorer and from the menu click open command window here
5. In the command prompt type the following command:
    1. Note that in the command below the seed_urls\ it can then be either twitter, blogs or news articles just have a look within the seed_urls folder for which seed urls you would like and note that the database_name is the name of the database you want the data saving to but the argument is optional by default it is called database.
    2. ..\Miniconda3\python.exe run.py seed_urls\blogs.txt database_name


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


## Plan for session 1 "Web scraping theory and methods"
PR: slides intro to the whole NLP summer school week (10 minutes)

PR: slides theory overview (10-15 minutes) to include:
 * history
 * rationale
 * web as corpus

SW: Around 10 minutes slides and 20 minutes practical for each of the following three steps.

 1. Receive a seed URL list of 100 seed URLs.  Three seed lists will be produced:
    * Blogs
    * News articles
    * Links taken from Twitter corpus
 2. Visit the URLs manually and look for features that might be complex:
    * Forms
    * Logins and restricted access
    * Dynamic pages
    * Language
    * Encodings
    * Navigation and content areas
    * Any metadata such as usernames, etc.
 3. Run the spider over the data:
    1. Insert the URL list into the input list
    2. Retrieve a URL at random from the input list and;
       1. Download the page
       2. Compare it to the output list and discard if duplicate
       3. Parse the page using Urllib2 and BeautifulSoup, extract URLs and metadata
       4. Insert into the output list
    3. End condition met?  Else go to 2.
 4. Export data

Here we will have a single output database table containing the data itself, metadata about the download process, and possibly some features extracted from the page (particularly the page `title` and `h1` element contents).

## Plan for session 2 "Web as corpus creation and cleaning"
SW: 20 minutes for the students to inspect their own data hopefully to discover issues of:
 * encoding 
 * double escaping

PR: slides with overview of research findings (10-15 minutes)
 * cleaneval

PR: practical 5 steps (timing to be decided)

Take over the data gathered in session 1 and start processing it:

 1. SQLite export to a collection of files (if we have not)
 2. Character set normalisation using python (`__future__`, iconv)
 3. Boilerplate removal (justext or boilerpipe)
 4. Normalising metadata such as dates and titles from the HTTP headers
 5. Writing to XML/JSON files as a corpus

