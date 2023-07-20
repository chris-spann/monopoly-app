# Monopoly CLI App with FastAPI and PostgreSQL


This is a Monopoly app that allows you to play the classic board game on your computer. It is built with FastAPI and managed with Poetry, and can be run in a Docker-Compose container with a Postgres database. Alembic is used for database migrations and Pydantic is used for data validation.

## Installation

To install the Monopoly app, follow these steps:

1. Clone the repository to your local machine.
2. Install Docker and Docker Compose on your machine if you haven't already.
3. Build the Docker images by running `docker-compose build` in the root directory of the project.
4. Run the Docker Compose container by running `docker-compose up`.

## Usage

To use the Monopoly app, follow these steps:

1. Start the app by running the Docker Compose container with `docker-compose up`.
2. Open your web browser and navigate to `http://localhost:8000/docs`.
3. Use the Swagger UI to interact with the API and play the game.

## Features

The Monopoly app includes the following features:

- Multiplayer support for up to 8 players.
- Postgres database for persistent storage.
- Alembic for database migrations.
- Pydantic for data validation.
- Pre-commit hooks

## Contributing

If you would like to contribute to the Monopoly app, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

## License

The Monopoly app is licensed under the MIT License. See `LICENSE` for more information.