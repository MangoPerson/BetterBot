python3 -m venv .venv
source .venv/bin/activate
pip install pipenv
pipenv install
touch .env
echo TOKEN=_TOKEN_HERE_ >> .env
echo AI_KEY=_AI_KEY_HERE_ >> .env