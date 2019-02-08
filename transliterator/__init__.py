d = {}

d[' '] = ['_', ' ','']
d['-'] = ['_', ' ','']
d['_'] = ['_', ' ','']

# note: sometimes a disappears when in middle of word because short vowel
#            alif   alif-hamza   3ayn   ta-marbuta alif-maqsura
d['a'] = [u'\u0627',u'\u0623',u'\u0639',u'\u0629',u'\u0649','']

#             ba
d['b'] = [u'\u0628']

#             dal     dal with space after
d['d'] = [u'\u062f',u'\u062f ']

#            alif   alif-hamza    ya
d['e'] = [u'\u0627',u'\u0623',u'\u064a','']

#            fa
d['f'] = [u'\u0641']

#            g/jim
d['g'] = [u'\u062c']

#           heavy-ha, soft he
d['h'] = [u'\u062d',u'\u0647','']

#                  ya     alif kasra
d['i'] = [u'\u064a', u'\u0625','']

#           gim/jja
d['j'] = [u'\u062c']

#             lam
d['l'] = [u'\u0644']

#             mim
d['m'] = [u'\u0645']

#                noon
d['n'] = [u'\u0646','']

#                waw
d['o'] = [u'\u0648','']

#             ra     # sometimes r-repeated like hurriya
d['r'] = [u'\u0631',u'']

#             sin     shim    elided-lam   saad
d['s'] = [u'\u0633',u'\u0634',u'\u0644',u'\u0635']

#             shim
d['sh'] = [u'\u0634']

#         tar-mabuta  deep-taa
d['t'] = [u'\u0629',u'\u0637']

#             waw      alif
d['u'] = [u'\u0648',u'\u0627','']

#             waw
d['w'] = [u'\u0648']

#             ya
d['y'] = [u'\u064a']

#             za
d['z'] = [u'\u0632','']

#for key, values in d.iteritems():
#    d['key'] = values + [ v+" " for v in values]

english_to_arabic = d



from re import findall, IGNORECASE, MULTILINE, UNICODE 
flags = IGNORECASE|MULTILINE|UNICODE


# tries to transliterate if you give it some text as a hint
# if a word matches the pattern in the text it returns the word
# if not, it returns an empty list
def get_transliterations_from_text(string, from_, to_, text):
    print("starting get_transliterations_from_text with", [string], "from", from_, "to", to_)
    length_of_string = len(string)
    pattern_as_string = get_transliteration_as_pattern(string, from_, to_)
    transliterations = set()
    for found in findall(pattern_as_string, text, flags=flags):
        if len(found) > 0.6 * len(string):
            transliterations.add(found)
    transliterations = list(transliterations)
    print("finishing get_transliterations_from_text with", transliterations)
    return transliterations

# PROBLEM: when word has too many optionally missed things
# should probably make it so word length has to be at least a certain length

def get_transliteration_as_pattern(string, from_, to_):
    print('\nstarting get_transliteration_as_pattern with', [string], "from ", from_, "to", to_)

    if isinstance(string, str):
        string = string.decode("utf-8")

    words = string.lower().split()
    from_ = from_.lower()
    to_ = to_.lower()

    char_to_variations = english_to_arabic
    print("char_to_variations is", char_to_variations)
    pattern_as_string = ""
    for index_of_word, word in enumerate(words):
        if index_of_word != 0:
            pattern_as_string += '(?:' + '|'.join(char_to_variations[" "]) + ')' # adds space
        #pattern_as_string += u"(?<=\\b)"
        for char in word:
            if char in char_to_variations:
                pattern_as_string += '(?:' + '|'.join(char_to_variations[char]) + ')'
            else:
                #pattern_as_string += '(.*)'
                pattern_as_string += char
        #pattern_as_string += u"(?=\\b)"
        pattern_as_string += u"(?<=[^ ]{2})"

    if from_=="arabic" and to_=="english":
        # sometimes n doesn't appear in arabic, so put it on the end just in case
        pattern_as_string += "(|n)"

    print("pattern_as_string = ", [pattern_as_string])
    return pattern_as_string

gtap = get_transliteration_as_pattern
