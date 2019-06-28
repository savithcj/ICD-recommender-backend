import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str)  # mode for setUseNumbers
options = vars(parser.parse_args())

print("Running importRules")
os.system("python manage.py importRules")

print("Running generateCodeTable")
os.system("python manage.py generateCodeTable")

print("Running generateTreeCodeTable")
os.system("python manage.py generateTreeCodeTable")

print("Running generateDaggerAsterisk")
os.system("python manage.py generateDaggerAsterisk")

print("Running setUseNumbers")
if options["mode"]:
    os.system("python manage.py setUseNumbers -m " + options["mode"])  # Sets numbers randomly
else:
    os.system("python manage.py setUseNumbers")  # Sets numbers to 0

print("Running calcBlockUseNumbers")
os.system("python manage.py calcBlockUseNumbers")
