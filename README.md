# Getting started

## **Backend**

**Step 0:** Requirements

In our project we use: GIT, [Docker](https://docs.docker.com/desktop/windows/wsl/), Python 3.10.

If you use Windows — WSL 2 should be **[installed](https://learn.microsoft.com/en-us/windows/wsl/install)**.

Also needed:

1. Make tool

    ```bash
    sudo apt update && sudo apt-get -y install make
    ```

   For Windows users

   Install chocolatey from [here](https://chocolatey.org/install). Then run:

    ```shell
    choco install make
    ```

**Step 1**: Clone the backend project repository. Notice that we are currently developing at dev branch.

```bash
git clone git@github.com:likecompany/auth.git
cd abra_back
mv .env_dist .env
```

#### For backend

Do more step:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install poetry
poetry install
pre-commit install
sh scripts/mypy.sh
```

**Step 2:** Build and Run the Docker Container

2.1. Create `.env` file to the root of the project folder.

2.2. To start the project in Docker run:

```shell
make build
make migrations
make application
make application-logs
```

To run the project locally:

```shell
python3 app/main.py
```

2.3 You can find OpenAPI schema at http://localhost/docs

**Step 3:** Understand the architecture

3.1 You might be overwhelmed by the amount of custom elements in the project. But let me reassure you that it’s quite
easy to use once you get the gist.

3.4 We try to keep our code as much typed as possible. All inputs and outputs of any endpoint must be typed. You can
find schemas at app/schemas. Feel free to add new schemas but examine existing ones first.

3.5 All common functions (*auth*, *session*) are kept at `app/core/depends`. Before writing new piece of
code
make sure it has not been written yet ;)

********************Step 4:******************** Develop!

4.1 We use a bunch of code analysers. You can find full list at `.pre-commit-config.yaml`. They run automatically on
every
commit. Please notice that some of them (*black*, *isort*) can modify your code. If it is the case please run:

```shell
git add [filename]
```

again on the files that were changed.
