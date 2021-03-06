# tinfoil-client-redirector
Flask application designed to accept requests only from valid Tinfoil clients.

## Run tinfoil-client-redirector as local development server for testing
### PowerShell
```
$env:FLASK_APP = "tinfoil_client_redirector"
$env:FLASK_ENV = "development"
flask run --host=0.0.0.0
```

## To import Tinfoil auth value to database
```
flask import-auth-value KEY VALUE
```
