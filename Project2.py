#!/usr/bin/env python
# coding: utf-8

# # Project 2: Creating the Input/Output Data
# ### Importing previous step

# In[5]:


from Project1 import *


# # Transforming Text into Numbers and Visualizing Neural Network

# In[6]:


from IPython.display import Image

review = "This was a horrible, terrible movie."

Image(filename='sentiment_network.png')


# In[15]:


review = "The movie was excellent"
Image(filename='sentiment_network_pos.png')


# In[10]:


# Creating a set named vocab that contains every word in the vocabulary.
vocab = set(total_counts.keys())


# In[11]:


# Checking the Vocabulary size in vocab set
vocab_size = len(vocab)
#print(vocab_size)


# In[16]:


Image(filename='sentiment_network_2.png')
#It represents the layers of the neural network we'll be building throughout this notebook. 
#layer_0 is the input layer, layer_1 is a hidden layer, and layer_2 is the output layer.


# ### TODO: 
# 
# Create a numpy array called layer_0 and initialize it to all zeros. We will find the zeros function particularly helpful here. We will create layer_0 as a 2-dimensional matrix with 1 row and vocab_size columns.

# In[17]:


layer_0 = np.zeros((1,vocab_size))
layer_0.shape


# layer_0 contains one entry for every word in the vocabulary, as shown in the above image. We need to make sure we know the index of each word, Below cell to create a lookup table that stores the index of every word.

# In[34]:


# Create a dictionary of words in the vocabulary mapped to index positions 
# (to be used in layer_0)
word2index = {}
for i,word in enumerate(vocab):
    word2index[word] = i
    
# display the map of words to indices #word2index will show all words
#print(word2index['the'])
#print(word2index['simultaneously'])
#print(word2index['unmelodious'])


# TODO: Complete the implementation of update_input_layer. It should count how many times each word is used in the given review, and then store those counts at the appropriate indices inside layer_0.

# In[29]:


def update_input_layer(review):
    """ Modify the global layer_0 to represent the vector form of review.
    The element at a given index of layer_0 should represent
    how many times the given word occurs in the review.
    Args:
        review(string) - the string of the review
    Returns:
        None
    """
     
    global layer_0
    
    # clear out previous state, reset the layer to be all 0s
    layer_0 *= 0
    
    # count how many times each word is used in the given review and store the results in layer_0 
    for word in review.split(" "):
        layer_0[0][word2index[word]] += 1


# Updating the input layer with the first review. The indices assigned may not be the same as in the solution, but hopefully we'll see some non-zero values in layer_0.

# In[30]:


update_input_layer(reviews[0])
layer_0


# TODO: Complete the implementation of get_target_for_labels. It should return 0 or 1, depending on whether the given label is NEGATIVE or POSITIVE, respectively.

# In[35]:


def get_target_for_label(label):
    """Convert a label to `0` or `1`.
    Args:
        label(string) - Either "POSITIVE" or "NEGATIVE".
    Returns:
        `0` or `1`.
    """
    if(label == 'POSITIVE'):
        return 1
    else:
        return 0


# In[36]:


labels[0]


# In[37]:


get_target_for_label(labels[0])


# In[38]:


labels[1]


# In[39]:


get_target_for_label(labels[1])


# In[ ]:




