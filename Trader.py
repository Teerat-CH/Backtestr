import schedule
from datetime import datetime

def job():
    print("Hello World ", str(datetime.now()))

# schedule.every().hours.at(":05").do(job)
# schedule.every().hours.at(":10").do(job)
# schedule.every().hours.at(":15").do(job)

schedule.every().minutes.at(":00").do(job)

while True:
    schedule.run_pending()