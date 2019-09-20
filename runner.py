
from shutil import copyfile
import os

class Runner:
    def __init__(self):
        print("------------------------------------------------------")
        print("-                                                    -")
        print("-     DISCRETE EVENTS SYSTEMS SIMULATOR - SETUP      -")
        print("-                                                    -")
        print("------------------------------------------------------\n\n")

        PATH = input("Please, input the target folder name: ")

        settings = File_object = open("settings.py","w")
        settings.write("PATH = \"" + PATH + "/\"" )
        settings.close()

        os.mkdir(os.getcwd()+ "/"+ PATH)
        copyfile('input.txt', PATH+"/input.txt" )
    
if __name__ == '__main__':
    x = Runner()
    