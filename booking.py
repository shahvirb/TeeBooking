import click
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def wait_url_change(driver, timeout=600):
    old_url = driver.current_url
    WebDriverWait(driver, timeout).until(lambda driver: old_url != driver.current_url
                                                    and driver.execute_script(
        "return document.readyState == 'complete'"))


@click.command()
@click.argument('firstname')
@click.argument('lastname')
@click.argument('phone')
@click.argument('email')
def main(firstname, lastname, phone, email):
    driver = webdriver.Firefox()
    driver.get("https://web2.vermontsystems.com/wbwsc/txaustinwt.wsc/search.html?display=detail&module=GR")

    wait_url_change(driver)
    print(driver.current_url)
    wait_url_change(driver)
    print(driver.current_url)

    driver.find_element_by_xpath('// *[ @ id = "processingprompts_dailyfirstname"]').send_keys(firstname)
    driver.find_element_by_xpath('// *[ @ id = "processingprompts_dailylastname"]').send_keys(lastname)
    driver.find_element_by_xpath('//*[@id="processingprompts_dailyphone"]').send_keys(phone)

    wait_url_change(driver)
    print(driver.current_url)

    # // *[ @ id = "webcheckout_billemail"]

    driver.close()

if __name__ == "__main__":
    main()