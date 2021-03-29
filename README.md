### Hexlet tests and linter status:
[![Actions Status](https://github.com/Deepsick/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/Deepsick/python-project-lvl4/actions)
[![Github Actions Status](https://github.com/Deepsick/python-project-lvl4/workflows/Python%20CI/badge.svg)](https://github.com/Deepsick/python-project-lvl4/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/7d325cf968b20604acea/maintainability)](https://codeclimate.com/github/Deepsick/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7d325cf968b20604acea/test_coverage)](https://codeclimate.com/github/Deepsick/python-project-lvl4/test_coverage)

# Task manager

Simple todo app with:
- Users
- Labels
- Statuses
- Tasks


## Installation

Python packaging and dependency management tool ```Poetry``` should be preinstalled.

1. Fill in ```.env``` according to ```.env-example```
2. Install dependencies
```bash
make install
```
3. Migrate all tables
```bash
make migrate
``` 

## Usage

1. Run local server
```bash
make server
```


## Testing

```bash
make install
make lint
make test
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Deploy link
https://hexlet-django-task-manager.herokuapp.com/

