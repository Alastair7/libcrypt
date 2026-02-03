# LibCrypt

## What is LibCrypt?

A TUI application from where you can execute your own scripts easier than writing the whole command.

## How to run

### Configure the application

Before running LibCrypt it is required to add the enviroment variables (if they exist) and add the scripts path.

Create a file named `appconfig.yaml` and use the structure below to implement the app configuration.
If you don't use any enviroment variables you can set it as `environment_variables: {}`
```yaml
app:
  scripts_path: path/to/scripts/dir
  environment_variables:
    dev:
       VARIABLE1: VALUE 
       VARIABLE2: VALUE
    np:
       VARIABLE1: VALUE 
       VARIABLE2: VALUE
    prod:
       VARIABLE1: VALUE 
       VARIABLE2: VALUE
```

### Run LibCrypt

1. `uv sync`
2. `make run`
