from bs4 import BeautifulSoup
from requests_html import HTMLSession
from unidecode import unidecode
import pywhatkit as pwk
import sys, os

KEYWORDS = []                                   # Fill this list with string keywords, separated by commas
WPP_GROUP_ID = None                             # Fill here for whatsapp group id to send results
AUTO_MSG_HOUR = None                            # Fill here for auto message hour (24 hours format)
AUTO_MSG_MIN = None                             # Fill here for auto message minute

def getArticles():
    """
    Requests articles from the specified website, returns a list with all articles found

    Input: none
    Output: List of html segments with relevant articles
    """
    url = "https://diariooficial.elperuano.pe/Normas"

    # Makes a session to render js scripts
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=5)  # Sleep is set to 5 to allow page to render, the value of sleep could be changed

    soup = BeautifulSoup(r.html.html, 'html.parser')
    articles = soup.find_all('article', class_=['edicionesoficiales_articulos', 'edicionesoficiales_articulos_dig'])

    return articles

def getInfo(article):
    """
    Takes an article previously crawled, and generates a dictionary with keys containing
    relevant information (title, resolution, date, description, link)

    Input:
        article: a single article from the ones previously crawled
    
    Output: a dictionary containing relevant information from the article
    """
    articleInfo = {}

    articleInfo["title"] = article.find("h4").text
    articleInfo["resolucion"] = article.find("h5").find('a').text
    articleInfo["date"] = article.find("b").text.strip()

    # Checks for the 'extraordinaria' tag
    extraordinaria = article.find("strong", class_="extraordinaria")
    if extraordinaria:
        articleInfo["date"] += ' ' + extraordinaria.text

    articleInfo["description"] = article.find_all("p")[1].text
    articleInfo["link"] = article.find("h5").find('a').get('href')

    return articleInfo

def writeToFile(articleList):
    """
    Writes the contents from an articleList containing dictionaries with article information,
    to a text file 'results.txt'

    Input:
        articleList: a list of dictionaries containing information on articles

    Output: none
    """
    file = open('results.txt', 'w', encoding='utf-8')

    for article in articleList:
        file.write(article['title'] + '\n')
        file.write(article['resolucion'] + '\n')
        file.write(article['date'] + '\n')
        file.write('\n' + article['description'] + '\n')
        file.write('\n' + article['link'] + '\n')
        
        if article != articleList[-1]:
            file.write('\n' + '-'*50 + '\n'*2)

    file.close()

def extractKeyArticles(articleList, keywordList):
    """
    Takes a list of dictionaries with article information and returns a list with
    only the articles with a description that contains one of the specified keywords

    Input:
        articleList: a list of dictionaries containing information on article
        keywordList: a list of string keywords

    Output: a filtered list of dictionaries that contain any of the keyword
    """
    newArticleList = []

    for article in articleList:
        for keyword in keywordList:
            if unidecode(keyword).lower() in unidecode(article["description"]).lower():
                newArticleList.append(article)
                break

    return newArticleList

def getKeywordsFromFile(pathToFile, separator):
    """
    Gets the keyword from an external text file

    Input:
        pathToFile: a string path to the text file containing the keywords
        separator: a string separator used in the keyword file

    Output: a list of string keywords
    """
    keywordList = []

    file = open(pathToFile, 'r')

    for line in file:
        for keyword in line.split(separator):
            if keyword:
                keywordList.append(keyword.strip())

    return keywordList

def whatsappResults(articleList):
    """
    Sends a whatsapp message from the 

    Input: 
        articleList: a list of dictionaries containing information on article

    Output: none
    """
    results = ''

    for article in articleList:
        results += article['title'] + '\n'
        results += article['resolucion'] + '\n'
        results += article['date'] + '\n'
        results += '\n' + article['description'] + '\n'
        results += '\n' + article['link'] + '\n'
        
        if article != articleList[-1]:
            results += '\n' + '-'*50 + '\n'*2

    pwk.sendwhatmsg_to_group(WPP_GROUP_ID, results, AUTO_MSG_HOUR, AUTO_MSG_MIN, 30)

def main():
    keywordMode = False
    externalKeywordList = False
    autoMsgMode = False

    # CLI
    if len(sys.argv) < 1:
        raise Exception("Incorrect argument number. Usage: python crawler.py [-k] [-f ('PATH_TO_FILE' 'SEPARATOR_CHARACTER')] [-w]")
    
    if "-k" in sys.argv:
        keywordMode = True

    if '-f' in sys.argv:
        externalKeywordList = True

        try:
            keywordPath = sys.argv[sys.argv.index('-f') + 1]
            if not os.path.exists(keywordPath):
                raise Exception("Invalid path. Make sure to specify a valid path after the -f flag")
        except:
            raise Exception("Path to keyword file not provided. Usage: python crawler.py [-k] [-f ('PATH_TO_FILE' 'SEPARATOR_CHARACTER')] [-w]")
        
        try:
            keywordFileSeparator = sys.argv[sys.argv.index('-f') + 2]
            if len(keywordFileSeparator) > 1:
                raise Exception("Invalid separator. Expected single character.")
        except:
            print("Separator not specified. Assuming new line character as separator...")
            keywordFileSeparator = '\n'

    if '-w' in sys.argv:
        autoMsgMode = True

    # Get articles from website
    articles = getArticles()
    articleList = []

    # Make a list with the info from the articles
    for article in articles:
        articleList.append(getInfo(article))

    # Checks whether to use kw mode or extKwList mode
    if keywordMode or externalKeywordList:
        keywordList = None

        if externalKeywordList:
            keywordList = getKeywordsFromFile(keywordPath, keywordFileSeparator)
        elif len(KEYWORDS) > 0:
            keywordList = KEYWORDS
        else:
            print("Keyword list empty. All articles extracted.")

        if keywordList:
            articleList = extractKeyArticles(articleList, keywordList)

    # Writes results to a file
    writeToFile(articleList)
    
    # Automates a whatsapp message with the results
    if autoMsgMode:
        whatsappResults(articleList)

if __name__ == "__main__":
    main()