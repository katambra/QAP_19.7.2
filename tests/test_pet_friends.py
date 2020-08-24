from api import PetFriends
from settings import valid_email, valid_password, invalid_key


class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_get_all_pets_with_valid_key(self, filter=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_add_new_pet_with_valid_data(self, name='Буся', animal_type='толстопес',
                                         age=4, pet_photo='images/dog.jpg'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_successful_update_self_pet_info(self, name='Марли', animal_type='лабр', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

    def test_successful_delete_self_pet(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) == 0:
            self.pf.post_new_pet(auth_key, "Супер", "пес", 3, "images/dog.jpg")
            _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()

    def test_successful_create_pet_simple(self, name='Джо', animal_type='пес',
                                         age=3):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)

        assert status == 200
        assert result['name'] == name

    def test_successful_set_photo(self, pet_photo='images/dog.jpg'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        status, result = self.pf.set_photo(auth_key, pet_id, pet_photo)
        assert status == 200
        assert 'pet_photo' in result

    def test_get_api_key_with_invalid_email(self, email='katatambra@list.ru', password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_get_api_key_with_invalid_password(self, email=valid_email, password='asdf123'):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_get_all_pets_with_invalid_key(self, filter=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        auth_key = invalid_key
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_add_new_pet_with_invalid_age(self, name='Буся', animal_type='толстопес',
                                         age='сто', pet_photo='images/dog.jpg'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_add_new_pet_with_invalid_photo(self, name='Буся', animal_type='толстопес',
                                         age=4, pet_photo='images/Template.pdf'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_failed_update_self_pet_info_no_name(self, name='', animal_type='лабр', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

    def test_failed_delete_self_pet_invalid_key(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) == 0:
            self.pf.post_new_pet(auth_key, "Супер", "пес", 3, "images/dog.jpg")
            _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")
        auth_key = invalid_key
        pet_id = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()

    def test_failed_set_photo_invalid_format(self, pet_photo='images/Template.pdf'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        status, result = self.pf.set_photo(auth_key, pet_id, pet_photo)
        assert status == 200
        assert 'pet_photo' in result

    def test_failed_create_pet_simple_no_data(self, name='', animal_type='',
                                         age=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)

        assert status == 200
        assert result['name'] == name