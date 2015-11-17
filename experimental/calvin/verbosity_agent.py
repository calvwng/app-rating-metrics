import re

#global variables
histogramlst = {}
verbosityscoreslst = {}
max = 0
# maxReview = None

def reset():
    global histogramlst, verbosityscoreslst, max
    histogramlst = {}
    verbosityscoreslst = {}
    max = 0

def createHistogram(reviewlst):
   global max
   # global maxReview
   for i in range(1,11):
      histogramlst[i] = 0

   for i in range(len(reviewlst)):
      obj = reviewlst[i]
      #assigns only an array of words with special characters
      numWords = len(re.split(r'[^0-9A-Za-z]+', obj['original_review']))

      if numWords > max:
         max = numWords
         # maxReview = obj

      if numWords not in histogramlst:
         histogramlst[numWords] = 1
      else:
         histogramlst[numWords] += 1


def createVerbosityScale():
   global max
   for i in range(0, 10): # on a verbosity scale of 1 to 10
      lowerlimit = max * i / 10.0
      upperlimit = max * (i + 1) / 10.0
      verbosityscoreslst[i + 1] = upperlimit # upper bound pertaining to verbosity score of i
      print 'Word count of', lowerlimit, 'to', upperlimit, 'yields verbosity score', i
      for numWords in histogramlst:
         if float(numWords) == 0:
            print 0
         elif float(numWords) > lowerlimit and float(numWords) <= upperlimit:
            print '# of', numWords, 'worded reviews:', histogramlst[numWords], 'reviews'
      print

def assignVerbosityScores(objList):
   for obj in objList:
       wordCount = len(re.split(r'[^0-9A-Za-z]+', obj['original_review']))
       for i in verbosityscoreslst:
           if wordCount <= verbosityscoreslst[i]:
               obj['verbosity'] = i
               obj['verbosity_word_count'] = wordCount
               break

# SMOKETEST:
# # temp array of arrays of one string
# reviewlst = [{'original_review': 'This is a great game'},
#              {'original_review': 'good'},
#              {'original_review': 'bad'},
#              {'original_review': 'Why is this such a terrible game'},
#              {'original_review': 'five out of five'}]
# createHistogram(reviewlst)
# createVerbosityScale()
# assignVerbosityScores(reviewlst)
# print reviewlst