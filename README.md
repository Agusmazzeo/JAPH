# JAPH

### This is _Just Another Project Helper_ so we dont suffer too much setting up projects in our local environment.

![alt text](docker+python.png)

---

## How to start?

First, let's install the helper. You will need Python 3.6 or newer:

```
python3 -m pip install git+https://github.com/Agusmazzeo/JAPH.git@master
```

We only need a _config.yaml_ file to set up everything and start working:

```yaml
projects:
  - title: ExampleProject1
    description: One example project
    services:
      - name: one_ui
        type: UI
        pre_start:
          - npm install
        command: ng serve
        volume: /Users/ExampleProject1

      - name: one_api
        type: BE

      - name: one_db
        type: DB

  - title: ExampleProject2
    description: Another example project
    services:
      - name: another_ui
        type: UI
        command: ng serve
        volume: /Users/ExampleProject2

      - name: another_api
        type: BE

docker_compose_files:
  - /Users/me/ExampleProject1/docker/docker-compose.yml
  - /Users/me/ExampleProject2/docker/docker-compose.yml
```

Let's explain this config file:

- **Projects**: Group of services that we want to set up at the same time.
  - **Title**: Name of the project. Just a way to organize the group of services.
  - **Description**: A brief description of the project.
  - **Services**: List of services that we want in the project.
    - **Name**: Name of the service. This value must be the same that is in the docker-compose file (if its containarized).
    - **Type**: Service type. Some options are UI (User interface), BE (Backend), DB (Database).
    - **Pre_Start**: List of commands that will be run before the main command. This is an Optional field.
    - **Command**: Main command that the service will run. This is an Optional field. If this field is not set, japh will try to find a docker service with this service name.
    - **Volume**: Absolute directory where the Command will be run, if set.
- **Docker_Compose_Files**: List of docker-compose files where the services without command will be searched and set up.

## How to use?

**Usage**:

```console
$ japh [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `up`
- `down`
- `restart`
- `recreate`
- `build`

---

## `japh up`

**Usage**:

```console
$ japh up PROJECT [OPTIONS]
```

**Arguments**:

- `PROJECT`: [required]

**Options**:

- `--name TEXT`: Services' name to set up
- `--type TEXT`: Services' type to set up
- `--attached / --no-attached`: Flag for creating containers attached to shell execution [default: False]
- `--background / --no-background`: Flag for setting on service's logs [default: False]
- `--file-dir TEXT`: Config file path [default: False]
- `--help`: Show this message and exit.

---

## `japh down`

**Usage**:

```console
$ japh down [OPTIONS]
```

**Options**:

- `--file-dir TEXT`: Config file path [default: False]
- `--help`: Show this message and exit.

---

## `japh restart`

**Usage**:

```console
$ japh restart PROJECT [OPTIONS]
```

**Arguments**:

- `PROJECT`: [required]

**Options**:

- `--name TEXT`: Service name to restart (docker restart, not destroy)
- `--file-dir TEXT`: Config file path [default: False]
- `--help`: Show this message and exit.

---

## `japh recreate`

**Usage**:

```console
$ japh recreate PROJECT [OPTIONS]
```

**Arguments**:

- `PROJECT`: [required]

**Options**:

- `--name TEXT`: Service name to recreate (destroy and set up again)
- `--file-dir TEXT`: Config file path [default: False]
- `--help`: Show this message and exit.

---

## `japh build`

**Usage**:

```console
$ japh recreate PROJECT [OPTIONS]
```

**Arguments**:

- `PROJECT`: [required]

**Options**:

- `--name TEXT`: Service name to build
- `--no-cache BOOL`: Flag to indicate if cached information must be used during build.
- `--file-dir TEXT`: Config file path [default: False]
- `--help`: Show this message and exit.
