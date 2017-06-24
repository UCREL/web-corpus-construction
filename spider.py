#!/usr/bin/env python3

# ----------------------------------------------------------------
# Modules required for basic functionality
import argparse
import logging
import os
import sys
from functools import reduce
import operator

import HTTPClient
import CorpusTable
import Features
import Normalisation

# ----------------------------------------------------------------
# Pluggable module imports
#
# Add new modules below if you write any!
#
from filter         import DuplicateFilter, MinimumLengthFilter, MaximumLengthFilter, URLCountFilter, MetadataRegexpFilter
from urlfilter      import HTTPURLFilter, PreciseDuplicateURLFilter
from endcondition   import CorpusSizeEndCondition, RuntimeEndCondition, SampleEndCondition
from fitness        import SimplicityURLRank, SampleURLRank

# ----------------------------------------------------------------
# Parse command-line arguments
#
parser = argparse.ArgumentParser(description="A web crawler demo for the UCREL Summer School 2016")
parser.add_argument('-seeds', action="store", dest="list")
parser.add_argument('-db', action="store", dest="dbdir", default="output")
parser.add_argument('-loglevel', action="store", dest="loglevel", default="INFO")
args = parser.parse_args()


# ----------------------------------------------------------------
# Configure logging to console and to file using the logging framework.
#
log_level = logging.getLevelName(args.loglevel.upper())
logging.basicConfig(format='%(levelname)7s - %(name)s - %(asctime)s: %(message)s',
                    filename='run.log', level=log_level)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter('%(levelname)7s - %(name)-8s: %(message)s'))
logging.getLogger('').addHandler(console)
log = logging.getLogger('main')



# ----------------------------------------------------------------
# Load various components, and configure the modules that control
# the crawling process
#
corpus_table        = CorpusTable.CorpusTable(args.dbdir)                           # Storage layer
spider              = HTTPClient.HTTPClient()                                       # Retrieval code
url_normaliser      = Normalisation.URLNormaliser()                                 # URL normaliser
feature_extractor   = Features.Features(url_normaliser, ['title', 'h1'])            # Feature extractor
url_rank_function   = {'simple' : SimplicityURLRank.SimplicityURLRank(),            # URL fitness function
                       'sample' : SampleURLRank.SampleURLRank()
                      }
page_filters        = [                                                             # Filters for page rejection
                       #FuzzyDuplicateFilter.FuzzyDuplicateFilter(corpus_table),
                       DuplicateFilter.DuplicateFilter(corpus_table),
                       MinimumLengthFilter.MinimumLengthFilter(100),
                       MaximumLengthFilter.MaximumLengthFilter(800000),
                       URLCountFilter.URLCountFilter(0, 1000),
                       MetadataRegexpFilter.MetadataRegexpFilter('content_type', 'text\/(x?html|plain)'),
                      ]
url_filters         = [                                                             # Filters for URL rejection
                       HTTPURLFilter.HTTPURLFilter(),
                       PreciseDuplicateURLFilter.PreciseDuplicateURLFilter(corpus_table)
                      ]
end_conditions      = [                                                             # End conditions
                       CorpusSizeEndCondition.CorpusSizeEndCondition(100),
                       RuntimeEndCondition.RuntimeEndCondition(3600),
                       SampleEndCondition.SampleEndCondition()
                      ]

# ----------------------------------------------------------------
# Load initial URLs if a seed list is given
#
if args.list is not None:
    log.info("Reading seed URLs from %s" % args.list)
    with open(args.list) as f:
        for line in f:
            url = url_normaliser.normalise(line.rstrip())
            accepted = [f.accept(url) for f in url_filters]
            log.debug("%s out of %s URL filters accepted the URL" % (sum(accepted), len(url_filters)))
            if sum(accepted) == len(url_filters):
                corpus_table.insert_url(url, url_rank_function['simple'].goodness(url))

# ----------------------------------------------------------------
# Main crawling loop
#
cont = True
while cont:

    # ------------------------------------------------------------
    # Summarise the state in the logs, and update counters
    #
    corpus_size         = corpus_table.output_count()
    available_urls      = corpus_table.url_count(False)
    log.info("%i URLs downloaded; %i available" % (corpus_size, available_urls))


    # ------------------------------------------------------------
    # If we can't read anything, quit.
    # This is the one hard-coded end condition
    if available_urls == 0:
        log.fatal("No available URLs found.  Shutting down.")
        cont = False
        continue


    # ------------------------------------------------------------
    # Select the best URL from the database
    url, url_id, goodness, depth = corpus_table.best_url()
    log.info("URL chosen -- goodness: %s, depth: %s" % (goodness, depth))
    corpus_table.update_url(url_id)


    # ------------------------------------------------------------
    # Make a HTTP request for the page and contents
    log.info("Retrieving %s..." % url)
    page, body = spider.get_page(url, corpus_table)

    # If retrieval failed, continue onto next URL
    if page is None or body is None:
        continue


    # ------------------------------------------------------------
    # Extract features from the page and request data
    log.info("Performing feature extraction...")
    body, metadata = feature_extractor.get_page_metadata(page, body)


    # ------------------------------------------------------------
    # Run filters to remove pages with undesirable content
    log.info("Applying accept/reject page filters...")
    accept = True
    for f in page_filters:
        accept = accept & f.accept(body, metadata)
        log.info("Filter %s -- accept? %s" % (f.name, accept))
        if not accept:
            log.warning("Rejected page by filter: %s" % f.name)
            break

    if not accept:
        continue
    log.info("Page accepted!")


    # ------------------------------------------------------------
    # Run filters to remove undesirable forward links
    log.info("Applying accept/reject URL filters...")
    for f in url_filters:
        count_pre = len(metadata['urls'])
        metadata['urls'] = list(filter(lambda u: f.accept(u), metadata['urls']))
        count_post = len(metadata['urls'])
        log.info("URL Filter %s rejected %i urls" % (f.name, count_pre - count_post))
        if count_post == 0:
            break


    # ------------------------------------------------------------
    # Insert URLs into DB
    log.info("Inserting %i URLs" % len(metadata['urls']))
    urls = metadata.pop('urls')
    for url in urls:
        corpus_table.insert_url(url, url_rank_function['simple'].goodness(url), depth + 1)


    # ------------------------------------------------------------
    # Insert page data into DB and onto disk
    log.info("Inserting/writing page data...")
    metadata['url_id'] = url_id
    corpus_table.insert_page(metadata, body)


    # ------------------------------------------------------------
    # Test for end conditions
    end = False
    for e in end_conditions:
        end = end & e.end(corpus_table, body, metadata)
        log.info("End by condition '%s'? %s" % (e.name, end))
        if end:
            log.info("End condition reached.  Quitting...")
            cont = False


# Clean up database
log.debug("Disconnecting database...")
corpus_table.disconnect

# Tell people we didn't crash
log.info("Done.  Exiting under normal circumstances.")
