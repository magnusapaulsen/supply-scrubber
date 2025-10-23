import tkinter as tk
import threading
from tkinter import filedialog
import pdf_parser, calculate_total, apartments

def select_file():
    filepath = filedialog.askopenfilename(
        title='Select PDF file',
        filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')]
    )
    
    if filepath:
        # Split filepath into filename
        filename = filepath.split('/')[-1]
        # Show which file was found
        file_label.config(text=f'📄 {filename}', fg='Blue')
        # Set run-button state to normal, so that it can be used again
        run_button.config(state='normal')
        # Store it in the button itself so main() can access it
        run_button.selected_file = filepath
        return filepath
    return None

def main(status_label, root, run_button):
    try:
        # Get the file path stored in the button
        selected_file = getattr(run_button, 'selected_file', None)
        
        if not selected_file:
            status_label.config(text='No file selected', fg='#ffffff')
            return
            
        status_label.config(text='Parsing PDF...', foreground='#0000ff')
        root.update_idletasks()
        pdf_parser.main(selected_file)

        status_label.config(text='Calculating totals...', foreground='#0000ff')
        root.update_idletasks()
        calculate_total.main()

        status_label.config(text='Processing apartments...', foreground='#0000ff')
        root.update_idletasks()
        apartments.main()

        status_label.config(text='Complete!', foreground='#00ff00')
        
    except Exception as e:
        status_label.config(text=f'Error: {e}', foreground='#ff0000')
    
    finally:
        run_button.config(state='normal')

def run_in_thread():
    run_button.config(state='disabled')
    threading.Thread(
        target=main, 
        args=(status_label, root, run_button),
        daemon=True
    ).start()

def on_enter_browse(e):
    browse_button.config(bg='#ff0000')

def on_leave_browse(e):
    browse_button.config(bg='#00ff00')

def on_enter_run(e):
    if run_button['state'] == 'normal':
        run_button.config(bg='#0A84FF')

def on_leave_run(e):
    if run_button['state'] == 'normal':
        run_button.config(bg='#007AFF')

if __name__ == '__main__':
    root = tk.Tk()
    root.title('supply-scrubber')
    root.geometry('600x400')
    root.config(bg='#000000')
    
    # Title
    title_label = tk.Label(
        root,
        text='supply-scrubber',
        font=('Roboto', 24, 'bold'),
        bg='#000000',
        fg='#FFFFFF'
    )
    title_label.pack(pady=10)
    
    # Browse button
    browse_button = tk.Button(
        root,
        text='📁 Select PDF File',
        command=select_file,
        font=('Roboto', 12),
        bg='#000000', # Ser ikke bakgrunn pr nå
        fg='#111111',
        padx=10,
        pady=5,
        cursor='hand2',
        bd = 0
    )
    browse_button.pack(pady=10)
    browse_button.bind('<Enter>', on_enter_browse)
    browse_button.bind('<Leave>', on_leave_browse)
    
    # Filename text
    file_label = tk.Label(
        root,
        text='No file selected',
        font=('Roboto', 12),
        bg='#000000',
        fg='#ffffff'
    )
    file_label.pack(pady=10)
    
    # Status text
    status_label = tk.Label(
        root, 
        text='', 
        font=('Roboto', 12),
        bg='#000000',
        fg='#ffffff'
    )
    status_label.pack(pady=10)

    # Run button
    run_button = tk.Button(
        root,
        text='Run',
        command=run_in_thread,
        font=('Roboto', 12),
        bg='#000000', # Ser ikke bakgrunn pr nå
        fg='#111111',
        padx=10,
        pady=5,
        cursor='hand2',
        bd = 0
    )
    run_button.pack(pady=10)
    run_button.bind('<Enter>', on_enter_run)
    run_button.bind('<Leave>', on_leave_run)

    root.mainloop()