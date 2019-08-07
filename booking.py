import click
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re


def wait_url_change(driver, timeout=600, match=None):
    logging.debug(f'Waiting for URL change. timeout={timeout}s, match={match}')
    old_url = driver.current_url
    WebDriverWait(driver, timeout).until(
        lambda driver: old_url != driver.current_url
        and driver.execute_script("return document.readyState == 'complete'")
    )
    logging.debug(driver.current_url)
    if match and not re.search(match, driver.current_url):
        wait_url_change(driver, timeout, match)


def fill_checkout_form(driver, firstname, lastname, phone):
    logging.info('Filling checkout form')
    driver.find_element_by_xpath(
        '//*[@id="processingprompts_dailyfirstname"]'
    ).send_keys(firstname)
    driver.find_element_by_xpath(
        '//*[@id="processingprompts_dailylastname"]'
    ).send_keys(lastname)
    driver.find_element_by_xpath('//*[@id="processingprompts_dailyphone"]').send_keys(
        phone
    )


@click.command()
@click.argument("firstname")
@click.argument("lastname")
@click.argument("phone")
@click.argument("email")
def main(firstname, lastname, phone, email):
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("root").setLevel(logging.DEBUG)
    #logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)
    #logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

    with webdriver.Firefox() as driver:
        driver.get(
            "https://web2.vermontsystems.com/wbwsc/txaustinwt.wsc/search.html?display=detail&module=GR"
        )

        wait_url_change(driver, match=r'addtocart\.html')

        fill_checkout_form(driver, firstname, lastname, phone)

        wait_url_change(driver)
        # TODO
        # - wait for url change to one click page
        # - fill out email on next page
        # - submit form and close with success message in console



if __name__ == "__main__":
    main()
