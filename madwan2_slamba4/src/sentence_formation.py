from nltk.tokenize import sent_tokenize

incorrect_rules = [
"(ROOT (SBAR", # (done)
"(SBAR (S", #(DONE)
"(FRAG", #(Done)
"(SINV (V" # starts with V (DONE)
"(ROOT !(S" # not S after root (DOne)
]

''' Function to check the correct sentence formation of each sentence in the essay
Params: dot_processed_sentences - proper formatted sentencesself
        nlp - stanfordcorenlp object

returns - number of errors
'''
def check_sentence_formation(dot_processed_sentences, nlp):
    num_errors = 0
    for sentence in dot_processed_sentences:
        pos_tags = nlp.pos_tag(sentence)
        parse_tree_string = nlp.parse(sentence)
        parse_tree = parse_tree_string.split()
        line_parse_tree = parse_tree_string.split('\n')
        for item_index, item in enumerate(line_parse_tree):
            line_parse_tree[item_index] = item.strip() # removes trailing and preceding spaces

        if '(ROOT' in parse_tree:
            temp_index = parse_tree.index('(ROOT')
            try:
                ''' correct Rule - (ROOT (S '''
                if '(S' not in parse_tree[temp_index + 1]:
                    # print('1. -------------',parse_tree)
                    # print(sentence)
                    # print('*******************************')
                    num_errors += 1
                    continue
                # ''' incorrect Rule - (ROOT (SBAR '''
                elif parse_tree[temp_index + 1] == '(SBAR':
                    # print('2. -------------',parse_tree)
                    # print(sentence)
                    # print('*******************************')
                    num_errors += 1
                    continue
                elif parse_tree[temp_index + 1] == '(SINV':
                    ''' incorrect Rule - (ROOT (SINV starts with (V'''
                    if '(V' in parse_tree[temp_index + 2]:
                        # print('3. -------------',parse_tree)
                        # print(sentence)
                        # print('*******************************')
                        num_errors += 1
                        continue
            except:
                pass
        ''' FRAG should not be present '''
        if '(FRAG' in parse_tree:
            # print('4. -------------',parse_tree)
            # print(sentence)
            # print('*******************************')
            num_errors += 1
            continue
        if "(SBAR" in line_parse_tree:
            temp_index = line_parse_tree.index('(SBAR')
            try:
                ''' correct rule - (NP/(VP (SBAR (S '''
                if '(S' in line_parse_tree[temp_index + 1]:
                    if '(NP' not in line_parse_tree[temp_index - 1] and '(VP' not in line_parse_tree[temp_index - 1]:
                        # print('5. -------------',line_parse_tree)
                        # print(sentence)
                        # print(line_parse_tree[temp_index - 2 : temp_index + 3])
                        # print(parse_tree_string)
                        # print('*******************************')

                        num_errors += 1
                        continue
            except:
                pass
    return num_errors
