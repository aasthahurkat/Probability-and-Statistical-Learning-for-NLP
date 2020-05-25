# Report

-------------------------

## Part 1

The code for pos_solver.py aims to train the data by calculating - 
P(Si+1|Si) = count(Si, Si+1) / count(Si),

P(Wi|Si) = count(Wi, Si) / count(Si).

The transition matrix is calculated as a 12*12 matrix for all the POS(s).

For the Simple approach, each word is labeled as the maximum probability for that particular word and is independent of every other word in the sentence. 

For the HMM approach, we have calculated the MAP by calculating the probabilities of each POS of starting a sentence and applied forward and backward propogation to come up with the most likely sequence.

For the MCMC approach, we have performed gibbs sampling, where we randomly generate a first sample of results and then gradually bias it towards actual probability.

The main challange was underflow as the probabilities in the transition matrix were really small values and basically amounted to zero on multiplying with other probabilities. So as a solution, we used log transformations. 

The final results are as follows -

                  Words correct:     Sentences correct:
   0. Ground truth:      100.00%              100.00%
         1. Simple:       92.21%               39.95%
            2. HMM:       80.29%               23.90%
        3. Complex:       23.95%                0.00%


-------------------------

## Part 2

We have made use of mutltithreading capabilities of Python to optimize our program in getting much faster result.
In our code, we decided to use ThreadPoolExecutor for this purpose. The two kinds of decoding methods to be used in the
given problem were rearrangement of alphabets and replacement of alphabets. For each combination of rearrangement table,
we made a separate thread for it's execution. In each thread we are trying to modify the replacement table by switching
two alphabets at a time and then calculate the P(D) and P(D'). Based on the values of both probabilities, we are then 
either keeping the new replacement table or not. We are able to get a result of the text that is only a few alphabets
away from being fully decrypted. But this depends on chance, as our code is heavily dependant on random number generation.

-------------------------

## Part 3
The basic algorithm is as follows:

if P(Spam|Word) > P(NotSpam|Word)):
  return Spam
else:
  return NotSpam

Calculating individual values:
P(Spam|Word) = P(Word|Spam).P(Spam)/P(Word)

P(Word) ignored (since it is common on both sides) 
P(Word|Spam) = P(Word1|Spam). P(Word2|Spam) . P(Word3|Spam)......
P(Word1|Spam) = count of word1 in Spam + 1/ total words in Spam + Total words in (Spam + NotSpam)
P(Spam)= No. of documents marked Spam / Total no. of documents

If the classifier detects a new word that is not present in training data sets, P(thatWord|Spam) would be zero, making the complete product ZERO. Thus, taking logarithm on both sides

-------------------------
