# build.ps1

param(
    [string]$BASE_DIR = (Get-Location).Path,
    [string]$Command
)

function Build {
    docker build -t calculator-app .
}

function Run {
    docker run --rm --volume "${BASE_DIR}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest python -B app/calc.py
}

function Server {
    docker run --rm --volume "${BASE_DIR}:/opt/calc" --name apiserver --env PYTHONPATH=/opt/calc --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
}

function Interactive {
    docker run -ti --rm --volume "${BASE_DIR}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest bash
}

function TestUnit {
    docker run --rm --volume "${BASE_DIR}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest pytest --cov --cov-report=xml:results/coverage.xml --cov-report=html:results/coverage --junit-xml=results/unit_result.xml -m unit
    docker run --rm --volume "${BASE_DIR}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/unit_result.xml results/unit_result.html
}

function TestAPI {
    docker network create calc-test-api
    docker run -d --rm --volume "${BASE_DIR}:/opt/calc" --network calc-test-api --env PYTHONPATH=/opt/calc --name apiserver --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
    docker run --rm --volume "${BASE_DIR}:/opt/calc" --network calc-test-api --env PYTHONPATH=/opt/calc --env BASE_URL=http://apiserver:5000/ -w /opt/calc calculator-app:latest pytest --junit-xml=results/api_result.xml -m api
    docker run --rm --volume "${BASE_DIR}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/api_result.xml results/api_result.html
    docker rm --force apiserver
    docker network rm calc-test-api
}

switch ($Command) {
    "build" { Build }
    "run" { Run }
    "server" { Server }
    "interactive" { Interactive }
    "test-unit" { TestUnit }
    "test-api" { TestAPI }
    default { Write-Host "Comando no reconocido: $Command" }
}
