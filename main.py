import tkinter as tk, threading, pdf_parser, calculate_total, apartments

def main():
    try:
        pdf_parser.main()

        calculate_total.main()
        
        apartments.main()
        
    except Exception as e:
        print(f'Something went wrong: {e}')

if __name__ == '__main__':
    root = tk.Tk()
    root.title('supply-scrubber')
    root.geometry('600x400')
    t = tk.Label(root, text='...')
    t.pack()

    run = tk.Button(root, text='Run', command=main)
    run.pack()

    root.mainloop()