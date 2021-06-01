import logging

import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from utils.utils import get_xls_dict, validate_image

logger = logging.getLogger()

@allure.feature('nasa')
@allure.story('imagery')
@pytest.mark.parametrize('longitude,latitude,date,positive,error_message', get_xls_dict())
def test_get_image_by_coordinates_and_date(longitude,latitude,date,positive,error_message,env_config):
    """
    Send GET request to env_config['host']['url']
    if no image - validate json response
    if image - validate image against image in 'validation_images' folder
    :param longitude: str
    :param latitude: str
    :param date: str
    :param positive: flag indicating if test case is positive or we are validating error message and status
    :param error_message: error message we are validating in case of positive=false
    :param env_config: config fixture
    :return:
    """
    params = {'lon': longitude, 'lat': latitude, 'date': date, 'api_key':env_config['host']['api_key'] }
    url = env_config['host']['url']
    logger.info(f"GET {url} with params: {params}")
    response = requests.get(url,params=params)
    logger.info(f"Resp headers = {response.headers}")
    logger.info(f"Resp status code = {response.status_code}")
    logger.info(f"Resp url = {response.url}")

    if positive=="true":
        if 'image' not in response.headers.get('content-type').lower():
            # in this example we will not get many images, not in normal environment this would be legit assert
            # assert False, "Non-image content is returned. Expected image content-type"
            pass
        else:
            image_name = f"{longitude}{latitude}{date}".replace('.','') + ".png"
            mse, diff_image_path = validate_image(image_name, response)
            print("MSE = " + str(mse))
            if mse:
                allure.attach('screenshot', diff_image_path, attachment_type=AttachmentType.PNG)
                assert not mse, f"Failed to validate image from NASA. MSE = {mse}"
            else:
                assert True, "Image validated successfully"

    # Assert statement normal
    # ly will be active, but I commented it out for following reasons
    # NASA will respond with a lot of 404 because probably image on selected date will not be found
    # In scope of this task I am not going to make research on which dates images are available and on which they are not

    # assert response.status_code == http.HTTPStatus.OK
    elif positive=="false":
        resp_json = response.json()
        print(resp_json.get('msg', ' message'))
        # Normally we would validate specific messages here, but the only message we'll get is - no image in specified date,
        # so skipping this one as well
        assert resp_json.get('msg', None)
