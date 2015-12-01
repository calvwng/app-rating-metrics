import enchant

dict = enchant.Dict()

def spelling_score(s):
    correct = 0
    incorrect = 0
    for word in s.split():
        if dict.check(word):
            correct += 1
        else:
            incorrect += 1
    if incorrect == 0:
        return 5
    else:
        incorr_percent = incorrect / float(correct + incorrect)
        if incorr_percent > 0.3:
            return 0
        elif incorr_percent > 0.2:
            return 1
        elif incorr_percent > 0.1:
            return 2
        elif incorr_percent > 0.05:
            return 3
        else:
            return 4

def assignSpellcheckScores(objList):
   for obj in objList:
       obj['spellcheck'] = spelling_score(obj['original_review'])