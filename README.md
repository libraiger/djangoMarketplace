![304739666-a74021ea-9e83-4b79-b944-6f367cf906d9](https://github.com/libraiger/djangoMarketplace/assets/48214830/34206574-7abe-499b-9d87-e613042c82d9)


## Setting Up Your Development Environment

### Without Docker

#### Database Set Up

Before cloning and running the project, make sure to have PostgreSQL install on your machine. You can either download and install PostgreSQL or you can use the Docker image of PostgreSQL.

You can download the latest version of PostgreSQL [here](https://www.postgresql.org/download/). Follow the instructions and install it.
You can also pull the image of PostgreSQL. It is assumed that you have Docker install on your machine. After that, you can pull it with this command:

`docker pull postgres`

By default, the OpenUnited platform will look for a database named `ou_db` and use `postgres` as both the username and password.
For development purposes, if you already have a postgres server running locally with this default username/password combination, the easiest thing is to just create a database named: `ou_db`.
To override the database settings, you can copy `.env.example` to `.env` and set the values you want.

#### Running the Project

When the database it set up, copy `.env.example` to `.env`, if you haven't already, generate `DJANGO_SECRET_KEY` using [this website](https://djecrety.ir/) and set the value on the `.env` file.
After that, run the following commands:

```bash
git clone git@github.com:<your-username>/platform.git
cd platform
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=openunited.settings.development
./setup.sh
```

Run the tests:

`python manage.py test`

Finally, start the server:

`python manage.py runserver`

Then navigate to: http://localhost:8000/ in your browser.

#### Customizations

If you want to extend your local development, create a `local.py` in `openunited/settings`. Import `base.py` or `development.py` and make sure to export it:

`export DJANGO_SETTINGS_MODULE=openunited.settings.local`

*It is advised to put this line into your bash configuration.*

### With Docker

Make sure you have docker install on your machine.

```
cp .env.example .env
cp docker.env.example docker.env

# create a network named as platform_default
docker network create platform_default

docker compose --env-file docker.env up --build
```

Run the tests:

`docker-compose --env-file docker.env exec platform sh -c "python manage.py test"`

Then navigate to: http://localhost:8000/ in your browser.

**Notes: Docker Networking**

- For linux machine you can set the `network_name=host` in `docker.env`
- For docker desktop in Mac or Windows you can set the custom network `network_name=custom_network_name` in `docker.env`.
(N.B. If you facing issue like `network custom_network_name not found`, you have to create it like `docker network create custom_network_name` )

**Not working?** Please double-check your settings and if you still continue to experience problems, [create an issue](https://github.com/OpenUnited/platform/issues) detailing your problem.

#### Docker Compose Notes

- If you want to have auto-reload during development and use ipdb/pdb/breakpoint add following to docker-compose.yml > services > platform

```yaml
services:
  platform:
    # ...
    volumes:
      - .:/code/
    # ...
    stdin_open: true
    tty: true

```

- After adding ipdb/pdb/breakpoint, you can check container id by `docker ps` and attach it to debug `docker attach <container-id>`

### How to Make a Contribution

Before moving on, please make sure that the project is run locally on your machine without any problem.

Here's a quick rundown on how you can make a contribution:

1) Find an issue that you are interested in addressing or a feature that you would like to add.
2) Create a new branch for your fix using `git checkout -b branch-name-here`
3) Make the appropriate changes for the issue you are trying to address or the feature that you want to add.
4) Use `git add insert-paths-of-changed-files-here` to add the file contents of the changed files.
5) Commit your changes. The commit messages should follow [this format](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commit-message-format).
6) Push the changes to the remote repository using `git push origin branch-name-here` and submit a pull request.
7) Wait for the pull request to be reviewed by a maintainer.
8) Make changes to the pull request if the reviewing maintainer recommends them.
9) Celebrate your success after your pull request is merged!

#### Making Changes

Every change that is made needs to be formatted according to [Black](https://black.readthedocs.io/en/stable/).
You can run `black .` before pushing your changes but it is recommended to use an extenstion that runs this command every time you save a file.
For VS Code, you can install the extension in [here](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter).

- If your changes introduces a new feature, make sure to include the necessary tests such as unit tests, integration tests etc.
- If your changes modifies the existing implementation, make sure to extend and/or modify the tests.
- If your changes requires an update on the documentation, please update the documentation accordingly.

**NOTE:** If your work includes changes in the front-end, make sure to run `watch_css_changes.sh` script during the development. Otherwise, the styles might not apply.
