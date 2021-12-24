import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36'}

def extract_job(low):
  title = low.find("td", class_="company").find("a", class_="preventLink").find("h2").get_text(strip=True)
  company = low.find("td", class_="company").find("span", class_="companyLink").find("h3").get_text(strip=True)
  job_id = low.find("td", class_="image").find("a", class_="preventLink")
  if job_id == None:
    link = "https://remoteok.com"
  else:
    job_id = job_id["href"]
    link = f"https://remoteok.com{job_id}"
  return {"title":title, "company":company, "link":link}

def extract_jobs(url):
  jobs = []
  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, "html.parser")
  jb = soup.find("table", id="jobsboard")
  lows = jb.find_all("tr", class_="job")
  for low in lows:
    job = extract_job(low)
    jobs.append(job)
  return jobs    

def get_jobs(word):
  url = f"https://remoteok.com/remote-{word}-jobs"
  jobs = extract_jobs(url)
  return jobs