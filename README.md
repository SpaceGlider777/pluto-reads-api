# Pluto Reads API

API consumed by the Pluto Reads Angular app to provide book recommendations.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install requirements.txt
```
Use `flask run` to start the application.

## Get most purchased books

`GET /popular/`

## Get highest rated books

`GET /highest-rated/`

## Get book by ISBN

`GET /book/<isbn>/`

## Get recommendations by ISBN

`GET /recommendations/<isbn>/`

## Search for books

`GET /search/<str>/`

## License

[MIT](https://choosealicense.com/licenses/mit/)
