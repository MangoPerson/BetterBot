python -m venv .venv
call .venv\Scripts\activate.bat
pip install pipenv
pipenv install
type nul > .env
echo TOKEN=_TOKEN_HERE_ >> .env
echo AI_KEY=_AI_KEY_HERE_ >> .env