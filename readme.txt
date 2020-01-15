This was a part of the assignment under my course Elements of Artificial Intelligence.


Basic algorithm:

if P(Spam|Word) > P(NotSpam|Word)): return Spam else: return NotSpam

Calculating individual values: P(Spam|Word) = P(Word|Spam).P(Spam)/P(Word)

P(Word) ignored (since it is common on both sides) P(Word|Spam) = P(Word1|Spam). P(Word2|Spam) . P(Word3|Spam)...... P(Word1|Spam) = count of word1 in Spam + 1/ total words in Spam + Total words in (Spam + NotSpam) P(Spam)= No. of documents marked Spam / Total no. of documents

If the classifier detects a new word that is not present in training data sets, P(thatWord|Spam) would be zero, making the complete product ZERO. Thus, taking logarithm on both sides
