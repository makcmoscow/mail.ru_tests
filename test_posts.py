from urllib.parse import urljoin
import requests
import pytest


BASEURL = 'https://jsonplaceholder.typicode.com/'
parameters = {'title': 'my simple test' , 'body': 'passed well', 'uId': '15', 'url': 'posts', 'url_not_exist': 'possts', 'url_post_to_modify': 'posts/1', 'post_id': '1', 'existed_post_title': 'non est facere', 'url_too_big_post_id': 'posts/150'}


class TestApiPosts():
    @pytest.mark.parametrize('url, expected', [(parameters['url'], 200), (parameters['url_not_exist'], 404)])
    def test_responce(self, url, expected):  # проверяем доступность раздела сайта, содержащего посты.
        posts_url = urljoin(BASEURL, url)   # формируем URL раздела путем присоединения к базовому URL нужного окончания
        response = requests.get(posts_url)  # запрашиваем страничку с разделом
        posts_page_code = response.status_code  # смотрим код ответа
        assert posts_page_code == expected  # ошибка в случае несовпадения кода ответа с ожидаемым.

    @pytest.mark.parametrize('title, body, uId, url', [(parameters['title'], parameters['body'], parameters['uId'], parameters['url'])])
    def test_create(self, title, body, uId, url):
        payload = {'title':title, 'body':body, 'userId':uId}  # Формирум данные для отправки на сайт
        response = requests.post(urljoin(BASEURL, url), data=payload).json()  # Получаем результат отправки
        assert response['userId'] == uId   # Проверяем, что заголовок и тело поста, а также
        assert response['title'] == title  # ID создателя поста соответствуют отправленному
        assert response['body'] == body    #

    @pytest.mark.parametrize('title, userID, id, url_post_to_modify', [(parameters['title'], parameters['uId'], parameters['post_id'], parameters['url_post_to_modify'])])
    def test_modify(self, title, userID, id, url_post_to_modify):                   # формируем данные для отправки запроса
        payload = {'title': title, 'userId': userID, 'id': id}                      # отправляем запрос. В качестве результата
        response = requests.put(urljoin(BASEURL, url_post_to_modify), data=payload) # мы можем только убедиться, что код ответа
        assert response.status_code == 200                                          # равен 200, так как реально данные не меняются


    @pytest.mark.parametrize('url_to_modify', [parameters['url']])
    def test_delete(self, url_to_modify):                                               # То же самое, что и в тесте
        response = requests.delete(urljoin(BASEURL, parameters['url_post_to_modify']))  # test_modify, проверяем код 200
        assert response.status_code == 200

    @pytest.mark.parametrize('url, uID, existed_post_title', [(parameters['url'], parameters['uId'], parameters['existed_post_title'])])
    def test_check_title(self, url, uID, existed_post_title):
        user_id = 5                                                 # Определяем ID автора поста из существующих авторов
        posts_url = urljoin(BASEURL, url)                           # запрашиваем все посты, фильтруем по автору и ищем
        response = requests.get(posts_url).json()                   # заголовок у первого поста. Должен быть равен опре-
        posts_list = [p for p in response if p['userId'] == user_id]# деленной фразе (non est facere)
        assert posts_list[0]['title'] == existed_post_title

    @pytest.mark.parametrize('url_too_big_post_id', [(parameters['url_too_big_post_id'])])  # В случае несуществующего
    def test_check_post_not_exist(self, url_too_big_post_id):                               # поста атрибут text должен
        response = requests.get(urljoin(BASEURL, url_too_big_post_id))                      # быть равен {}
        assert response.text == '{}'
