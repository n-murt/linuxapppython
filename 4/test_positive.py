import subprocess
import yaml
from sshcheckers import ssh_checkout

with open('config.yaml') as file:
    data = yaml.safe_load(file)

    # подготавливаем директории


class TestPositive:

    def test_step1(self, make_bad_arx):
        # test1 =================== create archive
        result1 = ssh_checkout("127.0.0.1", "user2", "test",
                               "cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data["type"], data["folder_out"]),
                               "Everything is Ok")
        # check if arx2.7z in out
        result2 = ssh_checkout("127.0.0.1", "user2", "test", "cd {}; ls".format(data["folder_out"]),
                               "arx2.{}".format(data["type"]))
        assert result1 and result2, "Test1 FAIL"

    def test_step2(self, make_files):
        # test1 ======== take docs from folder: out and copy this docs to folder1
        result1 = ssh_checkout("127.0.0.1", "user2", "test",
                               "cd {}; 7z e arx2.{} -o{} -y".format(data["folder_out"], data["type"],
                                                                    data["folder_ext1"]),
                               "Everything is Ok")
        result2 = ssh_checkout("127.0.0.1", "user2", "test", "cd {}; ls".format(data["folder_ext1"]), make_files[0])
        assert result1 and result2, "Test2 FAIL"

    #    def test_step2_1(self):
    #        # test1 ======== take docs from folder: out and copy this docs to folder1
    #        result1 = checkout(
    #            "cd {}; 7z x arx2.7z -o{} -y".format(data["folder_out"], data["folder_ext1"]), "Everything is Ok")
    #        result2 = checkout("cd {}; ls".format(data["folder_ext1"]), "one")
    #        result3 = checkout("cd {}; ls".format(data["folder_ext1"]), "two")
    #        result4 = checkout("cd {}; ls".format(
    #            data["folder_ext1"]+'/path'), "three")
    #        assert result1 and result2 and result3 and result4, "Test2_1 FAIL"

    def test_step3(self):
        # test3 =========show info about arx2.7z
        assert ssh_checkout("127.0.0.1", "user2", "test",
                            "cd {}; 7z t arx2.{}".format(data["folder_out"], data["type"]),
                            "Everything is Ok"), "Test3 FAIL"

    def test_step3_1(self):
        # test3 =========show info about arx2.7z
        assert ssh_checkout("127.0.0.1", "user2", "test",
                            "cd {}; 7z l arx2.{}".format(data["folder_out"], data["type"]),
                            "Name"), "Test3_1 FAIL"

    def test_step4(self):
        # test4 ========= add archive update
        assert ssh_checkout("127.0.0.1", "user2", "test",
                            "cd {}; 7z u {}/arx2.{}".format(data["folder_in"], data["folder_out"], data["type"]),
                            "Everything is Ok"), "Test4 FAIL"

    def test_step5(self):
        # test5 ========= delete docs one and two from archive in folder out
        assert ssh_checkout("127.0.0.1", "user2", "test",
                            "cd {}; 7z d arx2.{}".format(data["folder_out"], data["type"]),
                            "Everything is Ok"), "Test5 FAIL"

    def test_step6(self):
        # test6 ========= check crc32
        res = subprocess.run("crc32 /home/user/out/arx2.7z", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        assert ssh_checkout("127.0.0.1", "user2", "test",
                            "cd {}; 7z h arx2.{}".format(data["folder_out"], data["type"]),
                            res.stdout.rstrip().upper()), "test6 FAIL"
