"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    occurrences = []  
    for die in hand:
        if die > len(occurrences):
           occurrences.extend([0 for dummy_idx in range(len(occurrences) ,die)]) 
        occurrences[die - 1] += 1
    maxi = 0
    for idx in range(len(occurrences)):
        if (idx+1) * occurrences[idx] > maxi:
            maxi = (idx + 1) * occurrences[idx]
    return maxi

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [number+1 for number in range(num_die_sides)]
    die_seqs = list(gen_all_sequences(outcomes, num_free_dice))
    for idx in range(len(die_seqs)):
        seq = list(die_seqs[idx])
        seq.extend(list(held_dice))
        die_seqs[idx] = tuple(seq)
    scr = 0.0
    for seq in die_seqs:
        scr += score(seq)  
    return scr / len(die_seqs)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    answer_set = set([()])
    for dummy_idx in range(len(hand)):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in range(1,len(hand)+1):
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                if set(tuple(new_sequence)).issubset(set(range(1,len(hand)+1))):
                    temp_set.add(tuple(set(new_sequence)))
        answer_set = answer_set.union(temp_set)
    answer_set2 = set([()])
    for seq in answer_set:
        temp_seq = []
        for element in seq:            
            temp_el = hand[element -1]
            temp_seq.append(temp_el)
        answer_set2.add(tuple(temp_seq))
    return answer_set2    

            

    

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    #return (0.0, ())
    maxval = 0.0
    maxseq= ()
    allholds = gen_all_holds(hand)
    for seq in allholds:
        val = expected_value(seq, num_die_sides, len(hand)-len(seq))
        if val > maxval:
            maxval = val
            maxseq = seq
            
        
        
    return (maxval, maxseq)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

        
    

#print gen_all_sequences((1,2,3),2)
#print gen_all_holds((4, 4, 3))
#print set([1,1]).issuperset(set([2, 1]))
#def get_all_lists(hand,length)
#print range(len((1,4)))
#print strategy((1, 2), 6)
