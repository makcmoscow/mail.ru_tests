from urllib.parse import urljoin
import requests

BASEURL = 'https://jsonplaceholder.typicode.com/'



class TestApiPosts():
    def test_responce(self):
        posts_url = urljoin(BASEURL, 'posts')
        response = requests.get(posts_url)
        posts_page_code = response.status_code
        assert posts_page_code == 200

    def test_create(self):
        payload = {'title':'my simple test', 'body':'passed well', 'userId':'15'}
        response = requests.post(urljoin(BASEURL, 'posts'), data=payload).json()
        assert response['title'] == 'my simple test'
        assert response['body'] == 'passed well'
        assert response['userId'] == '15'

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