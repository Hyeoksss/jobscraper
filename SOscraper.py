import requests
from bs4 import BeautifulSoup

def get_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", class_="s-pagination").find_all("a", class_="s-pagination--item")
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)
 
def extract_job(html):
  title = html.find("h2", class_="mb4").find("a")["title"]
  company_row = html.find("h3", class_="mb4")
  company = company_row.find("span").get_text(strip=True)
  job_id = html["data-jobid"]
  return {'title':title, 'company':company, 'link':f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page, URL):
  jobs = []
  for page in range(last_page):
    print(f'Scrapping SO: Page: {page}')
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", class_="-job")
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs    

def get_jobs(word):
  URL = f"https://stackoverflow.com/jobs?q={word}"
  last_page = get_last_page(URL)
  jobs = extract_jobs(last_page, URL)
  return jobs