from genericpath import exists
import tkinter as tk
from tkinter import BOTH, HORIZONTAL, LEFT, TOP, Y, X, StringVar, ttk
from tkinter import filedialog
from tkinter.font import BOLD
from pymarkov import markov
from pymarkov.vis import visualize_markov

def build_chat(parent, m: markov.Markov):
    """Build chat UI"""
    f = ttk.Frame(parent)
    f.pack(expand=True,fill=BOTH)
    logframe = ttk.Frame(f)
    logframe.pack(expand=True,fill=BOTH)
    log = tk.Text(logframe)
    log.pack(side=LEFT,fill=BOTH)
    ys = ttk.Scrollbar(logframe, orient='vertical', command=log.yview)
    log['yscrollcommand'] = ys.set
    ys.pack(side=LEFT,fill=Y)
    
    chat_input = StringVar()
    centry = ttk.Entry(f, textvariable=chat_input)
    centry.pack(side=TOP,fill=X)

    def add_line(msg: str):
        """Add a line of text to the output"""
        log['state'] = 'normal'
        log.insert('end', msg + '\n')
        log.see('end')
        log['state'] = 'disabled'
        
    def chat_respond(_):
        """Handle chatbot text entry and response"""
        inp = chat_input.get().strip()
        if len(inp) > 0:
            m.process_text(inp)
            add_line(f'You: {inp}')
        add_line(f"AI: {' '.join(m.generate())}")
        chat_input.set('')
        
    add_line('Start typing to train and chat with the bot! Or, press enter to make the AI generate a sentence.')
    centry.bind('<Return>', chat_respond)
    
    return f, add_line

def build_train(parent, m: markov.Markov):
    """Build training window"""
    f = ttk.Frame(parent)
    f.pack(expand=True,fill=BOTH)
    
    desc = ttk.Label(f, text="Here, you can import a file to train the Markov model with some sample text!", anchor='n')
    desc.pack(fill=X)
    
    fsf = ttk.Frame(f)
    fsf.pack(fill=X)
    
    filepath = StringVar()
    entry = ttk.Entry(fsf, textvariable=filepath)
    entry.pack(side=LEFT,expand=True, fill=X)

    selectbtn = ttk.Button(fsf, text='Browse...', command=(
        lambda: filepath.set(filedialog.askopenfilename(title='Open training file', initialdir='.'))
        ))
    selectbtn.pack(side=LEFT)
    
    trainbtn = ttk.Button(f, text='Train')
    trainbtn.pack(expand=True)
    
    statustext = StringVar()
    status = ttk.Label(f, textvariable=statustext)
    status.pack(expand=True)
    
    visbtn = ttk.Button(f, text='Visualize', command=(lambda: visualize_markov(m)))
    visbtn.pack(expand=True)
    
    def train(path: str):
        if not exists(path):
            statustext.set(f"File '{path}' does not exist!")
            return
        
        len_a = len(m)
        statustext.set('Reading...')
        with open(path, 'r') as file:
            txt = file.readlines()
            statustext.set('Processing...')
            for line in txt:
                m.process_text(line)
        len_b = len(m)
        statustext.set(f"Added {len_b - len_a} nodes!")
        
    trainbtn.configure(command=(lambda: train(filepath.get())))
    
    return f

def build_gui(m: markov.Markov):
    """Build main window"""
    root = tk.Tk()
    root.title("Markov Experiments")
    nb = ttk.Notebook(root)
    chat, add_line = build_chat(nb, m)
    train = build_train(nb, m)
    nb.add(chat, text='Chatbot')
    nb.add(train, text='Training')
    
    nb.pack(expand=True,fill=BOTH)
    
    return root, add_line
    
def main():
    m = markov.Markov()
    root, add_line = build_gui(m)
    
    root.mainloop()
    
if __name__ == "__main__":
    main()