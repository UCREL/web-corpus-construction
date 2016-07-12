#Ranking methods
All ranking are subclasses of *URLRank*. We have given you one example
*SimplicityURLRank* which ranks by the length of the URL the more parts
to the URL the worse the rank.

We would like you to create your own within *SampleURLRank* here are some
examples of how it could rank by:

1. The depth of the URL.
2. Depth or breadth first approach.
3. Given a sample document rank links higher that have more similar content
to the sample document.
4. The social media links.
5. Content creation/modification

#End conditions
All end conditions are subclasses of *EndCondition*. We have given you to
examples *CorpusSizeEndCondition* and *RuntimeEndCondition* which do the
following:

1. *CorpusSizeEndCondition* returns True when the size of the corpus is greater
than the given threshold. At the moment this is set at 100 documents.
2. *RuntimeEndCondition* returns True when the spider has been running more
than the given time in seconds. At the moment this is set at 6 minutes.

We would like you to create your own end condition within *SampleEndCondition*.
Here are a few examples of what you could do:

1. Base the end condition on your Ranking method e.g. Once there are no more
URLs in the fringe that have a goodness value greater than X.
2. The depth of the URLs e.g. once all URLs have a depth less than 3.
3. Create a new Ranking method for your end condition. 

#Filter methods
We currently have 5 filter methods of which they do the following:

1. *DuplicateFilter* checks that the web page does not already exist
2. *MinimumLengthFilter* checks if the page has more than a certain amount of
characters within the page content.
3. *MaximumLengthFilter* checks if the page has less than a certain amount of
characters within the page content.
4. *URLCountFilter* has a lower and upper bound threshold on the number of
links a page can have.
5. *MetadataRegexpFilter* checks if a header within the metadata matches a
specified pattern. At the moment this is set to check if the content type is
html or text.

Have a look at the threshold you can set and see the differences in the data
you collect.
