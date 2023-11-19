# Условие:
# Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).

import subprocess
import os
from pathlib import Path

tst = "/tmp/tst"
out = "/tmp/out"
folder1 = "/tmp/folder1"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False



def setup():
    if not os.path.exists(tst):
        os.makedirs(tst)
    if not os.path.exists(out):
        os.makedirs(out)
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    Path(out+'/bad_arx.7z').touch()


def test_step1():
    # test1 ======== take docs from folder: out and copy this docs to folder1
    assert checkout("cd {}; 7z e bad_arx.7z -o{} -y".format(out,
                    folder1), "ERROR"), "Test1 FAIL"


def test_step2():
    # test2 =========show info about arx2.7z
    assert checkout("cd {}; 7z t bad_arx.7z".format(out),
                    "ERROR"), "Test2 FAIL"
