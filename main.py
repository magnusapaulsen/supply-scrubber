import pdf_parser, calculate_total, apartments

def main():
    try:
        # Run pdf_parser to parse washes.pdf and create washes.json
        pdf_parser.main()

        # Run calculate_total to update washes.json with totals
        calculate_total.main()

        # Run apartments to process washes.json and create apartments.json
        apartments.main()

    except Exception as e:
        print(f'Something went wrong: {e}')

if __name__ == '__main__':
    main()