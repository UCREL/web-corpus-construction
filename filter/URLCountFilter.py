



from .Filter import Filter

class URLCountFilter(Filter):


    def __init__(self, lower_threshold=0, upper_threshold=1000):
        Filter.__init__(self, 'URL Count')
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold


    def accept(self, body, metadata=None):
        '''Overrides Filter#accept.

        Rejects pages with a number of links that is below the lower_threshold,
        or higher than the upper_threshold.'''

        self._log.debug("Number of URLs: %s >= %s >= %s" % (self.lower_threshold, len(metadata['urls']), self.upper_threshold))

        return len(metadata['urls']) >= self.lower_threshold and len(metadata['urls']) <= self.upper_threshold



