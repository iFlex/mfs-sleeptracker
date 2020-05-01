import sys
sys.path.insert(0,'./python')

from fitbit_translator import Translator
import json
from os import walk

translator = Translator({'user':'tester'})
test_data_store = {}


def load_test_data(name, path):
    global test_data_store

    with open(path,"r") as f:
        test_data_store[name] = json.loads(f.read())


def load_all_test_data_files(path):
    print(walk(path))
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            load_test_data(filename, dirpath+filename)
        break

load_all_test_data_files("./test/resources")

def test_heartrate_successful_translation():
    pass #translator.translate('') 

def test_heartrate_failing_translation():
    pass #translator.translate('') 

def test_sleep_successful_translation():
    pass #translator.translate('') 

def test_sleep_failing_translation():
    pass #translator.translate('') 

def test_weight_successful_translation():
    pass #translator.translate('') 

def test_weight_failing_translation():
    pass #translator.translate('') 