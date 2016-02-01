"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list2 =[]
    if len(list1) == 0 :
        return []
    list2.append(list1[0])
    for idx in range(1,len(list1)):
        if list1[idx - 1] != list1[idx]:
            list2.append(list1[idx])
    return list2

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list3 = []
    for item1 in list1 :
        if (item1 in list2) and (item1 not in list3) :
            list3.append(item1)
    return list3

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    list3 = list(list1)
    for item2 in list2:
        item_idx = 0
        for idx in range(len(list3)):
            if item2 > list3[idx]: 
                item_idx += 1
            else:
                break
        list3.insert(item_idx, item2)
    return list3
            
            
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    length = len(list1)
    if length < 2 :
        return list(list1)
    else:
        return merge(merge_sort(list1[:length/2]), merge_sort(list1[length/2:]))
        
    
    

# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [word]    
    elif len(word) == 1:
        return ["", word]
    else:
        first = word[0]
        rest_strings = gen_all_strings(word[1:])
        tmp = []
        for string in rest_strings:            
            for idx in range(len(string)):
                tmp.append(string[:idx]+first+string[idx:])
            tmp.append(string + first)
        tmp.extend(rest_strings)
        return tmp
    

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
## run()
#print range(-1)
###print merge([1,2,2,4,4,5,6,7],[2,3,3,5,8,9])    
##print merge([3, 4, 5], [3, 4, 5])
##a = range(5)
##print a[:4]
#print merge([2],[2])
#print merge_sort([20, 9,8,9, 10,4,5,4, 2])
#print gen_all_strings("")
#print gen_all_strings("b")
#print gen_all_strings("ab")
#print gen_all_strings("abc")
#
#print len(['', 'd', 'd', 'dd', 'dd', 'g', 'gd', 'dg', 'gd', 'dg', 'gdd', 'dgd', 'ddg', 'gdd', 'dgd', 'ddg', 'g', 'gd', 'dg', 'gd', 'dg', 'gdd', 'dgd', 'ddg', 'gdd', 'dgd', 'ddg', 'gg', 'gg', 'ggd', 'ggd', 'gdg', 'gdg', 'dgg', 'dgg', 'ggd', 'ggd', 'gdg', 'gdg', 'dgg', 'dgg', 'ggdd', 'ggdd', 'gdgd', 'gddg', 'gdgd', 'dggd', 'dggd', 'dgdg', 'gddg', 'dgdg', 'ddgg', 'ddgg', 'ggdd', 'ggdd', 'gdgd', 'gddg', 'gdgd', 'dggd', 'dggd', 'dgdg', 'gddg', 'dgdg', 'ddgg', 'ddgg'])
#print len(['ggd', 'ggd', 'gdg', 'gdg', 'dgg', 'dgg', 'ggdd', 'ggd', 'dgd', 'gddg', 'gdgd', 'dgg', 'ggd', 'dgdg', 'gddg', 'dgd', 'dgg', 'ddgg', 'ggdd', 'ggd', 'dgd', 'gddg', 'gdgd', 'dgg', 'ggd', 'dgdg', 'gddg', 'dgd', 'dgg', 'ddgg', 'gg', 'gg', 'ggd', 'ggd', 'gdg', 'gdg', 'dgg', 'dgg', 'gd', 'dg', 'gdd', 'dgd', 'ddg', 'gdd', 'dgd', 'ddg', 'g', 'gd', 'dg', 'gd', 'dg', 'gdd', 'dgd', 'ddg', 'gdd', 'dgd', 'ddg', 'g', 'gd', 'dg', 'd', 'dd', 'dd', '', 'd'])
#string = "abc"
#first = "0"
#tmp =[]
#for idx in range(len(string)):
#    tmp.append(string[:idx]+first+string[idx:])
#
#print tmp    
#    
#    
    
    
    
    
    
    
    
    
    