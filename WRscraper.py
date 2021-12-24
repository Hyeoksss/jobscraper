import requests
from bs4 import BeautifulSoup

word = "python"
url = f"https://weworkremotely.com/remote-jobs/search?term={word}"

def extract_job(low):
  title = low.find("span", class_="title").get_text()
  company = low.find("span", class_="company").get_text()
  job_a = low.contents[-1]
  job_id = job_a["href"]
  link = f"https://weworkremotely.com{job_id}"
  return {"title":title, "company":company, "link":link}

def extract_jobs(url):
  jobs = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  sections = soup.find_all("section", class_="jobs")
  for section in sections:
    lows = section.find("ul").find_all("li", {"class":["", "feature"]})
    for low in lows:
      job = extract_job(low)
      jobs.append(job)
  return jobs

def get_jobs(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = extract_jobs(url)
  return jobs    