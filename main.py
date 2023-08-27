# Импортируем необходимые библиотеки
# googleapiclient.discovery позволяет создавать и взаимодействовать с ресурсами API Google.
# googleapiclient.errors содержит классы ошибок, которые могут возникнуть при работе с API Google.
import googleapiclient.discovery
import googleapiclient.errors

# Задаем параметры для запросов к API YouTube
api_service_name = "youtube"  # Название сервиса
api_version = "v3"  # Версия API
DEVELOPER_KEY = "AIzaSyCti6aFRKKuq-m_oYVFYEa_1cWOF_kZ8xw"  # Ваш токен-ключ разработчика от Google

# Пытаемся подключиться к серверу YouTube
try:
    # Создаем объект YouTube с использованием googleapiclient.discovery.build.
    # Этот объект будет использован для отправки запросов к серверу YouTube.
    youtube = googleapiclient.discovery.build(api_service_name, api_version,
                                              developerKey=DEVELOPER_KEY)
except Exception as e:
    # Если возникает исключение, выводим сообщение об ошибке с помощью f-строки.
    print(f"Произошла ошибка при подключении к YouTube API: {e}")


# Функция для поиска видео на YouTube
def youtube_search(query, page_token=None):
    # Создаем объект запроса search().list с нужными параметрами.
    # part="snippet" означает, что мы хотим получить основную информацию о каждом видео.
    # maxResults=5 означает, что мы хотим получить информацию максимум о 5 видео.
    # q=query означает, что мы хотим искать видео по заданному запросу.
    # type="video" означает, что мы хотим найти только видео, а не каналы или плейлисты.
    # pageToken=page_token позволяет нам переходить по страницам результатов.
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=query,
        type="video",
        pageToken=page_token
    )
    # Исполняем запрос и возвращаем результат.
    return request.execute()


# Функция для вывода информации о видео
def print_video_details(response):
    # Проходимся по каждому элементу в списке результатов
    for item in response['items']:
        # Получаем название видео
        title = item['snippet']['title']
        # Получаем ID видео
        video_id = item['id']['videoId']

        # Создаем запрос для получения статистики о видео
        details = youtube.videos().list(part='statistics', id=video_id).execute()

        # Получаем количество просмотров видео
        views = details['items'][0]['statistics']['viewCount']
        # Получаем описание видео
        desc = item['snippet']['description']
        # Формируем ссылку на видео
        url = f"https://www.youtube.com/watch?v={video_id}"

        # Выводим всю информацию о видео
        print(f"Название: {title}")
        print(f"Просмотры: {views}")
        print(f"Описание: {desc}")
        print(f"Ссылка: {url}")
        print("\n")


# Функция для взаимодействия с пользователем
def interact_with_user():
    # Приветствуем пользователя и объясняем, что делает программа
    print("Добро пожаловать в YouTube Search API!")
    print("Эта программа позволяет вам искать видео на YouTube и получать информацию о них.\n")

    # Просим пользователя ввести запрос
    query = input("Введите свой запрос: ")

    # Получаем первую страницу результатов
    response = youtube_search(query)

    # Выводим информацию о видео на первой странице результатов
    print_video_details(response)

    # Зацикливаем процесс запроса следующей страницы результатов, пока пользователь не решит выйти
    while True:
        next_page = input(
            "Хотите ли вы перейти на следующую страницу результатов? "
            "Введите 1 для продолжения или любой другой символ для выхода: ")
        if next_page == '1':
            # Получаем токен для следующей страницы результатов
            page_token = response.get('nextPageToken', None)
            if page_token:
                # Если токен есть, получаем следующую страницу результатов и выводим информацию о видео на ней
                response = youtube_search(query, page_token)
                print_video_details(response)
            else:
                # Если токена нет, это означает, что больше страниц с результатами нет
                print("Больше страниц с результатами нет.")
                break
        else:
            # Если пользователь ввел не '1', выходим из цикла
            break


# Запускаем функцию взаимодействия с пользователем
interact_with_user()

# Выводим сообщение о завершении работы программы
print('Программа завершила свою работу')
