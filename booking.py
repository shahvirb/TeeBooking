import click
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re


def wait_url_change(driver, timeout=600, match=None):
    logging.debug(f"Waiting for URL change. timeout={timeout}s, match={match}")
    old_url = driver.current_url
    WebDriverWait(driver, timeout).until(
        lambda driver: old_url != driver.current_url
        and driver.execute_script("return document.readyState == 'complete'")
    )
    logging.debug(driver.current_url)
    if match and not re.search(match, driver.current_url):
        wait_url_change(driver, timeout, match)


def fill_checkout_form(driver, firstname, lastname, phone):
    logging.info("Filling checkout form")
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
    wait_url_change(driver)
    logging.info("Confirmation sent to {email}")


@click.command()
@click.argument("firstname")
@click.argument("lastname")
@click.argument("phone")
@click.argument("email")
def main(firstname, lastname, phone, email):
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("root").setLevel(logging.DEBUG)

    with webdriver.Firefox() as driver:
        driver.get(
            "https://web2.vermontsystems.com/wbwsc/txaustinwt.wsc/search.html?display=detail&module=GR"
        )
        wait_url_change(driver, match=r"addtocart\.html")
        fill_checkout_form(driver, firstname, lastname, phone)
        # User must now click "One click to finish"

        wait_url_change(driver, match=r"confirmation\.html")
        fill_confirmation_form(driver, email)


if __name__ == "__main__":
    main()
