# Seal-Pi

## Overview
Seal-Pi is a Flask-Vue based web-application developed for RaspberryPi to display camera footage and soon more.

## Installation
***There will be soon a docker-compose setup***

**Clone the repository**
```bash
git clone https://github.com/lytexdev/Seal-Pi.git
cd Seal-Pi
```

**Copy .env.example to .env and adjust it**
```bash
cp .env.example .env
```

**Install dependencies**
```bash
pip install -r requirements.txt
cd ./frontend
npm install
```

**Build frontend**
```bash
./seal build
```

**Start Flask server**
```bash
python3 app.py
```

## License
This project is licensed under the GNU General Public License v3 - see the [LICENSE](LICENSE) file for details.
