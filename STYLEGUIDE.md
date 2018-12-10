# Style Guide
## Python
- Code should generally follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with
  [Black](https://black.readthedocs.io/en/stable/) modifications
- Doc strings should generally follow [PEP
  257](https://www.python.org/dev/peps/pep-0257/) guidelines
- Flake8 (TODO)
- Pylint (TODO)
- `import` statements (TODO)

## JavaScript
- We use Prettier for formatting. It's done automatically as a pre-commit hook via [Husky](https://github.com/typicode/husky).
- We use ESLint for linting, following the [Airbnb style guide](https://github.com/airbnb/javascript). This is integrated into our CircleCI builds, but we'd also recommend choosing an editor with an ESLint extension (VSCode, for example). That way, you can get inline messages about syntax that's going to cause ESLint to complain.
