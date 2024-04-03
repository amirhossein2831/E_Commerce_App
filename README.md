# :fire: Django E-Commerce Hub :fire:

## Empowering Your Online Shopping Experience :bento: :bento:

Welcome to the Django E-Commerce Hub, where we redefine your online shopping journey! Our platform offers a seamless and
secure environment for buyers and sellers alike. Explore a wide range of products, manage your shopping cart
effortlessly, and enjoy a smooth checkout process. Join us as we revolutionize the way you shop online!

## Acknowledgements

- [Virtual Environments](#virtual_env)
- [Env file](#env_file)
- [DB && Docker](#db)
- [Generate Fake DB Record](#factory)
- [Email, Celery with Flower](#celery)
- [Run Server](#run)
- [Swagger](#swagger)
- [Authors](#author)
- [Skills](#skill)
- [License](#license)

# Virtual Environments  <a name="virtual_env"></a>

I prefer to use Pipenv which is a tool that simplifies Python dependency management by automatically creating and
managing virtual environments for your projects. It combines the functionality of pip and virtualenv into a single
package, making it easier to manage dependencies and ensure project consistency.

- **Installation:** Install Pipenv using pip:
  if you already have pipenv jump this one
  ```bash
  pip install pipenv
  ```

- **Creating a Virtual Environment:** Create a virtual environment for your project:
  ```bash
  pipenv install
  ```
- [More about pipenv](https://pipenv.pypa.io/en/latest/)

# Env File  <a name="envfile"></a>

Environment variables are a way to store configuration settings or sensitive information that your application needs to
function properly. They are typically stored in a file named `.env` in the root directory of your project. Here's a
summary of how to use and manage environment variables in your project:

- **Creating an Environment File**

Create a file named `.env` in the root directory of your project. This file will store your environment variables.
you need to create variable for DB, redis, email connection

- **Adding Variables**

Add your environment variables to the `.env` file using the `KEY=VALUE` format. For example:

  ```plaintext
  # DB Connection
  
  CONNECTION=mysql,sql,..
  NAME=appname
  ROOT=username
  PASSWORD=password
  HOST=hostname
  PORT=portname
  
  # REDIS Connection
  
  REDIS_PORT=redisport
  REDIS_PASSWORD=redispassword
  FLOWER_PORT=flowerport
  
  # SMTP Connection
  
  EMAIL_TYPE=smtp,..
  EMAIL_HOST=Emailhost
  EMAIL_HOST_USER=username
  EMAIL_HOST_PASSWORD=password
  EMAIL_PORT=port

  ```

# DB && Dokcer <a name="db"></a>

fortunately We utilize Docker to manage our database environment. Docker enables containerization, simplifying
deployment across different environments.

We leverage Docker Compose to define and run multi-container Docker applications. Docker Compose reads environment
variables from a `.env` file and build from Dockerfile, allowing flexible configuration. feel free to update the docker
compose file as you need

To start the database and related services, execute:

```bash
docker compose up --build  
```

once you run it with `--build` just run `docker compose up` unless you changed the docker file

for running any command inside your container simple use `docker comopse run web command` EX:

```bash
docker compose run web python manage.py store_seed
```

# Generate Fake DB Record  <a name="factory"></a>

Factory Boy is a Python library that simplifies the creation of object instances in tests or database seeding. It
provides a convenient and flexible way to define factory classes for generating test data.

- **Data Generation:** Automatically generate values for fields based on predefined strategies or custom functions.
- **Seeding Databases:** Use Factory Boy to populate databases with test data, making it easier to set up and tear down
  test environments.

```bash
docker compose run web python manage.py store_seed
```

- some time may an error occur while seeding db but don't worry we use transaction so all record rollback
  and run it again

# Email, Celery with Flower <a name="celery"></a>

so app also support sending email for make it work you need to add your email server for that just add variable
to `.env` file

 ```plaintext
 
  # SMTP Connection
  
  EMAIL_TYPE=smtp,..
  EMAIL_HOST=Emailhost
  EMAIL_HOST_USER=username
  EMAIL_HOST_PASSWORD=password
  EMAIL_PORT=port

  ```

as you now sending email or some task may take too much time so it's time to set up celery

 ```plaintext

  # REDIS Connection
  
  REDIS_PORT=redisport
  REDIS_PASSWORD=redispassword
  FLOWER_PORT=flowerport

  ```

add the variable to you `.env` file. you also have access to flower to find out about jobs

make sure your dokcer compose is up with no error to enjoy celery

# Run Server <a name="run"></a>

for running server you don't need to run `python manage.py runserver` case we create a script that run migration and
runserver you just need dto make sure the docker compose is up

# Swagger for API Documentation <a name="swagger"></a>

We use Swagger for API documentation, providing a clear overview of our API endpoints and their functionalities.

**Accessing Swagger Documentation:**

Visit `host:port/swagger` or `host:port/redoc` to explore our API documentation and understand how to interact with our
endpoints.

# Authors <a name="authors"></a>

This project was developed by our dedicated team of developers, committed to delivering high-quality software solutions:

- [Amir Hossein Motaghian](https://github.com/johndoe)

For inquiries or collaboration opportunities, feel free to reach out to any of our team members via their respective
GitHub profiles.

# Skills <a name="skills"></a>

- **Backend Development:** Experienced in building robust backend systems using Python, Django
- **Database Management:** Skilled in database design, optimization, and management MySQL
- **API Development:** Expertise in designing and implementing RESTFUL documenting with Swagger, and testing with
  Postman.
- **Security:** Well-versed in web application security principles, including authentication, authorization, and
  protection against common vulnerabilities.
- **Agile Methodologies:** Practiced in Agile development methodologies such as Scrum and Kanban, fostering
  collaboration and delivering incremental value to stakeholders.
- **Continuous Learning:** Committed to staying up-to-date with the latest technologies and best practices through
  continuous learning and participation in community events.
- **Packages:** we give a thanks to the authors of these packages also:<br>
  1_django-debug-toolbar, 2_djangorestframework, 3_mysqlclient, 4_python-dotenv, 5_djoser <br>
  6_djangorestframework-simplejwt, 7_drf-nested-routers, 8_drf-yasg, 9_factory_boy,
  10_pillow, 11_django-cors-headers, 12_django-templated-mail, 13_redis, 14_celery, 15_flower

Our diverse skill set enables us to tackle complex challenges and deliver innovative solutions to meet our clients'
needs.

# License <a name="license"></a>

This project is licensed under the [MIT License](LICENSE), granting you the freedom to use, modify, and distribute the
code for both commercial and non-commercial purposes. See the [LICENSE](LICENSE) file for more details.
