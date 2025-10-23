import tkinter as tk, pdf_parser, calculate_total, apartments
from tkinter import filedialog

def main():
    try:
        pdf = select_file()
    except Exception as e:
        print(f'Something went wrong: {e}')
    else:
        try:
            pdf_parser.main(pdf)
        except Exception as e:
            print(f'Something went wrong: {e}')
        else:
            try:
                calculate_total.main()
            except Exception as e:
                print(f'Something went wrong: {e}')
            else:
                try:
                    apartments.main()
                except Exception as e:
                    print(f'Something went wrong: {e}')

def select_file():
    filename = filedialog.askopenfilename(
        title = 'Select PDF-file',
        filetypes = [('PDF files', '*.pdf'), ('All files', '*.*')]
    )

    if filename:
        # file_label.config(text=f"Selected: {filename}")
        return filename

if __name__ == '__main__':
    main()
    print('Program ended')