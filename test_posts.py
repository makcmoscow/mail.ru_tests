from urllib.parse import urljoin
import requests
import pytest

BASEURL = 'https://jsonplaceholder.typicode.com/'



class TestApiPosts():
    @pytest.mark.parametrize('url, expected', [('posts', 200), ('posts/123', 404)])
    def test_responce(self, url, expected):
        posts_url = urljoin(BASEURL, url)
        response = requests.get(posts_url)
        posts_page_code = response.status_code
        assert posts_page_code == expected

    @pytest.mark.parametrize('title, body, uId, url', [('my simple test', 'passed well', '15', 'posts')])
    def test_create(self, title, body, uId, url):
        payload = {'title':title, 'body':body, 'userId':uId}
        response = requests.post(urljoin(BASEURL, url), data=payload).json()
        print(response)
        assert response['userId'] == uId
        assert response['title'] == title
        assert response['body'] == body


    def test_modify(self):
        payload = {'title': 'my simple test', 'userId': '15', 'id':'1'}
        response = requests.put(urljoin(BASEURL, 'posts/1'), data=payload)
        assert response.status_code == 200

    def test_delete(self):
        response = requests.delete(urljoin(BASEURL, 'posts/1'))
        assert response.status_code == 200

    def test_modify_err_url(self):
        response = requests.delete(urljoin(BASEURL, 'posts'))
        assert response.status_code == 404

    def test_check_title(self):
        user_id = 5
        posts_url = urljoin(BASEURL, 'posts')
        response = requests.get(posts_url).json()
        posts_list = [p for p in response if p['userId'] == user_id]
        assert posts_list[0]['title'] == 'non est facere'

    def test_check_too_big_id(self):
        posts_url = urljoin(BASEURL, 'posts/101')
        response = requests.get(posts_url)
        assert response.status_code == 404








if __name__ == '__main__':
    TestApiPosts().test_check_too_big_id()
