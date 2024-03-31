# :fire: Django E-Commerce Hub :fire:
## Empowering Your Online Shopping Experience :bento: :bento:

Welcome to the Django E-Commerce Hub, where we redefine your online shopping journey! Our platform offers a seamless and secure environment for buyers and sellers alike. Explore a wide range of products, manage your shopping cart effortlessly, and enjoy a smooth checkout process. Join us as we revolutionize the way you shop online!


## Acknowledgements

- [Virtual Environments](#virtual_env)
- [Env file](#env_file)
- [DB](#db)


# Virtual Environments  <a name="virtual_env"></a>  

I prefer to use Pipenv which is a tool that simplifies Python dependency management by automatically creating and managing virtual environments for your projects. It combines the functionality of pip and virtualenv into a single package, making it easier to manage dependencies and ensure project consistency.


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

Environment variables are a way to store configuration settings or sensitive information that your application needs to function properly. They are typically stored in a file named `.env` in the root directory of your project. Here's a summary of how to use and manage environment variables in your project:

- **Creating an Environment File**

Create a file named `.env` in the root directory of your project. This file will store your environment variables.

- **Adding Variables**

Add your environment variables to the `.env` file using the `KEY=VALUE` format. For example:
  
  ```plaintext
  CONNECTION=mysql,postgresql,...
  NAME=db_name
  ROOT=user_name_of_db
  PASSWORD=your_password
  HOST=your_host
  PORT=app_port
  PMA_PORT=db_port
  ```

# DB  <a name="db"></a>

fortunately We utilize Docker to manage our database environment. Docker enables containerization, simplifying deployment across different environments.

We leverage Docker Compose to define and run multi-container Docker applications. Docker Compose reads environment variables from a `.env` file, allowing flexible configuration. feel free to update the docker compose file as you need


To start the database and related services, execute:
```bash
docker compose up 
```

# Run Server <a name="run"></a>

now you can run the app and send api :rocket: <br>
while you are in pipenv shell run

```bash
python manage.py runserver
```