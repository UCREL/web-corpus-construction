from .EndCondition import EndCondition

class SampleEndCondition(EndCondition):

    def __init__(self):
        EndCondition.__init__(self, "Sample End Condition")

    def end(self, corpus_table, body, metadata):
        '''Returns true if the crawler should stop else false.

        Currently set to False to allow the crawler to run.
        '''

        return False
