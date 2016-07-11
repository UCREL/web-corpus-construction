




from .EndCondition import EndCondition
import time

class RuntimeEndCondition(EndCondition):


    def __init__(self, time_in_seconds):
        EndCondition.__init__(self, "Runtime (%s secs)" % time_in_seconds)
        self.start_up_time = time.time()
        self.runtime = time_in_seconds 

    def end(self, corpus_table, body, metadata):
        '''Overrides EndCondition#end.

        Ends after a given number of seconds have elapsed.'''

        return time.time() > (self.start_up_time + self.runtime)




