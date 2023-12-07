import os

os.system('python -m pip install --upgrade pip')
os.system('pip install -r requirements.txt')
os.system('cls')

from sped_vs_sefaz import sped_vs_sefaz

sped_vs_sefaz()