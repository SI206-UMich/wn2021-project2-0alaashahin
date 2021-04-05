from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

#Group Members: Nick Sidor, Alaa Shahin and Ari Feldberg
def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    data = ""
    with open(filename) as f:
        data = f.read()
    
    soup = BeautifulSoup(data, "lxml")
    titles = []
    titles = soup.find_all( 'a', class_ = "bookTitle")

    booktitles = []
    for t in titles: 
        booktitles.append(t.text.strip())
    
    authorname = []
    authors = soup.find_all("div", class_="authorName__container")
    for a in authors:
        authorname.append(a.text.strip())
    

    final = []
    for i in range(len(booktitles)):
        final.append((booktitles[i], authorname[i]))
    return final



def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    r = requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc")
    soup = BeautifulSoup(r.text, "lxml")

    links = []
    urls = soup.find_all( 'a', class_ = "bookTitle")
    for i in urls[:10]:
        if i["href"].startswith("/book/show/"):
            links.append("https://www.goodreads.com"+i["href"])
    return links


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, "lxml")
    
    title = soup.find('h1', class_ = "gr-h1 gr-h1--serif").text.strip()
    author = soup.find('a', class_ ="authorName").text.strip()
    number_pages = int(soup.find('span', itemprop = "numberOfPages").text.strip()[:3])

    return (title, author, number_pages)
    

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    data = ""
    with open(filepath, encoding="utf-8") as f:
        data = f.read()

    soup = BeautifulSoup(data, "lxml")
    categories = []
    categories = soup.find_all('div', class_="category clearFix")

    genres = []
    genres = soup.find_all('h4', class_ = "category__copy")

    titles = []
    titles = soup.find_all('img', class_ = "category__winnerImage")

    genreLst = []
    for g in genres:
        genreLst.append(g.text.strip())

    titleLst = []
    for t in titles:
        titleLst.append(t.get('alt', None))

    urlLst = []
    for c in categories:
        urlLst.append(c.find('a')['href'])

    bestBookLst = []
    for i in range(len(urlLst)):
        bestBookLst.append(((genreLst[i], titleLst[i]), urlLst[i]))

    return bestBookLst

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    write_file = open(filename, 'w', newline="")
    writer = csv.writer(write_file, delimiter=",")
    writer.writerow(["Book title", "Author Name"])

    for i in data:
        writer.writerow(i)

    write_file.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    with open(filepath, encoding="utf-8") as f:
        data = f.read()
    soup = BeautifulSoup(data, 'lxml')
    description = soup.find('div', class_ = 'readable stacked').find('span', id = "freeText4791443123668479528").text

    regex = r'\b[A-Z][a-z]{3,}(?:\s[A-Z]\w+)+'
    entities = re.findall(regex, description)
    return entities
    

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()


    def test_get_titles_from_search_results(self):

        
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        results = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(results), 20)
        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(results, list)
        # check that each item in the list is a tuple
        for i in results:
            self.assertIsInstance(i, tuple)
        
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(results[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(results[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIsInstance(TestCases.search_urls, list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for i in TestCases.search_urls:
            self.assertIsInstance(i, str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for i in TestCases.search_urls:
            self.assertTrue("https://www.goodreads.com/book/show/" in i)

        
    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries= []
        for i in TestCases.search_urls:
            summaries.append(get_book_summary(i)) 
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        for i in summaries:
            self.assertIsInstance(i, tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(i), 3)
            # check that the first two elements in the tuple are string
            self.assertIsInstance(i[0], str)
            self.assertIsInstance(i[1], str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertIsInstance(i[2], int)
            # check that the first book in the search has 337 pages
            self.assertEqual(summaries[0][2], 337)
            
    def test_summarize_best_books(self):
        #summarize_best_books("best_books_2020.htm")

        # call summarize_best_books and save it to a variable
        results = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(results), 20)

        for i in results:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(i), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(i[0]) + len(i) - 1, 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(results[0][0][0], 'Fiction')
        self.assertEqual(results[0][0][1], "The Midnight Library")
        self.assertEqual(results[0][1], 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(results[-1][0][0], 'Picture Books')
        self.assertEqual(results[-1][0][1], 'Antiracist Baby')
        self.assertEqual(results[-1][1], 'https://www.goodreads.com/choiceawards/best-picture-books-2020')

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        results = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(results, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)

        file = open('test.csv')
        csv_reader = csv.reader(file)
        csv_lines = []
        for i in csv_reader:
            csv_lines.append(i)

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book title', 'Author Name'])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'])

        file.close()



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



