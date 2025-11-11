import tkinter as tk
import threading
from tkinter import filedialog
import queue
import pdf_parser, calculate_total, apartment_summary, wash_summary

# Thread-safe queue for GUI updates
update_queue = queue.Queue()

def select_file():
    filepath = filedialog.askopenfilename(
        title='Select PDF file',
        filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')]
    )
    
    if filepath:
        filename = filepath.split('/')[-1]
        file_label.config(text=f'{filename}', fg='Blue')
        run_button.config(state='normal')
        run_button.selected_file = filepath
        return filepath
    return None

def worker():
    try:
        selected_file = getattr(run_button, 'selected_file', None)
        if not selected_file:
            update_queue.put(('status', 'No file selected', '#ffffff'))
            return

        update_queue.put(('status', 'Parsing PDF...', '#0000ff'))
        pdf_parser.main(selected_file)

        update_queue.put(('status', 'Calculating totals...', '#0000ff'))
        calculate_total.main()

        update_queue.put(('status', 'Grouping apartments...', '#0000ff'))
        apartment_summary.main()

        update_queue.put(('status', 'Calculating washes...', '#0000ff'))
        wash_summary.main()

        update_queue.put(('status', 'Complete!', '#00ff00'))

    except Exception as e:
        update_queue.put(('status', f'Error: {e}', '#ff0000'))
    finally:
        update_queue.put(('enable_button',))

def run_in_thread():
    run_button.config(state='disabled')
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    check_queue()  # Start polling

def check_queue():
    try:
        while True:
            msg = update_queue.get_nowait()
            if msg[0] == 'status':
                text, color = msg[1], msg[2]
                status_label.config(text=text, foreground=color)
            elif msg[0] == 'enable_button':
                run_button.config(state='normal')
                return  # Stop polling if done
    except queue.Empty:
        pass
    # Continue polling every 100ms
    root.after(100, check_queue)

# Hover effects
def on_enter_browse(e): browse_button.config(bg='#222222')
def on_leave_browse(e): browse_button.config(bg='#333333')
def on_enter_run(e):
    if run_button['state'] == 'normal':
        run_button.config(bg='#222222')
def on_leave_run(e):
    if run_button['state'] == 'normal':
        run_button.config(bg='#333333')

if __name__ == '__main__':
    root = tk.Tk()
    root.title('supply-scrubber')
    root.geometry('600x400')
    root.config(bg='#000000')
    
    # Title
    title_label = tk.Label(root, text='supply-scrubber', font=('Roboto', 24, 'bold'), bg='#000000', fg='#FFFFFF')
    title_label.pack(pady=10)
    
    # Browse button
    browse_button = tk.Button(root, text='Select PDF File', command=select_file,
                              font=('Roboto', 12), bg='#333333', fg='#ffffff',
                              padx=10, pady=5, cursor='hand2', bd=0)
    browse_button.pack(pady=10)
    browse_button.bind('<Enter>', on_enter_browse)
    browse_button.bind('<Leave>', on_leave_browse)
    
    # File label
    file_label = tk.Label(root, text='No file selected', font=('Roboto', 12), bg='#000000', fg='#ffffff')
    file_label.pack(pady=10)
    
    # Status label
    status_label = tk.Label(root, text='', font=('Roboto', 12), bg='#000000', fg='#ffffff')
    status_label.pack(pady=10)

    # Run button
    run_button = tk.Button(root, text='Run', command=run_in_thread,
                           font=('Roboto', 12), bg='#333333', fg='#ffffff',
                           padx=10, pady=5, cursor='hand2', bd=0)
    run_button.pack(pady=10)
    run_button.bind('<Enter>', on_enter_run)
    run_button.bind('<Leave>', on_leave_run)

    root.mainloop()