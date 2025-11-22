import customtkinter as ctk
import threading
from tkinter import filedialog
from CTkSpinbox import CTkSpinbox
import queue
import pdf_parser, calculate_total, apartment_summary, wash_summary

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

        update_queue.put(('status', 'Waiting for input...'))
        apartments = wash_summary.load('apartments.json')
        apts = wash_summary.prepare_data(apartments)
        price_list_apartments = wash_summary.load('price_list_apartments.json')

        summary = {}
        for apt in apts:
            ui['root'].after(0, lambda apartment = apt: get_input(ui, apartment))

            while True:
                msg = update_queue.get()
                if msg[0] == 'answer' and msg[1] == apt:
                    summary[apt] = msg[2]
                    break
        wash_summary.save(wash_summary.finalize_data(apartments, summary, price_list_apartments), 'apartments.json')

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
    root.geometry('500x600')
    root.iconbitmap('icon.ico')

    root.grid_rowconfigure(0, weight = 0)
    root.grid_columnconfigure(0, weight = 1)

    # Create gui dictionary for widgets
    ui = {}
    ui['root'] = root

    # Add title to gui dictionary
    ui['title'] = ctk.CTkLabel(
        root,
        text = 'supply-scrubber',
        font = ctk.CTkFont(size = 24, weight = 'bold')
    )
    ui['title'].grid(row = 0, column = 0, pady = 24)

    # Add select button to gui dictionary
    ui['select'] = ctk.CTkButton(
        root,
        text = 'Select PDF',
        font = ctk.CTkFont(size = 12, weight = 'normal'),
        command = lambda: select_file(ui), # Lambda to not call the function immediately
    )
    ui['select'].grid(row = 1, column = 0, pady = 24)

    # Add file label to gui dictionary
    ui['file'] = ctk.CTkLabel(
        root,
        text = 'No file selected',
        font = ctk.CTkFont(size = 12, weight = 'normal')
    )
    ui['file'].grid(row = 2, column = 0, pady = 12)

    # Add status label to gui dictionary
    ui['status'] = ctk.CTkLabel(
        root,
        text='',
        font = ctk.CTkFont(size = 12, weight = 'normal')
    )
    ui['status'].grid(row = 3, column = 0, pady = 24)

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
    ui['run'].grid(row = 4, column = 0, pady = 12)

    return root, ui

def get_input(ui, apartment: str):
    if hasattr(ui['root'], 'wash_frame'):
        ui['root'].wash_frame.destroy()

    frame = ctk.CTkFrame(ui['root'], fg_color = 'transparent', corner_radius = 10)
    frame.grid(row = 5, column = 0, pady = 24)
    ui['root'].wash_frame = frame
    
    frame.grid_rowconfigure(0, weight = 0)
    frame.grid_columnconfigure(0, weight = 1)

    question = ctk.CTkLabel(frame, text = f'{apartment}', width = 192, height = 24, corner_radius = 10)
    question.grid(row = 0, column = 0, pady = 6)

    spinbox = CTkSpinbox(frame, width = 96, height = 48, start_value = 0, min_value = 0, max_value = 99, step_value = 1, scroll_value = 1, border_color = '#000000', font = ctk.CTkFont(size = 24, weight = 'normal'), fg_color = 'transparent', text_color = ('#000000', '#ffffff'), button_color = 'transparent', button_hover_color = ('#cccccc', '#333333'), button_border_color = ('#ffffff', '#000000'))
    spinbox.grid(row = 1, column = 0, pady = 6)
    spinbox.set(0)
    spinbox.focus()

    def submit(event = None):
        value = int(spinbox.get() or 0)
        update_queue.put(('answer', apartment, value))
        frame.destroy()

    butt = ctk.CTkButton(frame, corner_radius = 10, fg_color = '#ff0000', hover_color = '#aa0000', text_color = '#ffffff', font = ctk.CTkFont(size = 12, weight = 'normal'), text = 'Submit', command = submit)
    butt.grid(row = 2, column = 0, pady = 6)

    spinbox.focus_set()
    ui['root'].after(100, spinbox.focus_set)

    

if __name__ == '__main__':
    root, ui = create_gui()
    root.mainloop()