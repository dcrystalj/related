import re

def filtertxt(txt):

    txt = txt.lower()

    #remove common_words
    txt = re.sub('(in )|(the )|(or )|(and )|(/\n)|(on )', '', txt)

    #remove space
    txt = re.sub('(  )+|(   )+', ' ', txt)

    #remove special chars
    txt = re.sub('[!?,."):/\-\'(\^123456789]', '',txt)
    return txt