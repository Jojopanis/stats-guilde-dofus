import requests
from bs4 import BeautifulSoup

urls= ['https://www.dofus.com/fr/mmorpg/communaute/annuaires/pages-persos/99753800295-kaygrim','https://www.dofus.com/fr/mmorpg/communaute/annuaires/pages-persos/497379700292-zaridem','https://www.dofus.com/fr/mmorpg/communaute/annuaires/pages-persos/738006100292-bapao']

def generate_headers(url):
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"{url}",}

class Server:

    def __init__(self, server):
        self.server = server
        self.url = self.generate_server_url()
        self.guilds = self.generate_url_list()
        self.last_page = self.get_last_page()

    def generate_server_url(self):
        servers = {
        'Ombre' : 50,
        'Tal Kasha' : 290,
        'Imajiro' : 291,
        'Orukam' : 292,
        'Tylezia' : 293,
        'Hell Mina' : 294,
        'Draconiros' : 295,}
        return f"https://www.dofus.com/fr/mmorpg/communaute/annuaires/pages-guildes?&server_id={servers[self.server]}"
    
    def generate_url_list(self, pages=1):
        server_list = {}
        for i in range(0,pages):
            response = requests.get(self.url+f'&page={i+1}', headers=generate_headers(self.url))
            soup = BeautifulSoup(response.content, 'html.parser').find('tbody').find_all('tr')
            for guild in soup:
                infos = guild.find_all('td')
                server_list[infos[1].find('a').text] = infos[1].find('a')['href']
        return server_list
    
    def generate_guild(self, guild):
        return Guild(f"https://www.dofus.com{self.guilds[guild]}/membres")

    def get_last_page(self):
        response = requests.get(self.url, headers=generate_headers(self.url))
        soup = BeautifulSoup(response.content, 'html.parser')
        return int(soup.find('ul', class_='ak-pagination pagination').find_all('li')[-3].text.strip())

class Guild:
    
    def __init__(self, url):
        self.url = url
        self._response = requests.get(url, headers=generate_headers(url))
        self._soup = BeautifulSoup(self._response.content, 'html.parser')

    def generate_member_list(self):
        member_list = {}
        # perso = Perso(f"https://www.dofus.com{}")
        for i in self._soup.find('tbody').find_all('tr'):
            member_list[i.find('a').text]= i.find('a')['href']
        return member_list

class Perso:

    def __init__(self, url):
        self._response = requests.get(url, headers=generate_headers(url))
        self._soup = BeautifulSoup(self._response.content, 'html.parser')
        self.professions = self.set_professions()
        self.level = self.set_level()
        self.classe = self.set_class()
        self.title = self.set_title()
        self.name = self.set_name()

    def set_professions(self):
        ak_content = self._soup.find_all('div', class_='ak-content')
        professions = {}
        for content in ak_content:
            try:
                professions[content.find('a').text.strip()] = int(content.find('div', class_='ak-text').text[8:-1])
            except:
                break
        return professions

    def set_level(self):
        omega = 0
        if self._soup.find(class_='ak-omega-level'):
            omega = 200
        return int(self._soup.find(class_='ak-directories-level').text.strip()[7:])+omega
    
    def set_class(self):
        return self._soup.find(class_='ak-directories-breed').text.strip()
    
    def set_title(self):
        return self._soup.find(class_='ak-directories-grade').text.strip()
    
    def set_name(self):
        return(self._soup.select_one('div[class*="ak-character-ornament"]').text.strip())

    def get_infos(self):
        return {
            'name': self.name,
            'title': self.title,
            'class': self.classe,
            'level': self.level,
            'professions': self.professions
        }

if __name__ == '__main__':
    orukam = Server('Orukam')
    old = orukam.generate_guild('Old Spirit')
    print(old.generate_member_list())



