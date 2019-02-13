import pandas as pd
import uuid
import datetime
import random
from datetime import timedelta

start = 'Lead'
intermediate_stages = ['Discovery', 'Demo', 'Trial']
fail = 'Closed Lost'
success = 'Closed Won'

base_date = datetime.datetime.now() + timedelta(days=-365)

data = []
for i in range(0, 400):
    unique_id = uuid.uuid4().hex
    start_date = base_date + timedelta(days=random.randint(1, 30))
    data.append(dict(unique_id=unique_id, stage_name=start, sort=start_date))

    last_intermediate = False
    for stage in intermediate_stages:
        date = start_date + timedelta(days=random.randint(1, 30))
        if random.randint(1, 100) < 80:
            data.append(dict(unique_id=unique_id, stage_name=stage, sort=date))
            if stage == intermediate_stages[-1]:
                last_intermediate = True
        else:
            data.append(dict(unique_id=unique_id, stage_name=fail, sort=date))
            break

    if last_intermediate:
        date = start_date + timedelta(days=random.randint(1, 30))
        if random.randint(1, 100) < 80:
            data.append(dict(unique_id=unique_id, stage_name=success, sort=date))
        else:
            data.append(dict(unique_id=unique_id, stage_name=fail, sort=date))

df = pd.DataFrame(data)
periscope.materialize(df)