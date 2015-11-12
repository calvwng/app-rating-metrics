import re
# temp array of arrays of one string
reviewlst = [['This is a great game'],['good'],['bad'],['Why is this such a shitty game'],['five out of five']]

#
histogramlst = {}


for i in range(len(reviewlst)):
           
           for j in reviewlst[i]:
                         
                         #assigns only an array of words with special characters
                               temp = len(re.split(r'[^0-9A-Za-z]+',j))
                                     
                                           if temp not in histogramlst:
                                                            histogramlst[temp] = 1
                                                                  else:
                                                                                   histogramlst[temp] += 1

                                                                                   print("Number of words : occurance")
                                                                                   for key in histogramlst:
                                                                                              print str(key) + " : " + str(histogramlst[key])
                                                                                                 

