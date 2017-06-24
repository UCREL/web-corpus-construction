# Feature extraction code.
#

import logging
import re
import hashlib
from urllib.parse import urljoin

# Pip modules
from bs4 import BeautifulSoup, SoupStrainer

class Features:

    def __init__(self, url_normaliser, tags=[]):
        self._log = logging.getLogger('features')

        self.url_normaliser = url_normaliser

        self.tags = {}
        for tag in tags:
            self.tags[tag] = SoupStrainer(tag)
        self._link_extractor = SoupStrainer('a')



    def get_links(self, body, rel_url=None):
        '''Return a list of strings that are absolute HTTP URLs from the body text provided'''

        urls = []
        for url in BeautifulSoup(body, "html.parser", parse_only=self._link_extractor):
            href = url.get('href')
            if href is None:
                continue

            # Remove any whitespace
            href = href.strip()
            
            # Check for relative URL and fix if rel_url != None
            if re.match('^[a-zA-Z]{2,}:', href) == None and rel_url is not None:
                abs_href = urljoin(rel_url, href)
                self._log.debug("Converting relative URL to absolute: %s -> %s" % (href, abs_href))
                href = abs_href

            # Normalise string
            href_norm = self.url_normaliser.normalise(href)
            self._log.debug("Normalised URL: %s -> %s" % (href, href_norm))

            # Add to the list
            self._log.debug("Adding URL to candidate list: %s" % href_norm)
            urls.append(href_norm)


        return urls


    def get_tags(self, body):
        '''Return a list of tag contents for each tag in the list'''

        tags = {}
        for tag, parser in self.tags.items():
            t = BeautifulSoup(body, "html.parser", parse_only=parser)
            t = self._get_all_tag_strings(t)
            t = list(map(lambda x: str(x).strip(), t))
            tags[tag] = t
            
        return tags


    def get_http_headers(self, page):
        '''Return a select list of HTTP metadata'''

        headers       = dict(page.info())
        headers_copy  = headers.copy()
        # Normalise all header keys to lower case.
        for key in headers_copy:
            value = headers.pop(key)
            headers[key.lower()] = value

        return headers


    def get_page_metadata(self, page, body):
        '''Extract all features from the page and return a dictionary containing
        salient metadata'''
        
        # Retrieve candidate URLs
        links   = self.get_links(body, page.geturl())
        tags    = self.get_tags(body)
        headers = self.get_http_headers(page)

        # Hash the page data as binary
        sha1    = hashlib.sha1()
        sha1.update(body)
        sha1 = sha1.hexdigest()

        # Build a metadata description of the page data
        metadata      = {   'date'         : None,
                            'charset'      : None,
                            'content_type' : None,
                            'title'        : tags['title'][0]   if tags['title'] else '',
                            'h1'           : tags['h1'][0]      if tags['h1']    else '',
                            'urls'         : links,
                            'hash'         : sha1
                        }

        # Fix common header formatting issues to simplify later processing
        if 'content-type' in headers:
            content_type = headers['content-type']

            if ';' in content_type:
                charset = re.findall("charset=[-\w]*", content_type)[0].split("=")[1]
                content_type = content_type.split(";")[0]
                metadata['charset']      = charset

            metadata['content_type'] = content_type

        # Populate date if it's there
        if 'date' in headers:
            metadata['date'] = headers['date']

        return body, metadata



    # ^ Public
    # -----------------------------------------------------------------
    # v Private


    def _get_all_tag_strings(self, tags):
        '''Given a list of BeautifulSoup tags it returns a list of the most inner strings within those tags.'''

        all_tag_strings = []
        while True:
            tags_left = []
            for index, tag in enumerate(tags):
                tag_data = self._get_tag_string(tag)
                if type(tag_data) == type(''):
                    all_tag_strings.append(tag_data)
                elif tag_data == None:
                    pass
                else:
                    tags_left.extend(tag_data)
            if len(tags_left) == 0:
                break
            tags = list(tags_left)

        # Remove all Strings that are empty in the list
        all_tag_strings = filter(lambda tag_string: tag_string, all_tag_strings)

        return all_tag_strings



    def _get_tag_string(self, tag):
        '''Given a BeautifulSoup tag retruns either a List of tags, None or a unicode string.

        It will return a list of tags if tag given has more than one inner tag
        wihtin it.

        It will return None if their is no String within the html tags.

        If none of the above happen it will return the unicode string.
        '''

        while tag.string == None:
            tag = tag.contents
            # More than one tag within a tag
            if len(tag) > 1:
                return tag
            # No String in the inner tag
            elif len(tag) == 0:
                return None
            # The String within the most inner tag.
            else:
                tag = tag[0]
        return tag.string.strip()



