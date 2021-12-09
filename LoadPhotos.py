# Импортируем нужные модули
from urllib.request import urlretrieve
import vk, os, time, math

# Авторизация

session = vk.Session(access_token='59ef803926baf56aa845b40185d09a3038ea3ca349ed123be1db70f81e3fad647510d9405d6ecab162261')
vkapi = vk.API(session, v='5.81')

url = "https://vk.com/albums-162255584"
# Разбираем ссылку
#album_id = url.split('/')[-1].split('_')[1]

owner_id = url.split('/')[-1].split('_')[0].replace('albums', '')

albums = vkapi.photos.getAlbums(owner_id=owner_id)#, album_ids=album_id
print(albums)
for i in range(albums["count"]):
    photos_count = albums["items"][i]["size"]
    album_id = albums["items"][i]["id"]
    
    counter = 0 # текущий счетчик
    prog = 0 # процент загруженных
    breaked = 0 # не загружено из-за ошибки
    time_now = time.time() # время старта

    #&nbsp;Создадим каталоги

    if not os.path.exists('saved'):
        os.mkdir('saved')
    photo_folder = 'saved/album{0}_{1}'.format(owner_id, album_id)
    if not os.path.exists(photo_folder):
        os.mkdir(photo_folder)

    for j in range(math.ceil(photos_count / 1000)): # Подсчитаем&nbsp;сколько раз нужно получать список фото, так как число получится не целое - округляем в большую сторону
        photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id, count=1000, offset=j*1000) #&nbsp;Получаем список фото
        for photo in photos["items"]:
            counter += 1
            url = photo["sizes"][0]["url"] # Получаем адрес изображения
            print('Загружаю фото № {} из {}. Прогресс: {} %'.format(counter, photos_count, prog))
            prog = round(100/photos_count*counter,2)
            try:
                urlretrieve(url, photo_folder + "/"+os.path.split(url)[1].split('?')[0]) # Загружаем и сохраняем файл
            except Exception:
                print('Произошла ошибка, файл пропущен.')
                breaked += 1
                continue

    time_for_dw = time.time() - time_now
    print("\nВ очереди было {} файлов. Из них удачно загружено {} файлов, {} не удалось загрузить. Затрачено времени: {} сек.". format(photos_count, photos_count-breaked, breaked, round(time_for_dw,1)))