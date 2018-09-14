import urllib2
from bs4 import BeautifulSoup


def main():
    # specify the url
    main_page = "https://www.kobo.com/it/it/p/OfferteDelMese"

    # query the website and return the html to the variable page
    page = urllib2.urlopen(main_page)

    # parse the html using beautiful soup and store in variable `soup`
    html = BeautifulSoup(page, "html.parser")

    #print soup

    books = html.findAll('div', attrs={'class':'book-details'})
    for book in books:
        title = book.find('p', attrs={'class':'title product-field'}).text.strip()
        author = book.find('p', attrs={'class':'attribution product-field contributor-list'}).text.strip()
        price = book.find('p', attrs={'class':'product-field price'}).text.strip()

        print title + '\n' + author + '\n' + price + '\n'


if __name__ == "__main__":
    main()