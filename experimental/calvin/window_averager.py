import datetime, collections

test_scores = [{'verbosity': 1, "date": "2015-10-19T16:08:52"},
               {'verbosity': 2, "date": "2015-10-19T16:08:52"},
               {'verbosity': 3, "date": "2015-10-20T16:08:52"},
               {'verbosity': 4, "date": "2015-10-21T16:08:52"},
               {'verbosity': 5, "date": "2015-10-30T16:08:52"}]

def as_datetime(str):
    return datetime.datetime.strptime(str, '%Y-%m-%dT%X')

def as_date_only_str(date):
    return date.strftime('%Y-%m-%d')

# Assume the reviews are already sorted by ascending date:
# For each distinct date, find average <metric> score
# within |windowSize| days of the date.
# Returns a list of {'date': ..., 'avg_<metric>': ...} objects
def get_win_avgs(reviews, metric, window_size):
    win_avg_scores = collections.OrderedDict()
    next_key_date = None

    for i in range(0, len(reviews)):
        cur_review = reviews[i]
        cur_date = as_datetime(cur_review['date'])

        # Don't pick dates from the last window to use as the next window's center
        if next_key_date is not None and (next_key_date - cur_date).days > 0:
            print as_date_only_str(cur_date), 'is before next window center', as_date_only_str(next_key_date), ', so skipping'
            continue

        print "\nWindow center:", as_date_only_str(cur_date)
        min_date = cur_date - datetime.timedelta(days=window_size)
        max_date = cur_date + datetime.timedelta(days=window_size)
        next_key_date = max_date + datetime.timedelta(days=1) # Want next date past the window for next avg

        window_avg = 0
        total_scores = 0
        left_idx = i - 1
        right_idx = i + 1

        # Sum up scores within left side of window
        while left_idx >= 0:
            left_review = reviews[left_idx]
            left_date = as_datetime(left_review['date'])
            if left_date < min_date:
                #print 'Outside windowSize; done with left side'
                break
            window_avg += left_review[metric]
            total_scores += 1
            left_idx -= 1

        # Add current review's score to window's sum
        window_avg += cur_review[metric]
        total_scores += 1

        # Sum up scores within right side of window
        while right_idx < len(reviews):
            right_review = reviews[right_idx]
            right_date = as_datetime(right_review['date'])
            if right_date > max_date:
                #print 'Outside windowSize; done with right side'
                break
            window_avg += right_review[metric]
            total_scores += 1
            right_idx += 1

        print window_avg, "/", total_scores, "scores in datetime window"
        print "Window's avg:", float(window_avg) / total_scores
        win_avg_scores[as_date_only_str(cur_date)] = (window_avg) / total_scores
        #print 'Done with review', i
    return win_avg_scores

# print getWinAvgs(test_scores, 'verbosity', 1)