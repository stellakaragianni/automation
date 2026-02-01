# Contact List App Automation

A comprehensive UI test automation framework for the [Contact List App](https://thinking-tester-contact-list.herokuapp.com) using Python, Selenium WebDriver, and pytest.

## 🛠 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Programming Language** | Python | 3.10+ |
| **Testing Framework** | pytest | 8.0+ |
| **UI Automation** | Selenium WebDriver | 4.0+ |
| **Browser Driver** | WebDriver Manager | 4.0+ |
| **Web Browser** | Google Chrome | Latest |

## 📦 Prerequisites

Before running the tests, ensure you have the following installed:

1. **Python 3.10 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **Google Chrome Browser**
   - Download from: https://www.google.com/chrome/
   - The latest version is recommended

3. **pip (Python package manager)**
   - Usually comes with Python installation
   - Verify: `pip --version`

## 🚀 Installation

### 1. Download project and run locally on your IDE OR

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/contact-list-test-automation.git
cd contact-list-test-automation
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- selenium
- pytest
- pytest-html
- webdriver-manager

## ▶️ Running Tests

### Run All Tests

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_ui_selenium.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_ui_selenium.py::TestContactListHappyPath -v
```

### Run Specific Test

```bash
pytest tests/test_ui_selenium.py::TestContactListHappyPath::test_create_account_and_verify_login -v
```

### Run with Detailed Output

```bash
pytest -v -s
```

- `-v` = verbose (shows test names)
- `-s` = show print statements


### Console Output
```bash
pytest -v
```

**Example Output:**
```
tests/test_ui_selenium.py::TestContactListHappyPath::test_create_account_and_verify_login PASSED
tests/test_ui_selenium.py::TestContactListHappyPath::test_add_contact_and_verify_display PASSED
tests/test_ui_selenium.py::TestContactListHappyPath::test_logout_login_contact_persists PASSED
tests/test_ui_selenium.py::TestContactListUnhappyPath::test_signup_with_invalid_email PASSED
tests/test_ui_selenium.py::TestContactListUnhappyPath::test_login_with_incorrect_credentials PASSED

==================== 5 passed in 45.23s ====================

<img width="975" height="177" alt="image" src="https://github.com/user-attachments/assets/fe6099a4-988e-4a93-99d8-7db59f821d49" />

