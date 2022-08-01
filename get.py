from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
import re

class Word:
    def __init__(self, hanzi: str):

        self.hanzi = hanzi
        self.definitions = ""

        self.get_yellowbridge(hanzi)
        if not self.yb_exists:
            self.get_google(hanzi)

    def get_soup(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        return soup
    
    def get_yellowbridge(self, hanzi: str):
        url = f"https://www.yellowbridge.com/chinese/sentsearch.php?word={quote_plus(hanzi)}"
        soup = self.get_soup(url)

        if soup.find("h3", attrs={"class": "sad"}) is not None:
            # print(f"Word not found on YellowBridge: {hanzi}")
            self.yb_exists = False
            return
        else:
            self.yb_exists = True
            self.url = url

        self.pinyin = soup.find("span", attrs={"class": "speech phonetic pronouncer"}).text
        # self.definitions = [d.text for d in soup.find_all("a", attrs={"class": "definition"})]
        self.definitions = ''.join(list(soup.find("table", attrs={"id": "mainData"}).find("tr").strings)[1:])
        self.pos = soup.find_all("td")[-1].text

        self.examples = []
        for row in soup.find_all("table")[1].find_all('li'):
            strings = ''.join(row.strings)
            matches = re.fullmatch("([^\u0000-\u0080]+)([\u0000-\u0080]+)", strings)
            if not matches: 
                print("No matches:", strings, self.url)
                return
            chinese, english = matches.groups()
            self.examples.append({
                "Chinese": chinese,
                "English": english
            })
        self.soup = soup

    def get_google(self, hanzi: str):
        self.url = f"https://translate.google.com/?sl=zh-CN&tl=en&text={quote_plus(hanzi)}&op=translate"

    def __repr__(self):
        if self.yb_exists:
            return f"{self.hanzi} ({self.pinyin}): {self.definitions[0]}"
        else:
            return self.hanzi

if __name__ == "__main__":
    # hanzi = input("Enter a Chinese Word: ")
    hanzi = "参观"
    print(Word(hanzi))