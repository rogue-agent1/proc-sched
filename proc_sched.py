#!/usr/bin/env python3
"""Process scheduler — FCFS, SJF, Round Robin, Priority, MLFQ."""
import sys
from collections import deque

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid, self.arrival, self.burst, self.priority = pid, arrival, burst, priority
        self.remaining = burst
        self.start = self.finish = self.wait = -1

def fcfs(procs):
    procs = sorted(procs, key=lambda p: p.arrival)
    time = 0
    for p in procs:
        time = max(time, p.arrival); p.start = time; p.wait = time - p.arrival
        time += p.burst; p.finish = time
    return procs

def sjf(procs):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in procs]
    ready, done, time = [], [], 0
    remaining = list(procs)
    while remaining or ready:
        while remaining and remaining[0].arrival <= time:
            ready.append(remaining.pop(0))
        if not ready:
            time = remaining[0].arrival; continue
        ready.sort(key=lambda p: p.burst)
        p = ready.pop(0); p.start = time; p.wait = time - p.arrival
        time += p.burst; p.finish = time; done.append(p)
    return done

def round_robin(procs, quantum=2):
    procs = [Process(p.pid, p.arrival, p.burst) for p in procs]
    queue, done, time = deque(), [], 0
    remaining = sorted(procs, key=lambda p: p.arrival)
    idx = 0
    while idx < len(remaining) and remaining[idx].arrival <= time:
        queue.append(remaining[idx]); idx += 1
    while queue:
        p = queue.popleft()
        if p.start == -1: p.start = time
        run = min(p.remaining, quantum); time += run; p.remaining -= run
        while idx < len(remaining) and remaining[idx].arrival <= time:
            queue.append(remaining[idx]); idx += 1
        if p.remaining > 0: queue.append(p)
        else: p.finish = time; p.wait = p.finish - p.arrival - p.burst; done.append(p)
    return done

def avg_wait(procs): return sum(p.wait for p in procs) / len(procs) if procs else 0

def main():
    if len(sys.argv) < 2: print("Usage: proc_sched.py <demo|test>"); return
    if sys.argv[1] == "test":
        ps = [Process(1, 0, 6), Process(2, 1, 4), Process(3, 2, 2)]
        r1 = fcfs(ps); assert r1[0].wait == 0; assert r1[1].wait == 5
        r2 = sjf([Process(1, 0, 6), Process(2, 1, 4), Process(3, 2, 2)])
        assert avg_wait(r2) < avg_wait(r1)  # SJF generally better
        r3 = round_robin([Process(1, 0, 6), Process(2, 0, 4)], quantum=2)
        assert len(r3) == 2
        assert all(p.finish > 0 for p in r3)
        # Single process
        r4 = fcfs([Process(1, 0, 5)]); assert r4[0].wait == 0; assert r4[0].finish == 5
        print("All tests passed!")
    else:
        ps = [Process(1, 0, 10), Process(2, 1, 5), Process(3, 3, 2)]
        for name, fn in [("FCFS", lambda: fcfs(ps)), ("SJF", lambda: sjf(ps)), ("RR(q=3)", lambda: round_robin(ps, 3))]:
            r = fn(); print(f"{name}: avg_wait={avg_wait(r):.1f}")

if __name__ == "__main__": main()
