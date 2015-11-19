import datetime, collections

test_scores = [{'verbosity': 1, "date": "2015-10-19T16:08:52"},
               {'verbosity': 2, "date": "2015-10-19T16:08:52"},
               {'verbosity': 3, "date": "2015-10-20T16:08:52"},
               {'verbosity': 4, "date": "2015-10-21T16:08:52"},
               {'verbosity': 5, "date": "2015-10-30T16:08:52"}]

def asDatetime(str):
    return datetime.datetime.strptime(str, '%Y-%m-%dT%X')

def asDateOnlyStr(date):
    return date.strftime('%Y-%m-%d')

# Assume the reviews are already sorted by ascending date:
# For each distinct date, find average <metric> score
# within |windowSize| days of the date.
# Returns a list of {'date': ..., 'avg_<metric>': ...} objects
def getWinAvgs(reviews, metric, windowSize):
    winAvgScores = collections.OrderedDict()
    nextKeyDate = None

    for i in range(0, len(reviews)):
        curReview = reviews[i]
        curDate = asDatetime(curReview['date'])

        # Don't pick dates from the last window to use as the next window's center
        if nextKeyDate != None and (nextKeyDate - curDate).days > 0:
            print asDateOnlyStr(curDate), 'is before next window center', asDateOnlyStr(nextKeyDate), ', so skipping'
            continue

        print "\nWindow center:", asDateOnlyStr(curDate)
        minDate = curDate - datetime.timedelta(days=windowSize)
        maxDate = curDate + datetime.timedelta(days=windowSize)
        nextKeyDate = maxDate + datetime.timedelta(days=1) # Want next date past the window for next avg

        windowAvg = 0
        totalScores = 0
        leftIdx = i - 1
        rightIdx = i + 1

        # Sum up scores within left side of window
        while leftIdx >= 0:
            leftReview = reviews[leftIdx]
            leftDate = asDatetime(leftReview['date'])
            if leftDate < minDate:
                #print 'Outside windowSize; done with left side'
                break
            windowAvg += leftReview[metric]
            totalScores += 1
            leftIdx -= 1

        # Add current review's score to window's sum
        windowAvg += curReview[metric]
        totalScores += 1

        # Sum up scores within right side of window
        while rightIdx < len(reviews):
            rightReview = reviews[rightIdx]
            rightDate = asDatetime(rightReview['date'])
            if rightDate > maxDate:
                #print 'Outside windowSize; done with right side'
                break
            windowAvg += rightReview[metric]
            totalScores += 1
            rightIdx += 1

        print windowAvg, "/", totalScores, "scores in datetime window"
        print "Window's avg:", float(windowAvg) / totalScores
        winAvgScores[asDateOnlyStr(curDate)] = (windowAvg) / totalScores
        #print 'Done with review', i
    return winAvgScores

print getWinAvgs(test_scores, 'verbosity', 1)