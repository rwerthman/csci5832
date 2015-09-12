'''
Created on Sep 9, 2015

@author: Bob

Pseudocode
------------

Part 1
-------

Script should take in two arguments: the path to the word list and the path for the hashtag list
(the absolute path needs to be found, not dependent on the os)

Step 1: Read in list of words (read in a maximum of 75000 words) and hashtags
read in a file line by line and find the first alphanumeric word on each line
store each word in a dictionary

Recursive step?
Step 3: break up hashtag in mulitple words using MaxMatch algorithm
find largest word in hashtag from list of words
append it to a string or write it a file without a newline 
repeat until at the end the hashtag
TODO: output maxmatched hashtags to a file

Part 2
---------

Create a working Word Error Rate that takes two files as input: 
    the hashtags outputted by the maxmatch and what the hashtag should really look like based on the english language
    
TODO: change min edit algo to make it work
TODO: Compute WER from result of minimum edit distance divided by length of gold standard list


'''

import re
import sys
import os



def readWordsFromFile(filePath, limitNumWords, numWordsLimit):
    '''
    TODO: docstring
    '''
    wordlist = []
    #create a regular expression to match the first word in a line of the file
    pattern = re.compile('[a-zA-Z]+')
    #read the file into memory
    with open(filePath, 'r') as f:
        #go through the file line by line and get the first word out of each line
        #if we aren't limited by the number of words extract a word out of every line
        if not limitNumWords:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    wordlist.append(match.group(0))
        else:
            for line in f:
                #make sure the number of words in the set is under the number of word limit keep
                #adding them to the set
                if len(wordlist) < numWordsLimit:
                    match = re.search(pattern, line)
                    if match:
                        wordlist.append(match.group(0))
                else:
                    break
                
    return wordlist

def maxMatch(hashtag, wordlist, maxmatchedHashtag):
    '''
    TODO: docstring
    '''
    substringList = []
    largestWord = ""
    #go through each word in the wordlist
    for word in wordlist:
        #make a list of the words from the word list that are
        #in the hashtag 
        if word in hashtag[0:len(word)]:
            substringList.append(word)
    #if the list is not empty then get the largest word out of the substring list, remove it from the hashtag,
    #and call the max match algorithm again on the new hashtag 
    if len(substringList) != 0:
        #find largest string in the substring list
        substringList.sort(key=len, reverse=True)
        largestWord = substringList[0]
        #if there are still characters after the largest word is found 
        #look through the word list again for the next largest word
        if len(largestWord) < len(hashtag):
            maxmatchedHashtag = maxmatchedHashtag + largestWord + " "
            #return is necessary otherwise maxmatchedHashtag is discarded
            return maxMatch(hashtag[len(largestWord):len(hashtag)], wordlist, maxmatchedHashtag)
        #if the largest word is at the end of the hashtag
        #write it out to the output file and end MaxMatch for that hashtag
        elif len(largestWord) == len(hashtag):
            return (maxmatchedHashtag + largestWord)
        else:
            #this is for the largest word being longer than the hashtag
            #which should never happen
            print("Error: this maxMatch function statement should never be reached")
    else:
        #if the list is empty then there are no more words in the word list that fit into the hashtag
        #take the rest of the hash tag and add it to the maxmatchHashtag and return it
        return (maxmatchedHashtag + hashtag)
 

def checkCommandLineArgs(): 
    '''
    TODO: docstring
    ''' 
    #check the user gave the right number of arguments
    #if not print what the user should have given and then exit  
    if len(sys.argv) < 3:
        print("Usage: werthman-assgn1.py <absolute path to file of word list> <absolute path to file of hashtags>")
        sys.exit()
    else:
        #check if the user gave the absolute path for both files otherwise print script usage and exit
        if os.path.isabs(sys.argv[1]) == False and os.path.isabs(sys.argv[2]) == False:
            print("Usage: werthman-assgn1.py <absolute path to file of word list> <absolute path to file of hashtags>")
            sys.exit()
        else:
            #if the user gave the right number of arguments and both absolute paths return them
            return (sys.argv[1], sys.argv[2])     

def  minEditDist(target, source):
    ''' Computes the min edit distance from target to source. Figure 3.25 in the book. Assume that
    insertions, deletions and (actual) substitutions all cost 1 for this HW. Note the indexes are a
    little different from the text. There we are assuming the source and target indexing starts a 1.
    Here we are using 0-based indexing.'''
    
    #number of rows of the matrix/table
    n = len(target)
    #number of columns of the matrix/table
    m = len(source)

    #create the n by m matrix 
    distance = [[0 for i in range(m+1)] for j in range(n+1)]
    
    #create the base cases of the matrix 
    #which ends up being the length of each substring
    #1 2 3 4... down the rows
    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + 1
    
    #1 2 3 4... across the columns
    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + 1
    
    #fill in the rest of the matrix with costs
    #insertions = 1, delete = 1, substitution = 0 if the words are equal, 2 if they are not
    for i in range(1,n+1):
        for j in range(1,m+1):
            distance[i][j] = min(distance[i-1][j] + 1,
                                 distance[i][j-1] + 1,
                                 distance[i-1][j-1]+substCost(source[j-1],target[i-1]))
    return distance[n][m]

def substCost(source, target):
    if source == target:
        return 0
    else:
        return 1

def main():

    #check that the user gave the right number of arguments and absolute paths
    (wordlistPath, hashtaglistPath) = checkCommandLineArgs()
    print("Path to the word list: " + wordlistPath)
    print("Path to the hashtag list: " + hashtaglistPath)
    
    wordlist = readWordsFromFile(wordlistPath, True, 75000)
    hashtaglist = readWordsFromFile(hashtaglistPath, False)
    
    '''
    TODO: output maxmatch computed hashtags to a file
    '''
    
if __name__ == '__main__':
    main()