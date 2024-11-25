import requests
import json
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup

def generate_headers(url):
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"{url}",}

class Server:

    def __init__(self, server):
        self.name = server
        self._url = self._generate_server_url()
        self.guild_list = self._generate_url_list()
        self.last_page = self._get_last_page()

    def _generate_server_url(self):
        servers = {
        'Ombre' : 50,
        'Tal Kasha' : 290,
        'Imajiro' : 291,
        'Orukam' : 292,
        'Tylezia' : 293,
        'Hell Mina' : 294,
        'Draconiros' : 295,}
        return f"https://www.dofus.com/fr/mmorpg/communaute/annuaires/pages-guildes?&server_id={servers[self.name]}"
    
    def _generate_url_list(self, pages=1):
        server_list = {}
        for i in range(0,pages):
            response = requests.get(self._url+f'&page={i+1}', headers=generate_headers(self._url))
            soup = BeautifulSoup(response.content, 'html.parser').find('tbody').find_all('tr')
            for guild in soup:
                infos = guild.find_all('td')
                server_list[infos[1].find('a').text] = infos[1].find('a')['href']
        return server_list
    
    def generate_guild(self, guild):
        for i,name in enumerate(self.guild_list.keys()):
            if name == guild:
                return Guild(list(self.guild_list.items())[i], self.name)

    def _get_last_page(self):
        response = requests.get(self._url, headers=generate_headers(self._url))
        soup = BeautifulSoup(response.content, 'html.parser')
        return int(soup.find('ul', class_='ak-pagination pagination').find_all('li')[-3].text.strip())

class Guild:
    
    def __init__(self, tuple, server):
        self._url = f"https://www.dofus.com{tuple[1]}/membres"
        self.name = tuple[0]
        self._response = requests.get(self._url, headers=generate_headers(self._url))
        self._soup = BeautifulSoup(self._response.content, 'html.parser')
        self.members_list = self.generate_member_list()
        self.server = server

    def generate_member_list(self):
        member_list = {}
        for i in self._soup.find('tbody').find_all('tr'):
            member_list[i.find('a').text]= i.find('a')['href']
        return member_list
    
    def generate_member(self, member):
        for i,name in enumerate(self.members_list.keys()):
            if name == member:
                return Perso(list(self.members_list.items())[i])
            
    def generate_json(self):
        guild_doc = {}
        for i in tqdm(self.members_list.keys()):
            member = self.generate_member(i)
            guild_doc[i] = member.get_infos()
            sleep(1.5)
        with open(f'{self.server}/{self.name.strip()}.json', 'w') as f:
            json.dump(guild_doc, f, indent=2)
        return f'{self.name} done'
        
class Perso:

    def __init__(self, tuple):
        self._url = f"https://www.dofus.com{tuple[1]}"
        self._response = requests.get(self._url, headers=generate_headers(self._url))
        self._soup = BeautifulSoup(self._response.content, 'html.parser')
        self.professions = self.set_professions()
        self.level = self.set_level()
        self.classe = self.set_class()
        self.title = self.set_title()
        self.alignment = self.set_alignment()
        self.name = tuple[0]

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
        try:
            return int(self._soup.find(class_='ak-directories-level').text.strip()[7:])+omega
        except:
            return None
    
    def set_class(self):
        try:
            return self._soup.find(class_='ak-directories-breed').text.strip()
        except:
            return None
    
    def set_title(self):
        try:
            return self._soup.find(class_='ak-directories-grade').text.strip()
        except:
            return None
    
    def set_alignment(self):
        try:
            return self._soup.find(class_='ak-alignment-name').text.strip()
        except:
            return None

    def get_infos(self):
        return {
            # 'name': self.name,
            'title': self.title,
            'class': self.classe,
            'level': self.level,
            'alignement': self.alignment,
            'professions': self.professions
        }

if __name__ == '__main__':
    server = Server('Orukam')
    # old = server.generate_guild('Old Spirit')
    # print(old.generate_json())
    for i in server.guild_list.keys():
        guild = server.generate_guild(i)
        print(guild.generate_json())
        # print(guild.generate_member(list(guild.members_list.keys())[0]).get_infos())