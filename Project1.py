#!/usr/bin/env python
# coding: utf-8

# # Project 1:  Reading & getting familiar with the data

# In[2]:


# What we know!
g = open('reviews.txt','r') 
reviews = list(map(lambda x:x[:-1],g.readlines()))
g.close()

# What we WANT to know!
g = open('labels.txt','r') 
labels = list(map(lambda x:x[:-1].upper(),g.readlines()))
g.close()


# Note: The data in reviews.txt we're using has already been preprocessed a bit and contains only lower case characters. If we were working from raw data, where we didn't know it was all lower case, we would want to add a step here to convert it. That's so we treat different variations of the same word, like The, the, and THE, all the same way.

# In[3]:


#size of reviews list
len(reviews)


# In[5]:


#first element in reviews list
reviews[0]


# In[6]:


#first element in labels list
labels[0]


# ### Function to display the label and the corresponding review at ith position and eighty charaters

# In[7]:


def pretty_print_review_and_label(i):
    print(labels[i] + "\t:\t" + reviews[i][:80] + "...")


# In[8]:


#Viewing the data at various lines:
#print("labels.txt \t : \t reviews.txt\n")
#pretty_print_review_and_label(2137)
#pretty_print_review_and_label(12816)
#pretty_print_review_and_label(6267)
#pretty_print_review_and_label(21934)
#pretty_print_review_and_label(5297)
#pretty_print_review_and_label(4998)


# In[9]:


#importing packages
from collections import Counter
import numpy as np


# We'll create three Counter objects, one for words from postive reviews, one for words from negative reviews, and one for all the words.

# In[10]:


# Creating three Counter objects to store positive, negative and total counts
positive_counts = Counter()
negative_counts = Counter()
total_counts = Counter()


# TODO: We will examine all the reviews. For each word in a positive review, we will increase the count for that word in both positive counter and the total words counter; likewise, for each word in a negative review, we will increase the count for that word in both your negative counter and the total words counter.

# In[12]:


# Looping over all the words in all the reviews and increment the counts in the appropriate counter objects
for i in range(len(reviews)):
    if(labels[i] == 'POSITIVE'):
        for word in reviews[i].split(" "):
            positive_counts[word] += 1
            total_counts[word] += 1
    else:
        for word in reviews[i].split(" "):
            negative_counts[word] += 1
            total_counts[word] += 1


# In[20]:


# Examine the counts of 50 most common words in positive reviews
positive_counts.most_common()[0:50]


# In[21]:


# Examine the counts of 50 most common words in negative reviews
negative_counts.most_common()[0:50]


# As we can see, common words like "the" appear very often in both positive and negative reviews. Instead of finding the most common words in positive or negative reviews, what we really want are the words found in positive reviews more often than in negative reviews, and vice versa. To accomplish this, you'll need to calculate the ratios of word usage between positive and negative reviews.
# 
# TODO: Check all the words you've seen and calculate the ratio of postive to negative uses and store that ratio in pos_neg_ratios.
# 
# ### Approach
# 
# The positive-to-negative ratio for a given word can be calculated with positive_counts[word] / float(negative_counts[word]+1). Notice the +1 in the denominator – that ensures we don't divide by zero for words that are only seen in positive reviews.

# In[15]:


pos_neg_ratios = Counter()

# Calculate the ratios of positive and negative uses of the most common words
# Consider words to be "common" if they've been used at least 100 times
for term,cnt in list(total_counts.most_common()):
    if(cnt > 100):
        pos_neg_ratio = positive_counts[term] / float(negative_counts[term]+1)
        pos_neg_ratios[term] = pos_neg_ratio


# Examining the ratios we've calculated for a few words:

# In[16]:


#print("Pos-to-neg ratio for 'the' = {}".format(pos_neg_ratios["the"]))
#print("Pos-to-neg ratio for 'amazing' = {}".format(pos_neg_ratios["amazing"]))
#print("Pos-to-neg ratio for 'terrible' = {}".format(pos_neg_ratios["terrible"]))


