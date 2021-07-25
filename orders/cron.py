from datetime      import datetime, timedelta

from orders.models import Bidding

def update_bidding_status(now=datetime.now()):
    biddings = Bidding.objects.filter(status_id=1)
    
    for bidding in biddings:
        date_expired = bidding.created_at + timedelta(days=bidding.expired_within.period)

        if (date_expired.year, date_expired.month, date_expired.day) == (now.year, now.month, now.day):
            bidding.status_id = 2
            bidding.save()

    print(now)