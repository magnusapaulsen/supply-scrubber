import customtkinter as ctk
import threading
from tkinter import filedialog
import queue
import pdf_parser, calculate_total, apartment_summary, wash_summary
import sys

# Create queue for multithreading
update_queue = queue.Queue()

def select_file(ui):
    filepath = filedialog.askopenfilename(
        title = 'Select PDF',
        filetypes = [('PDF files', '*.pdf'), ('All files', '*.*')]
    )
    if filepath:
        filename = filepath.split('/')[-1]
        ui['file'].configure(text = filename) # Show filename
        ui['run'].configure(state = 'normal', text = 'Run', fg_color = '#ff0000', hover_color = "#aa0000", text_color = '#ffffff') # Enable Run button
        ui['run'].selected_file = filepath # Store selected file for when we run the parsing

def worker(ui):
    try:
        selected_file = getattr(ui['run'], 'selected_file', None)
        if not selected_file:
            update_queue.put(('status', 'No file selected'))
            return

        update_queue.put(('status', 'Parsing PDF...'))
        pdf_parser.main(selected_file)

        update_queue.put(('status', 'Calculating totals...'))
        calculate_total.main()

        update_queue.put(('status', 'Grouping apartments...'))
        apartment_summary.main()

        update_queue.put(('status', 'Waiting for input in terminal...'))
        wash_summary.main()

        update_queue.put(('status', 'Complete!', '#00ff00'))

    except Exception as e:
        update_queue.put(('status', f'Error: {e}', '#ff4444'))
    finally:
        update_queue.put(('exit',)) # Sending message to close the program

def run_in_thread(ui):
    ui['run'].configure(
        text = 'Running...',
        fg_color = ['#cccccc', '#333333'],
        text_color = '#ffffff',
        text_color_disabled = ['#aaaaaa', '#555555'],
        state = 'disabled'
    )
    threading.Thread(target = worker, args = (ui,), daemon = True).start() # Start background thread for GUI
    check_queue(ui) # Start loop that looks for new messages to update GUI with

def check_queue(ui):
    try:
        while True:
            msg = update_queue.get_nowait() # Check the queue to see if there is anything waiting
            if msg[0] == 'status': # If there is a status update
                text = msg[1] # Pick out the new status
                color = msg[2] if len(msg) > 2 else '#ffffff' # Pick out the color of the status, default to white
                ui['status'].configure(text = text, text_color = color)
            elif msg[0] == 'enable_button':
                ui['run'].configure(state = 'normal', fg_color = '#1f6aa5')
                return
            elif msg[0] == 'exit':
                ui['root'].after(3000, ui['root'].destroy) # Close the program
                return
    except queue.Empty:
        pass

    # Keep checking every 100 ms
    ui['root'].after(100, lambda: check_queue(ui))

def create_gui():
    # Set color mode and color theme
    ctk.set_appearance_mode('Dark') # 'Dark', 'Light' or 'System'
    ctk.set_default_color_theme('color_theme.json')

    # Create GUI window and set title, size and icon
    root = ctk.CTk()
    root.title('supply-scrubber')
    root.geometry('600x460')
    root.iconbitmap('icon.ico')

    # Create gui dictionary for widgets
    ui = {}
    ui['root'] = root

    # Add title to gui dictionary
    ui['title'] = ctk.CTkLabel(
        root,
        text = 'supply-scrubber',
        font = ctk.CTkFont(size = 24, weight = 'bold')
    )
    ui['title'].pack(pady = 24)

    # Add browse button to gui dictionary
    ui['browse'] = ctk.CTkButton(
        root,
        text = 'Select PDF',
        font = ctk.CTkFont(size = 12, weight = 'normal'),
        command = lambda: select_file(ui), # Lambda to not call the function immediately
    )
    ui['browse'].pack(pady = 24)

    # Add file label to gui dictionary
    ui['file'] = ctk.CTkLabel(
        root,
        text = 'No file selected',
        font = ctk.CTkFont(size = 12, weight = 'normal')
    )
    ui['file'].pack(pady = 24)

    # Add status label to gui dictionary
    ui['status'] = ctk.CTkLabel(
        root,
        text='',
        font = ctk.CTkFont(size = 12, weight = 'normal')
    )
    ui['status'].pack(pady = 24)

    # Add run button to gui dictionary (starts disabled)
    ui['run'] = ctk.CTkButton(
        root,
        text = 'Nothing to run',
        fg_color = ['#cccccc', '#333333'],
        text_color = '#ffffff',
        text_color_disabled = ['#aaaaaa', '#555555'],
        command = lambda: run_in_thread(ui), # Lambda to not call the function immediately
        state = 'disabled'
    )
    ui['run'].pack(pady = 24)

    return root, ui

if __name__ == '__main__':
    root, ui = create_gui()
    root.mainloop()