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
        
if __name__ == "__main__":
    main()