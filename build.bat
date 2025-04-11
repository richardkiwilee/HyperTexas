rm -rf build
rm -rf dist
pyinstaller.exe --paths=./HyperTexas HyperTexas/main.py -n HyperTexas -y -F
