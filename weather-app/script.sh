#!/bin/bash 



#Giving permission to file script.sh

chmod +x script.sh
#creating virtual enviroment as env

# Install Python virtual environment package if not already installed
#sudo apt-get install python3-venv
pip install virtualenv
python3 -m venv env
source ./env/bin/activate
#cd env && cd bin && source activate
which python
python -c "import sys; print(sys.executable)"

# Check if environment is activated
python -c "import sys; print('Python environment is activated' if hasattr(sys, 'real_prefix') else 'Python environment is not activated')"

#Instaling requiremt of projects

pip install -r requirements.txt

#to run this script type ./script.sh
# Create and activate the Python environment
python3 manage.py migrate

python3 manage.py runserver

deactivate
