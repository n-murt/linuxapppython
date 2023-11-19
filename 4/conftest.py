import pytest
import yaml
import random
import string
from datetime import datetime
from sshcheckers import ssh_checkout, upload_files

with open('config.yaml') as file:
    data = yaml.safe_load(file)


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("127.0.0.1", "user2", "test", "cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]),
                 "Everything is Ok")
    ssh_checkout("127.0.0.1", "user2", "test", "truncate -s 1 {}/bad_arx.{}".format(data["folder_out"], data["type"]),
                 "")


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return ssh_checkout("127.0.0.1", "user2", "test",
                        "mkdir {} {} {} {}".format(
                            data["folder_in"], data["folder_out"], data["folder_ext1"], data["folder_ext2"]),
                        "")


@pytest.fixture(autouse=True, scope="module")
def make_log():
    return ssh_checkout("127.0.0.1", "user2", "test",
                        "touch {}".format(
                            data["folder_in"]),
                        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("127.0.0.1", "user2", "test",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename,
                                                                                               data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return ssh_checkout("127.0.0.1", "user2", "test",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext1"],
                                                            data["folder_ext2"]),
                        "")


@pytest.fixture(autouse=True)
def log_test():
    fileavg = open("/proc/loadavg")
    with open("/tmp/stat.txt", "a") as file_object:
        file_object.write(datetime.now().strftime("%H:%M:%S.%f") + ", " + str(data["count"]) + ", " + data[
            "bs"] + ", " + fileavg.read())


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("127.0.0.1", "user2", "test", "/tmp/p7zip-full.deb", "p7zip-full.deb")
    res.append(ssh_checkout("127.0.0.1", "user2", "test", "echo 'test' | sudo -S dpkg -i p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("127.0.0.1", "user2", "test", "echo 'test' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return all(res)
