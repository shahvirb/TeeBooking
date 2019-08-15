import click
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re

logger = logging.getLogger(__name__)


def wait_url_change(driver, timeout=600, match=None):
    logger.debug(f"Waiting for URL change. timeout={timeout}s, match={match}")
    old_url = driver.current_url
    WebDriverWait(driver, timeout).until(
        lambda driver: old_url != driver.current_url
        and driver.execute_script("return document.readyState == 'complete'")
    )
    logger.debug(driver.current_url)
    if match and not re.search(match, driver.current_url):
        wait_url_change(driver, timeout, match)


def fill_checkout_form(driver, firstname, lastname, phone):
    logger.info("Filling checkout form")
    driver.find_element_by_xpath(
        '//*[@id="processingprompts_dailyfirstname"]'
    ).send_keys(firstname)
    driver.find_element_by_xpath(
        '//*[@id="processingprompts_dailylastname"]'
    ).send_keys(lastname)
    driver.find_element_by_xpath('//*[@id="processingprompts_dailyphone"]').send_keys(
        phone
    )


def fill_confirmation_form(driver, email):
    driver.find_element_by_xpath('//*[@id="webconfirmation_emailreceipt"]').send_keys(
        email
    )
    driver.find_element_by_xpath('//*[@id="webconfirmation_buttonsumbit"]').click()
    logger.info("Confirmation sent to {email}")


@click.command()
@click.argument("firstname")
@click.argument("lastname")
@click.argument("phone")
@click.argument("email")
def main(firstname, lastname, phone, email):
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    with webdriver.Firefox() as driver:
        driver.get(
            "https://web2.vermontsystems.com/wbwsc/txaustinwt.wsc/search.html?display=detail&module=GR"
        )
        wait_url_change(driver, match=r"addtocart\.html")
        fill_checkout_form(driver, firstname, lastname, phone)
        # User must now click "One click to finish"

        wait_url_change(driver, match=r"confirmation\.html")
        fill_confirmation_form(driver, email)

        driver.quit()


if __name__ == "__main__":
    main()
