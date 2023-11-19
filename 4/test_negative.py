import yaml
from sshcheckers import ssh_checkout_negative

with open('config.yaml') as file:
    data = yaml.safe_load(file)


class TestNegative:

    def test_step1(self, make_bad_arx):
        # test1 ======== take docs from folder: out and copy this docs to folder1
        assert ssh_checkout_negative("127.0.0.1", "user2", "test",
                                     "cd {}; 7z e bad_arx.{} -o{} -y".format(data["folder_out"], data["type"],
                                                                             data["folder_ext1"]),
                                     "ERROR"), "Test1 FAIL"

    def test_step2(self):
        # test2 =========show info about arx2.7z
        assert ssh_checkout_negative("127.0.0.1", "user2", "test",
                                     "cd {}; 7z t bad_arx.{}".format(data["folder_out"], data["type"]),
                                     "ERROR"), "Test2 FAIL"