# Looking closely at the values you just calculated, we see the following:
# 
# * Words that we would expect to see more often in positive reviews – like "amazing" – have a ratio greater than 1. The more 
#   skewed a word is toward postive, the farther from 1 its positive-to-negative ratio will be.
# * Words that we would expect to see more often in negative reviews – like "terrible" – have positive values that are less than 
#   1 . The more skewed a word is toward negative, the closer to zero its positive-to-negative ratio will be.
# * Neutral words, which don't really convey any sentiment because we would expect to see them in all sorts of reviews – like 
#   "the" – have values very close to 1. A perfectly neutral word – one that was used in exactly the same number of positive 
#   reviews as negative reviews – would be almost exactly 1. The +1 we suggested you add to the denominator slightly biases words   toward negative, but it won't matter because it will be a tiny bias and later we'll be ignoring words that are too close to     neutral anyway.
# 
# Ok, the ratios tell us which words are used more often in postive or negative reviews, but the specific values we've calculated are a bit difficult to work with. A very positive word like "amazing" has a value above 4, whereas a very negative word like "terrible" has a value around 0.18. Those values aren't easy to compare for a couple of reasons:
# 
# * Right now, 1 is considered neutral, but the absolute value of the postive-to-negative rations of very postive words is larger 
#   than the absolute value of the ratios for the very negative words. So there is no way to directly compare two numbers and see   if one word conveys the same magnitude of positive sentiment as another word conveys negative sentiment. So we should center   all the values around netural so the absolute value fro neutral of the postive-to-negative ratio for a word would indicate     how much sentiment (positive or negative) that word conveys.
# * When comparing absolute values it's easier to do that around zero than one.
# 
# To fix these issues, we'll convert all of our ratios to new values using logarithms.
# 
# ### TODO: 
# 
# Go through all the ratios we calculated and convert them to logarithms. (i.e. use np.log(ratio))
# 
# In the end, extremely positive and extremely negative words will have positive-to-negative ratios with similar magnitudes but opposite signs.

# In[17]:


# Convert ratios to logs
for word,ratio in pos_neg_ratios.most_common():
    pos_neg_ratios[word] = np.log(ratio)


# The following formulas for the calculation extreme values:
# 
# * For any postive words, convert the ratio using np.log(ratio)
# * For any negative words, convert the ratio using -np.log(1/(ratio + 0.01))
# 
# In case that second equation looks strange, here's what it's doing: First, it divides one by a very small number, which will produce a larger positive number. Then, it takes the log of that, which produces numbers similar to the ones for the postive words. Finally, it negates the values by adding that minus sign up front. The results are extremely positive and extremely negative words having positive-to-negative ratios with similar magnitudes but oppositite signs, just like when we use np.log(ratio).

# In[18]:


#Examining the new ratios we've calculated for the same words from before:
#print("Pos-to-neg ratio for 'the' = {}".format(pos_neg_ratios["the"]))
#print("Pos-to-neg ratio for 'amazing' = {}".format(pos_neg_ratios["amazing"]))
#print("Pos-to-neg ratio for 'terrible' = {}".format(pos_neg_ratios["terrible"]))


# We can see neutral words with values close to zero. In this case, "the" is near zero but slightly positive, so it was probably used in more positive reviews than negative reviews. But look at "amazing"'s ratio - it's above 1, showing it is clearly a word with positive sentiment. And "terrible" has a similar score, but in the opposite direction, so it's below -1. It's now clear that both of these words are associated with specific, opposing sentiments.
# 
# The first cell displays the words, ordered by how associated they are with postive reviews. (Notebook will most likely truncate the output so we are taking the first 50 words in the list.)
# 
# The second cell displays the 50 words most associated with negative reviews by reversing the order of the first list and then looking at the first 30 words. (If you want the second cell to display all the words, ordered by how associated they are with negative reviews, you could just write reversed(pos_neg_ratios.most_common()).)
# 
# You should continue to see values similar to the earlier ones we checked – neutral words will be close to 0, words will get more positive as their ratios approach and go above 1, and words will get more negative as their ratios approach and go below -1. That's why we decided to use the logs instead of the raw ratios.

# In[22]:


# Examine the 50 most common words in positive reviews after logarithm scaling
pos_neg_ratios.most_common()[:50]


# In[25]:


# Examine the 50 most common words in positive reviews after logarithm scaling
pos_neg_ratios.most_common()[-50:]


# In[35]:


# Examine the 50 most common words in negative reviews after logarithm scaling
pos_neg_ratios.most_common()[:-50:-1]


# Another approach:
#         words most frequently seen in a review with a "NEGATIVE" label
#         list(reversed(pos_neg_ratios.most_common()))[0:30]

