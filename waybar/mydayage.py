from datetime import datetime, timezone

# YOUR BIRTHDAY
# d1 = datetime(1990,1,1,0,0,0,0,timezone.utc)
#

d2 = datetime.now(timezone.utc)
d  = abs((d2 - d1))
days  = d.days
hours = d.seconds // 3600
minutes = (d.seconds - hours * 3600) // 60
print(f"{days:,.0f}::{hours}:{minutes}")
