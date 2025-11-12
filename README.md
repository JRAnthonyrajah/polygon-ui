# Polygon UI

A library/framework of UI components for Qt/PySide, similar to Mantine for webapps

---

## 📦 Project Overview

This project was generated using the [cookiecutter-poetry-project](https://github.com/JRAnthonyrajah/cookiecutter-poetry-project) template.

It uses:

- [Poetry](https://python-poetry.org/) for dependency management.
- [pyenv](https://github.com/pyenv/pyenv) and [task](https://taskfile.dev/) for environment setup and management.
- [pre-commit](https://pre-commit.com/) hooks for code quality.

---

## 🚀 Features

- 📦 Easy dependency management with Poetry
- ✅ Pre-commit hooks for consistent code formatting
- 🔄 Automatic versioning with [Commitizen](https://commitizen-tools.github.io/commitizen/)
- 🧪 Testing with Pytest

---

## 🛠️ Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/JRAnthonyrajah/polygon-ui
    cd polygon-ui
    ```


2. **Setup the environment using Taskfile:**
    ```bash
    task setup
    ```

---

## ⚙️ Usage

- **Run the application:**
    ```bash
    task run
    ```

- **Activate the Poetry shell:**
    ```bash
    task shell
    ```

- **Run tests:**
    ```bash
    poetry run pytest
    ```

- **Run pre-commit checks:**
    ```bash
    pre-commit run --all-files
    ```

---

## 🔄 Versioning

This project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) for automated semantic versioning:

- Make conventional commits:
    ```bash
    cz commit
    ```
- Bump the version:
    ```bash
    cz bump
    ```
- Push changes and tags:
    ```bash
    git push && git push --tags
    ```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Feel free to submit issues or pull requests!

---

## 📫 Contact

For questions or support, contact:
- **Author:** K3rm1t
- **Email:** janthonyrajah@gmail.com
