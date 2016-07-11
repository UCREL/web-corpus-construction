

# Native imports
import logging

# pip imports

class EndCondition:

    def __init__(self, name='EndCondition'):
        self._log = logging.getLogger('endcond')
        self.name = name


    def end(self, corpus_table, body, metadata):
        '''Returns true if the crawler should stop else false.'''

        return True


