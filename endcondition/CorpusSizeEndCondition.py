




from .EndCondition import EndCondition

class CorpusSizeEndCondition(EndCondition):


    def __init__(self, threshold):
        EndCondition.__init__(self, "Corpus Size (%s)" % threshold)
        self.threshold = threshold

    def end(self, corpus_table, body, metadata):
        '''Overrides EndCondition#end.

        Ends when the number of output files is greater than the threshold.'''
        
        corpus_size = corpus_table.output_count()
        return corpus_size > self.threshold



