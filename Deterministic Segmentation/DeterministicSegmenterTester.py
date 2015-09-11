'''
Created on Sep 11, 2015

@author: Bob
'''
import DeterministicSegmenter

def assertion(boolean, testName):
    if boolean:
        print(testName + " PASSED")
    else:
        print(testName + " FAILED")
        
def createWordAndHashtagFiles():
    wordlist = ['moon 5678', 'man 1234', 'over 345', 'the 5678', 'help 777777', 'me 9999',
                 't 7777', 'fi 9999']
    hashtaglist = ['#manoverthemoon', '#helpmeoverthere', '#findmefood', '#whaaaaat']
    
    #create the file with the test words
    with open('testwordlist.txt', 'w') as f:
        for word in wordlist:
            f.write('{0}\n'.format(word))
    
    #create the file with the test hashtags     
    with open('testhashtaglist.txt', 'w') as f:
        for hashtag in hashtaglist:
            f.write('{0}\n'.format(hashtag))
              
              
def testReadWordsFromFile():
    testwordlist = ['moon', 'man', 'over', 'the', 'help', 'me',
                 't', 'fi']
    testhashtaglist = ['manoverthemoon', 'helpmeoverthere', 'findmefood', 'whaaaaat']
    createWordAndHashtagFiles()
    hashtaglist = DeterministicSegmenter.readWordsFromFile('testhashtaglist.txt', False, 20)
    wordlist =  DeterministicSegmenter.readWordsFromFile('testwordlist.txt', True, 20)
    
    #tests that the right words and hashtags are in the lists
    for word in wordlist:  
        assertion(word in testwordlist, "Set contains {0}.".format(word))
        
    for hashtag in hashtaglist:  
        assertion(hashtag in testhashtaglist, "Set contains {0}.".format(hashtag))
    
    #test that the word list is limited by a certain size
    wordlist = DeterministicSegmenter.readWordsFromFile('testwordlist.txt', True, 2)
    assertion(len(wordlist) == 2, "Word list should be size 2.")
    
def testMaxMatchAlgo():
    testwordlist = ['moon', 'man', 'over', 'the', 'help', 'me',
                 't', 'fi']
    testhashtaglist = ['manoverthemoon', 'helpmeoverthere', 'findmefood', 'whaaaaat']
    for hashtag in testhashtaglist:
        maxmatchedHashtag = ""
        if hashtag == "manoverthemoon":
            #test for the hashtag being made up of entirely of words in the word list
            maxmatchedHashtag = DeterministicSegmenter.maxMatch("manoverthemoon", testwordlist, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "man over the moon", "manoverthemoon should be changed to man over the moon.")
        elif hashtag == "helpmeoverthere":
            #test for the hashtag being made up of some words from the word list
            maxmatchedHashtag = DeterministicSegmenter.maxMatch("helpmeoverthere", testwordlist, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "help me over the re", "helpmeoverthere should be changed to help me over the re.")
        elif hashtag == "whaaaaat":
            #test for the hashtag being made up of none of the words in the wordlist
            maxmatchedHashtag = DeterministicSegmenter.maxMatch("whaaaaat", testwordlist, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "whaaaaat", "whaaaaat should be changed to whaaaaat.")
        elif hashtag == "findmefood":
            #test for the hashtag being made up of none of the words in the wordlist
            maxmatchedHashtag = DeterministicSegmenter.maxMatch("findmefood", testwordlist, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "fi ndmefood", "findmefood should be changed to fi ndmefood.")
            
def main():
    testReadWordsFromFile()
    testMaxMatchAlgo()
    
    
if __name__ == '__main__':
    main()