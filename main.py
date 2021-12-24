from flask import Flask, render_template, request, redirect, send_file
from SOscraper import get_jobs as so_get_jobs
from ROscraper import get_jobs as ro_get_jobs
from WRscraper import get_jobs as wr_get_jobs
from exporter import save_to_file

app = Flask("SuperPython")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = so_get_jobs(word) + ro_get_jobs(word) + wr_get_jobs(word)
      db[word] = jobs  
  else:
    return redirect("/")  
  return render_template(
     "report.html", 
     searchingBy=word,
     resultsNumber=len(jobs),
     jobs=jobs
    )

@app.route("/export")
def export():
  try:  
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs, word)
    return send_file(f"{word}.csv")  
  except:
    return redirect("/")     


app.run(host="0.0.0.0")