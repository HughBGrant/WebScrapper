from requests import get
from bs4 import BeautifulSoup


def extract_rok_jobs(keyword):
  url = f"https://remoteok.com/remote-{keyword}-jobs"
  print(f"Requesting {url}")
  response = get(url, headers={"User-Agent": "Kimchi"})
  results = []

  if response.status_code != 200:
    print("Can't request website")
    return results

  soup = BeautifulSoup(response.text, "html.parser")
  jobs = soup.find_all('tr', class_='job')

  for job in jobs:
    link = job['data-href']
    position = job.find("h2", itemprop="title")
    company = job.find("h3", itemprop="name")
    locations = job.find_all('div', class_="location")[:-1]
    location = ' / '.join([
      location.string for location in locations if '💰' not in location.string
    ])
    job_data = {
      'link': f"https://remoteok.com/{link}",
      'company': company.string.strip().replace(',', ' '),
      'location': location.replace(',', ' '),
      'position': position.string.strip().replace(',', ' ')
    }
    results.append(job_data)

  print(f"got {len(results)} jobs")

  return results
