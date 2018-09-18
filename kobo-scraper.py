import sys, urllib2, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


class Book:
    def __init__(self, title, author, price, summary):
        self.title = title
        self.author = author
        self.price = price
        self.summary = summary

    def details(self):
        return self.title + '\n' + self.author + '\n' + self.price + '\n' + self.summary + '\n'


# get the books of the month
def get_monthly_books(url):
    book_list = []

    # query the website and return the html to the variable page
    page = urllib2.urlopen(url)

    # parse the html using beautiful soup and store in variable `soup`
    html = BeautifulSoup(page, "html.parser")

    # get the books with author and price
    books = html.findAll('div', attrs={'class': 'book-details'})
    for book in books:
        title = book.find('p', attrs={'class': 'title product-field'}).text.strip()
        author = book.find('p', attrs={'class': 'attribution product-field contributor-list'}).text.strip()
        price = book.find('p', attrs={'class': 'product-field price'}).text.strip()

        book_list.append(Book(title, author, price, ''))

    return book_list


# get the book of the day TODO
def get_daily_book(url):
    
    # query the website and return the html to the variable page
    page = urllib2.urlopen(url)

    # parse the html using beautiful soup and store in variable `soup`
    html = BeautifulSoup(page, "html.parser")
    
    # find highlighted books in the page
    books = html.findAll('div', attrs={'class':'secondary-heading widget-title'})
    
    
    for book in books:
        if book.text == 'Offerta del giorno':
            title = book.findNext('div', attrs={'class':'widget-text-description'}).h1.text.strip()
            author = book.findNext('span', attrs={'class':'visible-contributors'}).text.strip()
            price = book.findNext('div', attrs={'class':'pricing regular-price'}).text.strip()
            summary = book.findNext('div', attrs={'class':'widget-text-description'}).p.text.strip()
            
    book = Book(title, author, price, summary)
    
    return book


# send myself an email with the list of the books
def send_email(email, password, books):

    # prepare the email
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = "Kobo: ebooks in offerta"
    body = '\n'.join(b.details() for b in books)
    msg.attach(MIMEText(body.encode('utf-8'), 'plain'))

    # send the email
    server = smtplib.SMTP("smtp.live.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, password)
    server.sendmail(email, email, msg.as_string())

    print("Email sent to " + email)


def main():
    mm = get_monthly_books("https://www.kobo.com/it/it/p/OfferteDelMese")
    dd = get_daily_book("https://www.kobo.com/it")
    books = [dd] + mm  # make the book of the day the first of the list

    print '\n'.join(b.details() for b in books)

    if len(sys.argv) == 3:
        email = sys.argv[1]
        passw = sys.argv[2]
        send_email(email, passw, books)


if __name__ == "__main__":
    main()
