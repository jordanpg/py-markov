from pymarkov import markov

def main():
    m = markov.Markov()
    inp = ""
    print("Type _e to exit")
    while inp != "_e":
        inp = input("You: ")
        m.process_text(inp)
        out = m.generate()
        print('AI: ' + ' '.join(out))
        
def main_ngram(o = 1):
    m = markov.Markov(o)
    inp = ""
    print("Type _e to exit")
    while inp != "_e":
        inp = input("You: ")
        m.process_text_ngram(inp)
        out = m.generate_text_ngram(25)
        print('AI: ' + out)

if __name__ == "__main__":
    main_ngram(2)