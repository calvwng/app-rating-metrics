import re
# temp array of arrays of one string
reviewlst = [['This is a great game'],['good'],['bad'],['Why is this such a shitty game'],['five out of five']]

#global variables
histogramlst = {}
verbosityscoreslst = {}
max = 0


def createHistogram(reviewlst):
   global max
   for i in range(1,11):
      histogramlst[i] = 0

   for i in range(len(reviewlst)):
      for j in reviewlst[i]:
         #assigns only an array of words with special characters
         numWords = len(re.split(r'[^0-9A-Za-z]+',j))

         if numWords > max:
            max = numWords

         if numWords not in histogramlst:
            histogramlst[numWords] = 1
         else:
            histogramlst[numWords] += 1


def findverbosityscores():
   global max
   for i in range(10):
      lowerlimit = max * i/10.0
      upperlimit = max *(i+1)/10.0
      print 'Range', lowerlimit, 'to', upperlimit, 'yields verbosity score', i
      for numWords in histogramlst:
         if float(numWords) == 0:
            print 0
         elif float(numWords) > lowerlimit and float(numWords) <= upperlimit:
            print '# of', numWords, 'worded reviews:', histogramlst[numWords], 'reviews'
      print



createHistogram(reviewlst)
findverbosityscores()
