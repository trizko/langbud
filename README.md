# langbud - a spanish teaching companion 

### Requirements
You will need to install the following on your machine:
- python
- pip
- virtualenv

### Installation
To install the application, run the following commands from the root directory of this repository:
```bash
# create a virtualenv
python3.10 -m venv venv

# activate that virtualenv
source venv/bin/activate

# (if needed) update pip
pip install --upgrade pip

# install the dependencies
pip install -r requirements.txt
```

### Start
To start the application, run the following command:
```bash
python src/main.py
```