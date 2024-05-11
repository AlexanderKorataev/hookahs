import pytest
import cv2

from src.object_management.object import Object

@pytest.fixture
def sample_object():
    return Object(user_id=1, floating_id=10)

def test_set_gps_coords(sample_object):
    assert sample_object.gps_coords is None
    sample_object.set_gps_coords('123.456')
    assert sample_object.gps_coords == '123.456'

def test_get_age_or_set(sample_object, mocker):
    mocker.patch('src.object_management.object.getAge')

    assert sample_object.age is None

    image = cv2.imread(f'./notebooks/faces/{sample_object.user_id}')

    result = sample_object.get_age_or_set(image)

    assert sample_object.age
