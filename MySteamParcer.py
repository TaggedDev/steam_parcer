import re
import csv
import requests
from bs4 import BeautifulSoup




FILE = 'Steam.csv'

def getHtml(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Error: {response.status_code}. Unable to connect to {url}.')
    return response.text

def getContent(items): 
    result = []

    for eachGame in items: # получаем список AllGames (теперь items) из функции Main(), проходимся по каждому блоку в нём.
        gameTitle = eachGame.find('span', class_='title').get_text(strip=True) 
        gameLink = eachGame.get('href')
        prices = eachGame.find('div', class_="search_price").get_text(strip=True)
        prices = prices.strip('рpуб.').split() 
        try:
            gameLink = gameLink[::-1]
            gameLink = gameLink[gameLink.find('?')+1:]
            gameLink = gameLink[::-1]
        except:
            gameLink = 'No data'
        try:
            gameReleaseDate = eachGame.find('div', class_='search_released').get_text(strip=True)
        except:
            gameReleaseDate = 'No data'
        try:
            gameDiscount = eachGame.find('div', class_='search_discount').get_text(strip=True) # Есть скидка
        except:
            gameDiscount = 'No data' # Нет скидки
        try:
            if prices[0].strip('рpуб.') != 'Free': # если это не FTP, то ставим цену, иначе FTP
                gameOldPrice = prices[0].strip('рpуб.')
            else:
                gameOldPrice = 'Free to play'
        except:
            gameOldPrice = 'No data' # если её (почему-то?) нет
        try:
            if prices[-1].strip('рpуб.') != 'Play' or prices[-1].strip('рpуб.') != 'Demo': # если игра не ФТП или не Демка
                gameNewPrice = prices[-1].strip('рpуб.') # то ставь последний элемент (будет цифра!)
            elif prices[-1].strip('рpуб.') == 'Play': # если последнее слово Play, то это FTP
                gameNewPrice = 'Free to play' 
            elif prices[-1].strip('рpуб.') == 'Demo': # если последнее слово Demo, то это FD
                gameNewPrice = 'Free Demo' 
        except:
            gameNewPrice = 'No data' # Нет скидки
        try:
            gameEconomy = int(gameOldPrice) - int(gameNewPrice) # проверяем, есть ли оба параметра
        except:
            gameEconomy = 'No data' # если на игру нет скидки, то экономии нет
        
        result.append({
            'title': gameTitle,
            'link': gameLink,
            'release date': gameReleaseDate,
            'discount': gameDiscount,
            'old price': gameOldPrice,
            'new price': gameNewPrice,
            'economy': gameEconomy})
        print(gameTitle)
    saveFile(result, FILE)

def saveFile(items, path):
    print('Save file function') 
    with open('D:\\Code\\SteamParcer\\Steam.csv','w',encoding='utf8',newline='') as file:
    	writer = csv.writer(file, delimiter=';')
    	writer.writerow(['Title', 'Link', 'ReleaseDate', 'Discount', 'StandartPrice', 'NewPrice', 'Economy'])
    	for item in items: #games
    		writer.writerow([item['title'], item['link'], item['release date'],item['discount'], item['old price'], item['new price'], item['economy'],])

def getGames(html):
    print('Get games function')
    soup = BeautifulSoup(html, 'lxml')
    #pattern = r'^https://store.steampowered.com/app'
    games = soup.find_all('a', class_='search_result_row')
    return games

def main():
    AllGames = []
    start = 0
    url = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&tags=19%2C492%2C21%2C597%2C599%2C9%2C122'
    games = []
    while True:
        games = getGames(getHtml(url)) # вызываем функцию в которую закидываем элементы страницы Steam с 100 играми. 

        if games: # если список не пустой, то добавляем элементы в большой список AllGames и переходим на следующие 100 игр
            AllGames.extend(games)
            start += 100
            url = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&tags=19%2C492%2C21%2C597%2C599%2C9%2C122'
        else: # если на этой странице больше нет игр - пропускаем.
            break
    getContent(AllGames) # после получения всех игр, вызываем функцию для вытаскивания контента из <html>

if __name__ == "__main__":
    main()