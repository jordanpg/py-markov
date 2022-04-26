from genericpath import exists
import os
import tkinter as tk
from tkinter import BOTH, END, HORIZONTAL, LEFT, TOP, Y, X, IntVar, StringVar, ttk
from tkinter import filedialog
from tkinter.font import BOLD
from pymarkov import markov
from pymarkov.vis import visualize_markov

m: markov.Markov = markov.Markov(2)

def replace_markov(order: int):
    global m
    m = markov.Markov(order)

def build_chat(parent):
    """Build chat UI"""
    global m
    
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
        global m
        # print(m)
        inp = chat_input.get().strip()
        if len(inp) > 0:
            m.process_text_ngram(inp)
            add_line(f'You: {inp}')
        add_line(f"AI: {m.generate_text_ngram(25)}")
        chat_input.set('')
        
    add_line('Start typing to train and chat with the bot! Or, press enter to make the AI generate a sentence.')
    centry.bind('<Return>', chat_respond)
    
    return f, add_line

def build_train(parent):
    """Build training window"""
    global m
    
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
    
    orderf = ttk.Frame(f)
    orderf.pack(expand=True)
    orderl = ttk.Label(orderf, text="Order (-1 for sentence model) ")
    order = IntVar(value=2)
    
    def order_set():
        o = order.get()
        if o < 1 and o != -1:
            statustext.set('Order must be greater than zero or -1!')
            return
        replace_markov(o)
        statustext.set(f'Model remade with order k={o}' + ' (Sentence model)' if o == -1 else '')
    
    orderentry = ttk.Entry(orderf, textvariable=order)
    orderbtn = ttk.Button(orderf, command=order_set, text="Remake Model (TRAINING ERASED)")
    orderl.pack(side=LEFT)
    orderentry.pack(side=LEFT)
    orderbtn.pack(side=LEFT)
    
    visbtn = ttk.Button(f, text='Visualize', command=(lambda: visualize_markov(m)))
    visbtn.pack(expand=True)
    
    def train(path: str):
        if not exists(path):
            statustext.set(f"File '{path}' does not exist!")
            return
        
        len_a = len(m)
        statustext.set('Reading...')
        size = os.path.getsize(path)
        prog = 0
        with open(path, 'r', encoding='utf-8') as file:
            line = file.readline()
            statustext.set(f'Processing {prog/size}, {prog} of {size} ...')
            while line:
                m.process_text_ngram(line)
                prog += len(line.encode('utf-8'))
                statustext.set(f'Processing {prog/size}, {prog} of {size}...')
                line = file.readline()
        len_b = len(m)
        statustext.set(f"Added {len_b - len_a} nodes!")
        
    trainbtn.configure(command=(lambda: train(filepath.get())))
    
    return f

def build_text(parent):
    """Build text generator"""
    global m
    f = ttk.Frame(parent)
    f.pack(expand=True, fill=BOTH)
    
    lf = ttk.Frame(f)
    lf.pack(expand=True, fill=BOTH)
    text = tk.Text(lf)
    yscroll = ttk.Scrollbar(lf, orient='vertical', command=text.yview)
    text['yscrollcommand'] = yscroll.set
    text.pack(side=LEFT, fill=BOTH, expand=True)
    yscroll.pack(side=LEFT, fill=Y)
    
    def generate():
        global m
        out = m.generate_text_ngram(50,text.get('1.0',END))
        text.insert(END, out + ' ')
        
    pf = ttk.Frame(f)
    pf.pack(fill=X)
    gen_btn = ttk.Button(pf, text="Generate", command=generate)
    gen_btn.pack(side=LEFT,fill=X,expand=True)
    
    return f

def build_gui():
    """Build main window"""
    root = tk.Tk()
    root.title("Markov Experiments")
    nb = ttk.Notebook(root)
    chat, add_line = build_chat(nb)
    train = build_train(nb)
    text = build_text(nb)
    nb.add(chat, text='Chatbot')
    nb.add(text, text='Prompt')
    nb.add(train, text='Training')
    
    
    nb.pack(expand=True,fill=BOTH)
    
    return root, add_line
    
def main():
    root, add_line = build_gui()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()