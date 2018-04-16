import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import os
import re

def count_sentences():

    ''' Get the list of sentences'''
    sentences = sent_tokenize(one_essay)
    tagged_sentences = []
    processed_sentences = []

    ''' Convert all the sentences which have new line char into multiple sentences '''
    for sentence_index, sentence in enumerate(sentences):
        temp_sentence = sentence.strip().replace('\n\n', '\n').replace('\n\n\n', '\n')

        for split_sentence in temp_sentence.split('\n'):
            processed_sentences.append(split_sentence.strip())

    ''' if a dot has a alpha after it, consider it as a new line '''
    dot_processed_sentences = []
    for sentence_index, sentence in enumerate(processed_sentences):
        temp_sentence = sentence
        temp_sentences_list = []
        dot_index = 0
        while dot_index < len(temp_sentence) - 1:
            dot_index = temp_sentence.find('.', dot_index)
            if dot_index == -1:
                temp_sentences_list.append(temp_sentence)
                break
            ''' if the next char after . is alpha and there should be atleast 2 characters after the . '''
            if dot_index < len(temp_sentence) - 3:
                if temp_sentence[dot_index + 1].isalpha() and temp_sentence[dot_index - 1] != '.':
                    temp_sentences_list.append(temp_sentence[:dot_index+1])
                    temp_sentence = temp_sentence[dot_index+1:]
                    dot_index = 0
            else:
                temp_sentences_list.append(temp_sentence)
                break
            dot_index = dot_index + 1

        for dot_sentence in temp_sentences_list:
            dot_processed_sentences.append(dot_sentence)


    temp_flag = False

    ''' Processing based on POS tags and finite verb '''
    for sentence_index, sentence in enumerate(dot_processed_sentences):
        ''' Get the pos tag in each sentence after tokenizing it'''
        tagged_sentences.append(pos_tag(word_tokenize(sentence.strip())))

        ''' To process the sentences more by POS tags and capitalization '''
        for tagged_token_index, tagged_token in enumerate(tagged_sentences[sentence_index]):
            if tagged_token_index != 0: # Ignore 1st word
                '''
                    The previous tag should be alpha and not characters (: , ")
                    and it shouldn't be CC (coordinate conjunction) or IN (subordinate conjunction)
                    otherwise it will be a valid sentence.
                '''
                if tagged_sentences[sentence_index][tagged_token_index - 1][1].isalpha() and tagged_sentences[sentence_index][tagged_token_index - 1][1] != 'CC' and tagged_sentences[sentence_index][tagged_token_index - 1][1] != 'IN':
                    '''
                        Capitalization logic. If the word is capitalized and not an I or proper noun or noun then new sentence
                        (Doesn't work. Only 2 percent accuracy. will have more negative effect than positive)

                    # if tagged_token[0][0].isupper() and tagged_token[0] != 'I' and tagged_token[1] != 'NNP'
                    if tagged_token[0][0].isupper() and tagged_token[0] != 'I' and tagged_token[1] != 'NNP' and tagged_token[1] != 'NN' and tagged_token[1] != 'NNS':
                        # temp_flag = True
                        print(filename)
                        print(tagged_sentences[sentence_index][tagged_token_index - 1][1])
                        print(tagged_sentences[sentence_index])
                        print(sentence)
                        print(tagged_token)

                    '''
                    pass

    if temp_flag and filename_index > 0:
        print('------------------------------------------------------------------------------------')
        print(filename)
        print(sentences)
        print(one_essay)
        print('************************************************************************************************************************************************')


''' Get the list of filenames to iterate over one by one'''
filenames = os.listdir('essays_dataset/essays/')
# filename = 'essays_dataset/essays/' + '38209.txt'
print(len(filenames))
for filename_index, filename in enumerate(filenames):
    filepath = 'essays_dataset/essays/' + filename

    ''' Read file '''
    file = open(filepath, 'r')
    one_essay = file.read()

    count_sentences()

    print("******************ENd of", filename_index, "essay *********************************************")
    file.close()
    if filename_index == 90:
        # break
        pass
