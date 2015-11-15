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
         temp = len(re.split(r'[^0-9A-Za-z]+',j))
      
         if temp > max:
            max = temp
      
         if temp not in histogramlst:
            histogramlst[temp] = 1
         else:
            histogramlst[temp] += 1
   
      
def findverbosityscores():
   global max
   for i in range(10):
      lowerlimit = max * i/10.0
      upperlimit = max *(i+1)/10.0
      print lowerlimit,upperlimit
      for temp in histogramlst:
         if float(temp) == 0:
            print 0
         elif float(temp) > lowerlimit and float(temp) <= upperlimit:
            print temp,"is between ",lowerlimit,'and',upperlimit,'for',histogramlst[temp],'amount of times and the verbosity score is',i



createHistogram(reviewlst)
findverbosityscores()