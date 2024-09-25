pyinstaller main.py --noconfirm --onefile --paths "./venv/Lib/site-packages"
#New-Item -ItemType Directory -Path "./dist/src/ecac/relacao_pgtos/" -Force
#Copy-Item -Path "./src/ecac/relacao_pgtos/codigos_receita.json" -Destination "./dist/src/ecac/relacao_pgtos/"

clear
Write-Host "Build concluído com sucesso!"