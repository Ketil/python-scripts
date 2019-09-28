#!/usr/bin/env python3
'''Simple program doing markov analysis of text, based on state of the previous
words, and generates text based on that. '''
import sys
import random
import re


def add_space(text):
    '''Adds space before punctuation to separate it from a word'''
    return re.sub(r'([!,.:;?])', r' \1', text)


def remove_space(text):
    '''Remove space before punctuation to make it
    nicer to read'''
    return re.sub(r'\s+([!,.:;?])', r'\1', text)


def analysis(filename, order=2):
    '''Analyse file with markov chain of the specified order. Memory state
    is the last words at the current position.'''
    freq_table = {}
    sum_table = {}
    state = [' ' for x in range(order)]

    file_content = open(filename).read()
    file_content = add_space(file_content).lower()
    split_content = file_content.split()
    for word in split_content:
        tup = tuple(state)
        freq_table[tup] = freq_table.get(tup, {})
        freq_table[tup][word] = freq_table[tup].get(word, 0) + 1
        sum_table[tup] = sum_table.get(tup, 0) + 1
        state = state[1:] + [word]
    if not freq_table:
        raise ValueError('File should have more text')
    return freq_table


def generate(freq_table, max_i):
    '''Generate up to max_i words based on frequency table. It will stop if
    there is no valid word based on the current state.

    freq_table = {
        state0=(word0, word1, ...):
            [ (word2, frequency_of_word2_given_state),
              (word3, frequency_of_word3_given_state),
              ...
            ],
        state1=(word4, word5, ...): [(word6, frequency_of_word6_given_state)],
        ...
        }
    All state tuples must be of the same length.'''

    # Find a start state at the end of a sentence.
    for state in freq_table:
        if state[-1] == '.':
            break
    i = 0
    text = []
    while state in freq_table and i < max_i:
        i += 1
        word = []
        prob = []
        for key in freq_table[state]:
            word.append(key)
            prob.append(freq_table[state][key])

        word = random.choices(word, weights=prob)
        append = word[0]
        if state[-1] == '.':
            append = append.capitalize()
        state = tuple(list(state)[1:] + word)
        text.append(append)
    return text


def usage():
    '''Print usage instructions'''
    print('Usage {} FILE [ORDER]'.format(sys.argv[0]))


def main():
    '''Main program when run as script'''
    order = 2
    if len(sys.argv) > 2:
        order = int(sys.argv[2])
    if len(sys.argv) > 1:
        file = sys.argv[1]
        table = analysis(file, order)
        text = generate(table, 50000)
        print(remove_space(' '.join(text)))
    else:
        usage()


if __name__ == "__main__":
    main()
