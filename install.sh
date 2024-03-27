python3 -m venv .venv
source .venv/bin/activate
pip install pipenv
pipenv install
touch .env
echo "TOKEN=_TOKEN_HERE_\nAI_KEY=_YOUR_KEY_HERE_" >> .env