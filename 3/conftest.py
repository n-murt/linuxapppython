import pytest
import yaml
import random
import string
from datetime import datetime
from checkers import checkout

with open('config.yaml') as file:
    data = yaml.safe_load(file)


@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.{}".format(data["folder_out"], data["type"]), "")


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return checkout(
        "mkdir {} {} {} {}".format(
            data["folder_in"], data["folder_out"], data["folder_ext1"], data["folder_ext2"]),
        "")


@pytest.fixture(autouse=True, scope="module")
def make_log():
    return checkout(
        "touch {}".format(
            data["folder_in"]),
        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename,
                                                                                           data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return checkout(
        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext1"],
                                            data["folder_ext2"]),
        "")


@pytest.fixture(autouse=True)
def log_test():
    fileavg = open("/proc/loadavg")
    with open(data["folder_in"] + "/stat.txt", "a") as file_object:
        file_object.write(datetime.now().strftime("%H:%M:%S.%f") + ", " + str(data["count"]) + ", " + data[
            "bs"] + ", " + fileavg.read())
