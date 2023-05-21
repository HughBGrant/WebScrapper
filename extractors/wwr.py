from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
    final_url = f"{base_url}{keyword}"
    print(f"Requesting {final_url}")
    response = get(final_url)
    results = []

    if response.status_code != 200:
        print("Can't request website")
        return results

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all('section', class_="jobs")

    for job_section in jobs:
        job_posts = job_section.find_all('li')[:-1]

        for post in job_posts:
            anchor = post.find('a', recursive=False)
            link = anchor['href']
            company, _, location = anchor.find_all('span', class_="company")
            position = anchor.find('span', class_='title')
            job_data = {
                'link': f"https://weworkremotely.com{link}",
                'company': company.string.replace(',', ' '),
                'location': location.string.replace(',', ' '),
                'position': position.string.replace(',', ' ')
            }
            results.append(job_data)

    print(f"got {len(results)} jobs")

    return results
