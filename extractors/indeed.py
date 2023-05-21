from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")


def get_page_count(keyword):
    browser = webdriver.Chrome(options=options)
    base_url = "https://kr.indeed.com/jobs?q="
    final_url = f"{base_url}{keyword}"
    print(f"Requesting {final_url}")
    browser.get(final_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find('nav', attrs={"aria-label": "pagination"})

    if pagination == None:
        return 1

    pages = pagination.find_all('div', recursive=False)
    count = len(pages)

    if count == 0:
        return 1

    return count - 1


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print(f"Found {pages} pages in indeed")
    results = []

    for page in range(pages):
        SF = 'Failure'
        browser = webdriver.Chrome(options=options)
        base_url = "https://kr.indeed.com/jobs?q="
        final_url = f"{base_url}{keyword}&start={page * 10}"
        print(f"Requesting {final_url}")
        browser.get(final_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")

        if job_list != None:
            jobs = job_list.find_all('li', recursive=False)

            for job in jobs:
                zone = job.find("div", class_="mosaic-zone")

                if zone == None:
                    anchor = job.select_one('h2 a')
                    position = anchor['aria-label']
                    link = anchor['href']
                    company = job.find('span', class_='companyName')
                    location = job.find('div', class_='companyLocation')
                    job_data = {
                        'link': f"https://kr.indeed.com{link}",
                        'company': company.string.replace(',', ' '),
                        'location': location.string.replace(',', ' '),
                        'position': position.replace(',', ' ')
                    }
                    results.append(job_data)
                    SF = 'Success'

        print(f"Page {page + 1} is a {SF}.")

    return results
