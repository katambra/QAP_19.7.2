import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email: str, password: str) -> json:
        """делает запрос к API сервера и возвращает статус и результат
        в формате json + уникальный ключ пользователя, найденный по регистрационным данным"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """делает запрос к API сервера и возвращает статус и результат в формате
        json со списком питомцев в соответствии с фильтром. У фильтра либо пустое
        значение - список всех питомцев, либо 'my_pets' - список собственных питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """отправляет данные о новом питомце и возвращает статус и результат в формате json
        с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """отправляет запрос на изменение данных существующего питомца на сервер по указанному ID,
        возвращает статус и результата в формате json с обновленными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """отправляет на сервер запрос на удаление питомца по ID, возвращает статус
        и результат в формате json с текстом уведомления об удалении. На сегодняшний день
        тут есть баг - приходит пустая строка, но статус при этом 200"""
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """отправляет усеченные данные о новом питомце (без фото) и возвращает статус и результат
        в формате json с данными добавленного питомца"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def set_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """отправляет запрос на частичное изменение данных существующего питомца на сервер по указанному ID,
        а именно - публикацию фото, возвращает статус и результата в формате json с обновленными данными питомца"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/'+ pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
