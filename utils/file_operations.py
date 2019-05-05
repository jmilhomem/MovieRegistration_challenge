import sys
import json
import pprint
from typing import List, Union, Dict

# path where the files live
path_filename = sys.path[0] + "/utils/files/"


def save_to_file(content, filename, type_operation="a") -> bool:
    """
    save_to_file(content, filename, type_operation="a")
    :param: content and filename
    :return: True or False
    Function receives two parameters: content, filename and type_operation and it save the content into a file.
    type_operation = By default, it appends data. If "o" it overwrites the data file.
    """

    filename_splitted, extensionfile = str(filename).split(".")

    try:
        if type_operation == "o":
            file = open(path_filename + filename, "w")
            if str(extensionfile).lower() == "json":
                file.write(json.dumps(content) + "\n")
            else:
                file.write(str(content) + "\n")
            file.close()
            return True
        else:
            file = open(path_filename + filename, "a")
            if str(extensionfile).lower() == "json":
                file.write(json.dumps(content) + "\n")
            else:
                file.write(str(content) + "\n")
            file.close()
            return True

    except json.JSONDecodeError as e_json:
        print(f"\nYour settings file(s) contains invalid JSON syntax. {str(e_json)}")
        return False
    except Exception as e:
        print(f"\nOccurred an error during saving operation. Contact you support for help! {str(e)}")
        return False


def read_file(filename) -> List:
    """
    read_file(filename)
    :param: filename (filename.extension)
    :return: a list of data or False (If some error occurs)
    Function receives the filename as parameter and returns a list with the content.
    Files must be in txt, csv or json format.
    Important: json format must be as [{key:value}, {key2:value2}, ...]
    """

    try:
        filename_splitted, extensionfile = str(filename).split(".")
        if str(extensionfile).lower() == "txt":
            file = open(path_filename + filename, "r")
            file_read = [x.strip() for x in file.readlines()]
            file.close
            return file_read
        elif str(extensionfile).lower() == "csv":
            file = open(path_filename + filename, "r")
            file_treated = [x.strip() for x in file.readlines()]
            file_read = [x.split(",") for x in file_treated]
            file.close
            return file_read
        elif str(extensionfile).lower() == "json":
            #print(path_filename + filename)
            file = open(path_filename + filename, "r")
            file_read = json.load(file)
            file.close
            return file_read
        else:
            raise RuntimeError(f"\nFormat of file not supported. Supported formats: txt, csv and json.")
            return []
    except json.JSONDecodeError as e_json:
        print(f"\nThe {filename} file is empty or the file settings contains invalid JSON syntax. {str(e_json)}")
        return []
    except Exception as e:
        print(f"\nOccurred an error during reading file operation.\nError description: {str(e)}")
        return []
