def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def __is_negation(possible_negations):
    full_string = " ".join(possible_negations)
    if any(str in full_string for str in negation_list):
        print "negation here: " + full_string
        return -1
    return 1

def sentiment_score(s):
    score = 0
    count = 0
    possible_negations = []
    for word in s.split():
	possible_negations.append(word)
        count += 1
        if count > 3:
           possible_negations.pop(0)
        multiplier = 1
        if word in sent_dict:
            temp_score = sent_dict[word]
            score += temp_score * __is_negation(possible_negations)
    if score > 5:
        score = 5
    if score < -5:
        score = -5
    return score

sent_dict = {}
with open('vader_sentiment_lexicon.txt') as word_file:
    for line in word_file:
        word_weight = line.split()
        if is_number(word_weight[1]):
            sent_dict[word_weight[0]] = float(word_weight[1])

negation_list = open('negationWords.txt').read().splitlines()

