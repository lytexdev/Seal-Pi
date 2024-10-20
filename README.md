# Seal-Pi

## Overview
Seal-Pi is a Flask-based web application with Vue.js to display security camera footage.

## Installation
***There will be soon a docker setup***

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