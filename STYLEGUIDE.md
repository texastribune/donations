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
- We use Prettier for formatting using the config specified in `package.json`. Please ensure you have [pre-commit](https://pre-commit.com/) installed on your machine as this is how we automate formatting fixes (you'll also need to do `pre-commit install` at the root of this directory). When you attempt to commit an invalid JS, JSON or Vue file, you'll get a failure message. Prettier will then automatically make the style updates but then rely on you to re-stage the changes. You could also install the Prettier extension for your editor so that formatting fixes happen on save.
- We use ESLint for linting, following the [Airbnb style guide](https://github.com/airbnb/javascript). This is integrated into our CircleCI builds, but we'd also recommend choosing an editor with an ESLint extension (VSCode, for example). That way, you can get inline messages about syntax ESLint doesn't like.
