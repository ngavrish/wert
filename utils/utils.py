import os
import cv2
import numpy as np
import xlrd
import yaml


def get_root_path():
    """
    get project root path
    :return: String
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def get_xls_dict():
    """
    get dictionary filled with data from parsed exel file
    :return: Dict
    """
    config = get_config_dict()
    cls = []
    excel_file = xlrd.open_workbook(os.path.abspath(os.path.join(get_root_path(), config.get('test_data_path'), 'testdata.xlsx')))
    sheet = excel_file.sheet_by_name('Sheet1')
    nrows = sheet.nrows
    for i in range(nrows):
        cls.append(sheet.row_values(i))
    return cls

def get_config_dict():
    """
    get dictionary filled with parsed yaml config file
    :return: Dict
    """
    config_path = os.path.abspath(os.path.join(get_root_path(), 'config', 'env_config.yml'))
    with open(config_path) as f:
        return yaml.load(f)

def validate_image(image_name, response):
    """
    validate captured image against stored image in validation_images folder
    :param image_name:  validation and stored images share name, but different path
    :param response: get response
    :return: Int, String
    """
    diff_image_path = None
    env_config = get_config_dict()
    rest_image_file = open(os.path.join(get_root_path(), env_config['testrun_images_path'], image_name), "wb")
    rest_image_file.write(response.content)
    rest_image_file.close()
    rest_image = cv2.imread(os.path.join(get_root_path(), env_config['testrun_images_path'], image_name))
    validation_image = cv2.imread(os.path.join(get_root_path(), env_config['validation_images_path'], image_name))
    mse = np.sum(np.abs(rest_image - validation_image))
    if mse != 0:
        diff_image_path = os.path.join(get_root_path(), env_config['validation_images_path'], f"diff_{image_name}")
        cv2.imwrite(os.path.join(get_root_path(), env_config['validation_images_path'], f"diff_{image_name}"),
                    np.abs(rest_image - validation_image))
    return mse, diff_image_path
