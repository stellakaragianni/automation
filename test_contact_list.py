import pytest # Testing farmework
import time # For waiting & sleep
import random # For username creation
from selenium import webdriver # For controlling Chrome
from selenium.webdriver.common.by import By # for finding elements
from selenium.webdriver.support.ui import WebDriverWait # For Selenium to wait for web thingies to load
from selenium.webdriver.support import expected_conditions as EC # Instead fo writing complex wait-logic functions
from selenium.common.exceptions import TimeoutException # For handling time response errors


class ContactListPage:
    
    BASE_URL = "https://thinking-tester-contact-list.herokuapp.com"
    
    # Locators (tuples)
    SIGNUP_BUTTON = (By.ID, "signup")
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "submit")
    ADD_CONTACT_BUTTON = (By.ID, "add-contact")
    CONTACT_FIRST_NAME = (By.ID, "firstName")
    CONTACT_LAST_NAME = (By.ID, "lastName")
    LOGOUT_BUTTON = (By.ID, "logout")
    CONTACT_TABLE = (By.ID, "myTable")
    ERROR_MESSAGE = (By.ID, "error")
    
    # Constructor
    def __init__(self, driver):
        self.driver = driver # Save driver for easy access
        self.wait = WebDriverWait(driver, 10) # Driver wauit before usage
    
    # Open URL site
    def navigate_to_home(self):
        self.driver.get(self.BASE_URL)
    
    # Wait for the site to load until signup button is clickable
    def click_signup(self):
        self.wait.until(EC.element_to_be_clickable(self.SIGNUP_BUTTON)).click()
    
    # Method for Sign In - Wait until fields are visible & send values
    def fill_signup_form(self, first_name, last_name, email, password):
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME)).send_keys(first_name)
        self.wait.until(EC.visibility_of_element_located(self.LAST_NAME)).send_keys(last_name)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL)).send_keys(email)
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD)).send_keys(password)
    
    # Click Submit button
    def submit_form(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()
    
    # Checker if user is logged in
    def is_logged_in(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.ADD_CONTACT_BUTTON)) #wait for add contact button (aka user is logegd in); if it appears, return true - else throw exception
            return True
        except TimeoutException:
            return False
    
    # Add contact, update and view it
    def click_add_contact(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_CONTACT_BUTTON)).click()
    
    # wait till contact fields are shown; then fill with info
    def fill_contact_form(self, first_name, last_name):
        self.wait.until(EC.visibility_of_element_located(self.CONTACT_FIRST_NAME)).send_keys(first_name)
        self.wait.until(EC.visibility_of_element_located(self.CONTACT_LAST_NAME)).send_keys(last_name)
    
    # check if the contact exists on teh list
    def is_contact_displayed(self, first_name, last_name):
        try:
            contact_table = self.wait.until(EC.visibility_of_element_located(self.CONTACT_TABLE)) #laod the table;f the table appears within 10'', it's stored. else --> exception
            rows = contact_table.find_elements(By.TAG_NAME, "tr") # load the rows (aka tag <tr> on HTML) fromt he contact table
            # check each row if first & last name exist
            for row in rows:
                if first_name in row.text and last_name in row.text:
                    return True
            return False
        except TimeoutException:
            return False
    
    # Login + Logout methods
    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON)).click()
    
    def login(self, email, password):
        #self.nagivate_to_home()
        self.wait.until(EC.visibility_of_element_located(self.EMAIL)).send_keys(email)
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD)).send_keys(password)
        self.submit_form()
    
    # Handling method for error cases; returns the error msg (if one is shown)
    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text # gets the text content of element with ID = error
        except TimeoutException:
            return None

# Fixtures to set & clean up before & after the testing // change scope to class or session if you want each test to run in one tab
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome() # create a new chrome instance
    yield driver # pause driver here; come back after all tests are done
    driver.quit() # runs after the test, closes chrome window

@pytest.fixture(scope="function")
def page(driver):
    return ContactListPage(driver)



