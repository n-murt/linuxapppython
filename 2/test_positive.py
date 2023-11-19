# Условие:
# Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).


import subprocess
import os
from pathlib import Path


tst = "/tmp/tst"
out = "/tmp/out"
folder1 = "/tmp/folder1"


def checkout(cmd, text):
    result = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False

    # подготавливаем директории


def setup():
    if not os.path.exists(tst):
        os.makedirs(tst)
    if not os.path.exists(out):
        os.makedirs(out)
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    if not os.path.exists(tst+'/path'):
        os.makedirs(tst+'/path')
    Path(tst+'/one').touch()
    Path(tst+'/two').touch()
    Path(tst+'/path/three').touch()
    with open(tst+'/one', 'w') as f:
        f.write('This is a file with some content.')
        f.close

    with open(tst+'/two', 'w') as w:
        w.write('This is a file with some content.')
        w.close

    with open(tst+'/path/three', 'w') as w:
        w.write('This is a file with some content.')
        w.close


def test_step1():
    # test1 =================== create archive
    result1 = checkout(
        "cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    # check if arx2.7z in out
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "Test1 FAIL"


def test_step2():
    # test1 ======== take docs from folder: out and copy this docs to folder1
    result1 = checkout(
        "cd {}; 7z e arx2.7z -o{} -y".format(out, folder1), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder1), "one")
    result3 = checkout("cd {}; ls".format(folder1), "two")
    result4 = checkout("cd {}; ls".format(folder1), "three")
    assert result1 and result2 and result3 and result4, "Test2 FAIL"


def test_step2_1():
    # test1 ======== take docs from folder: out and copy this docs to folder1
    result1 = checkout(
        "cd {}; 7z x arx2.7z -o{} -y".format(out, folder1), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder1), "one")
    result3 = checkout("cd {}; ls".format(folder1), "two")
    result4 = checkout("cd {}; ls".format(folder1+'/path'), "three")
    assert result1 and result2 and result3 and result4, "Test2_1 FAIL"


def test_step3():
    # test3 =========show info about arx2.7z
    assert checkout("cd {}; 7z t arx2.7z".format(out),
                    "Everything is Ok"), "Test3 FAIL"


def test_step3_1():
    # test3 =========show info about arx2.7z
    assert checkout("cd {}; 7z l arx2.7z".format(out),
                    "Name"), "Test3_1 FAIL"


def test_step4():
    # test4 ========= add archive update
    assert checkout("cd {}; 7z u {}/arx2.7z".format(tst, out),
                    "Everything is Ok"), "Test4 FAIL"


def test_step5():
    # test5 ========= delete docs one and two from archive in folder out
    assert checkout("cd {}; 7z d arx2.7z".format(out),
                    "Everything is Ok"), "Test5 FAIL"
