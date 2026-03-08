import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the website
base_url = "https://realpython.github.io/fake-jobs/"

jobs = []

# Pagination loop (simulate multiple pages)
for page in range(1, 4):

    print(f"Scraping page {page}...")

    try:
        response = requests.get(base_url)

        if response.status_code != 200:
            print("Failed to retrieve page")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("div", class_="card-content")

        for job in job_cards:

            try:
                title = job.find("h2", class_="title").text.strip()
            except:
                title = "N/A"

            try:
                company = job.find("h3", class_="company").text.strip()
            except:
                company = "N/A"

            try:
                location = job.find("p", class_="location").text.strip()
            except:
                location = "N/A"

            try:
                link = job.find("a")["href"]
            except:
                link = "N/A"

            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Apply Link": link,
                "Page": page
            })

    except Exception as e:
        print("Error:", e)

# Convert to dataframe
df = pd.DataFrame(jobs)

# Remove duplicates
df = df.drop_duplicates()

# Save data
df.to_csv("jobs.csv", index=False)
df.to_json("jobs.json", orient="records", indent=4)

print("Scraping completed!")
print(f"Total jobs collected: {len(df)}")