# Random username generation: char - nums
def generate_random_username(prefix="user"):
    random_numbers = random.randint(100000, 999999)
    return f"{prefix}-{random_numbers}"

################################################################################################


# HAPPY PATHS
class TestContactListHappyPath:

    # Create new account & try login
    def test_create_account_and_verify_login(self, page):

        # Create your account info
        username = generate_random_username() # call function & generate username
        email = f"{username}@test.com"
        password = "Test1234!"
        # Navigate through page & complete sign in process
        page.navigate_to_home()
        page.click_signup()
        time.sleep(2)
        page.fill_signup_form("Gio", "Kay", email, password)
        page.submit_form()
      
        assert page.is_logged_in(), "User should be logged in after successful signup"
    
    # Add & view new contact
    def test_add_contact_and_verify_display(self, page):

        username = generate_random_username()
        email = f"{username}@test.com"
        password = "Test1234!"
        contact_first_name = "Anna"
        contact_last_name = "Vissi"
        # Sign Up
        page.navigate_to_home()
        page.click_signup()
        time.sleep(2)
        page.fill_signup_form("Gio", "Kay", email, password)
        page.submit_form()
        # Add contact
        page.click_add_contact()
        time.sleep(2)
        page.fill_contact_form(contact_first_name, contact_last_name)
        page.submit_form()
        
        # Checks if Anna Vissi exists on contacts list
        assert page.is_contact_displayed(contact_first_name, contact_last_name), f"Contact {contact_first_name} {contact_last_name} should exist on the list"
    
    def test_logout_login_contact_persists(self, page):
        
        username = generate_random_username()
        email = f"{username}@test.com"
        password = "Test1234!"
        contact_first_name = "Alice"
        contact_last_name = "Cooper"
        # Create account and add contact
        page.navigate_to_home()
        page.click_signup()
        time.sleep(2)
        page.fill_signup_form("Gio", "Kay", email, password)
        page.submit_form()
        page.click_add_contact()
        time.sleep(2)
        page.fill_contact_form(contact_first_name, contact_last_name)
        page.submit_form()
        
        # Logout
        page.logout()
        
        page.navigate_to_home() # This line is GOD !
        time.sleep(2)
        
        # Login again 
        page.login(email, password)
        
        # Check that contact has been saved successfully into your list
        assert page.is_logged_in(), "User should be logged in"
        assert page.is_contact_displayed(contact_first_name, contact_last_name), f"Contact {contact_first_name} {contact_last_name} should persists after logout and login"


###########################################################################################

# UNHAPPY PATHS
class TestContactListUnhappyPath:
    
    # Login with invalid emial
    def test_signup_with_invalid_email(self, page):

        invalid_email = "notanemail"
        password = "Test1234!"
        page.navigate_to_home()
        page.click_signup()
        time.sleep(2)
        page.fill_signup_form("Gio", "Kay", invalid_email, password)
        page.submit_form()
        
        # Asserting if user has logegd in with wrong email
        assert not page.is_logged_in(), "User should not be logged in with wrong email"
        error_message = page.get_error_message()
        assert error_message is not None, "Error message!"
    
    # Login with incorrect pswd
    def test_login_with_incorrect_credentials(self, page):

        username = generate_random_username()
        email = f"{username}@test.com"
        password = "Test1234!"
        wrong_password = "WrongPassword123!"
        page.navigate_to_home()
        page.click_signup()
        time.sleep(2)
        page.fill_signup_form("Gio", "Kay", email, password)
        page.submit_form()
        time.sleep(2)
        
        # Logout and try to login with wrong password
        page.logout()
        time.sleep(2)
        page.login(email, wrong_password)
        
        # Asserting if user has logegd in with wrong password
        assert not page.is_logged_in(), "User should not be logged in with wrong password"
        error_message = page.get_error_message()
        assert error_message is not None, "Error message: incorrect credentials"
        
    # call main to run script locally // Arguments: __file__ = my testing script(dynamic), s = flag for printing statements & v = shwos details of test execution
    if __name__ == "__main__":
        pytest.main([__file__, "-v", "-s"])
