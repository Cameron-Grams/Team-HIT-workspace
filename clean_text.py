import re
import spacy



def clean_text(text_list):
    """
    cleans twitter text for use in classification
    indended to be imported and used as a function with the following:
    requires:
    - regex re library in scope
    - spacy library in scope

    arguments: 
    - list of strings; the text passages that will be classified

    returns:
    - list of sentences which have been lemmatized and had punctuation
      removed; @ symbols were retained 

    """
    # import the nlp model
    nlp = spacy.load("en_core_web_lg")

    # list of punctuation symbols 
    p = "\!|\"|\$|\%|\&|\\|\'|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\|\?|\[|\\|\\|\]|\^|\_|\`|\{|\||\}|\~|\?|\#"
    # compiled symbols to work on multiple lines

    reg = re.compile(p, re.MULTILINE)

    # helper function to apply punctuation removal
    punct_less = lambda x: re.sub(reg, "", x)

    # control the nlp generator 
    vectorize = True

    # final list of sentences to be returned
    clean_tokens = []

    # generator of nlp documents
    text_pipe = nlp.pipe(text_list)

    while vectorize == True:
        try:
            tweet_ = next(text_pipe)
            clean_list = [punct_less(word.lemma_).strip() for word in tweet_]
            clean_text = ' '.join(clean_list)
            clean_tokens.append(clean_text) 
        except:
            print(f"Completed Text with {len(clean_tokens)} vectors.")
            vectorize = False
    return clean_tokens    


