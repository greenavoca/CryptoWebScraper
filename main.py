from features import create_crypto_csv, draw_chart


def main():
    menu = '''

    ----------CRYPTOCURRENCY SCRAPER & ANALYSER----------

    Choose an action:

        (c) - create csv file with cryptocurrencies
        (a) - analyse particular cryptocurrency (requires existing file/s)
        (q) - quit

    '''
    choice = input(menu).lower().strip()

    while choice != 'q':
        if choice == 'c':
            print('Downloading data (might take a while)...')
            create_crypto_csv()
        elif choice == 'a':
            crypto_name = input('Enter cryptocurrency name: ')
            draw_chart(crypto_name)
        else:
            print("Invalid input")

        choice = input(menu).lower().strip()

    print('Goodbye')


if __name__ == '__main__':
    main()
