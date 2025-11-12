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
- 🎨 Complete theme system (colors, spacing, typography)
- 🧩 Modular component architecture for Qt/PySide
- 🔧 PolyBook - Component development workshop
- 📱 Mantine-inspired design system for desktop applications

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

### Application Commands
- **Run the main application:**
    ```bash
    task run
    # or
    poetry run polygon-ui
    ```

- **Launch PolyBook (Component Workshop):**
    ```bash
    task polybook
    # or
    poetry run polybook
    ```

### Development Commands
- **Activate the Poetry shell:**
    ```bash
    task shell
    ```

- **Run tests:**
    ```bash
    task test
    # or
    poetry run pytest
    ```

- **Run tests in watch mode:**
    ```bash
    task test-watch
    ```

- **Run tests with coverage:**
    ```bash
    task coverage
    ```

- **Lint code:**
    ```bash
    task lint
    ```

- **Format code:**
    ```bash
    task format
    ```

- **Fix linting issues:**
    ```bash
    task fix
    ```

### PolyBook Features
PolyBook provides a powerful development environment for building and testing Polygon UI components:
- **Component Registry**: Discover and organize components
- **Live Preview**: Test components with different props in real-time
- **Story System**: Save and manage component states
- **Theme Switching**: Toggle between light/dark themes
- **Props Editor**: Dynamic component property manipulation
- **Code Generation**: Export component configurations as Python code

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
