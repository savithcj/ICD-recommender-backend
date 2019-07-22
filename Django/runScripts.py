import os
import argparse

# This script is used to run all of the setup scripts

parser = argparse.ArgumentParser()
# mode for setUseNumbers - 'random' for random numbers, otherwise numbers are set to 0
parser.add_argument('-m', '--mode', type=str)
options = vars(parser.parse_args())

# Importing rules
print("\n***********Running importRules***********")
os.system("python manage.py importRules")

# Generating the code table
print("\n***********Running generateCodeTable***********")
os.system("python manage.py generateCodeTable")

# Generating the tree code table
print("\n***********Running generateTreeCodeTable***********")
os.system("python manage.py generateTreeCodeTable")

# Generating the dagger asterisk table
print("\n***********Running generateDaggerAsterisk***********")
os.system("python manage.py generateDaggerAsterisk")

# Running the usage numbers with entered mode
print("\n***********Running setUseNumbers***********")
if options["mode"]:
    os.system("python manage.py setUseNumbers -m " + options["mode"])  # Sets numbers randomly
else:
    os.system("python manage.py setUseNumbers")  # Sets numbers to 0

# Calculating block use numbers
print("\n***********Running calcBlockUseNumbers***********")
os.system("python manage.py calcBlockUseNumbers")
