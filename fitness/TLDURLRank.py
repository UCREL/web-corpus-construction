from .URLRank import URLRank

import tldextract


class TLDURLRank(URLRank):

    all_tld_freq = {}

    def __init__(self, scale=1):
        URLRank.__init__(self, "TLD URL Rank", scale)

    def goodness(self, url):
        '''Overrides URLRank#goodness.

        Ranks based on the frequency of the TLD in the corpus which is based on
        1/number of TLDs already downloaded for that TLD.'''

        ext = tldextract.extract(url)
        tld_estimate = ext.suffix

        tld_freq = TLDURLRank.all_tld_freq.get(tld_estimate, 0) + 1
        TLDURLRank.all_tld_freq[tld_estimate] = tld_freq

        fit_score = 1 / tld_freq

        self._log.info('URL: %s fitness %f', url, fit_score)

        return fit_score
