@echo off
echo Copying default config and data files...
copy .\src\data.example.json .\src\data.json
copy .\src\config.example.json .\src\config.json

echo Creating virtual environment...
python -m venv recluse-env