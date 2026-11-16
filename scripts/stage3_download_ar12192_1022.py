# stage3_download_ar12192_1022.py - first real-data increment, Helioviewer route
# AR 12192 flare day 2014-10-22:
#   - six AIA channels at 12-min cadence, full day  (720 files)
#   - AIA 171 at 1-min, 11:00-18:00 UT             (420 files)
#   - HMI magnetograms at 720 s, full day          (~48 files)
# ~3 GB total; resumable (existing files skipped).
import sys, os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import helioviewer as hv

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "data", "solar", "raw", "ar12192_20141022"))

def times_between(t0, t1, step_s):
    t = [t0]
    while t[-1] < t1:
        nxt = t[-1] + timedelta(seconds=step_s)
        if nxt > t1:
            break
        t.append(nxt)
    return [x.strftime("%Y-%m-%dT%H:%M:%SZ") for x in t]

DAY0 = datetime(2014, 10, 22, 0, 0, 0)
DAY1 = datetime(2014, 10, 23, 0, 0, 0)
day12 = times_between(DAY0, DAY1, 720)
win1m = times_between(datetime(2014, 10, 22, 11, 0, 0), datetime(2014, 10, 22, 18, 0, 0), 60)
hmi720 = times_between(DAY0, DAY1, 720)

for chan, sid in [("aia_94", 8), ("aia_131", 9), ("aia_171", 10), ("aia_193", 11),
                  ("aia_211", 12), ("aia_335", 14)]:
    hv.download_series(day12, sid, os.path.join(OUT, "aia_12min_day", chan), chan)

hv.download_series(win1m, 10, os.path.join(OUT, "aia_1min_window", "171"), "aia_171")
hv.download_series(hmi720, 19, os.path.join(OUT, "hmi_720s_day"), "hmi_mag")

print("STAGE3 INCREMENT COMPLETE", flush=True)
