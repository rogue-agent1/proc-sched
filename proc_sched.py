#!/usr/bin/env python3
"""proc_sched: Process scheduling algorithms (FCFS, SJF, RR, Priority)."""
import sys
from collections import deque

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid; self.arrival = arrival; self.burst = burst
        self.priority = priority; self.remaining = burst
        self.start = -1; self.finish = -1; self.wait = 0

def fcfs(processes):
    procs = sorted(processes, key=lambda p: p.arrival)
    time = 0
    for p in procs:
        time = max(time, p.arrival)
        p.start = time; p.wait = time - p.arrival
        time += p.burst; p.finish = time
    return procs

def sjf(processes):
    procs = [Process(p.pid, p.arrival, p.burst) for p in processes]
    done = []
    time = 0
    remaining = list(procs)
    while remaining:
        available = [p for p in remaining if p.arrival <= time]
        if not available:
            time = min(p.arrival for p in remaining); continue
        shortest = min(available, key=lambda p: p.burst)
        shortest.start = time
        shortest.wait = time - shortest.arrival
        time += shortest.burst
        shortest.finish = time
        done.append(shortest)
        remaining.remove(shortest)
    return done

def round_robin(processes, quantum):
    procs = [Process(p.pid, p.arrival, p.burst) for p in processes]
    queue = deque()
    time = 0
    remaining = sorted(procs, key=lambda p: p.arrival)
    idx = 0
    done = []
    while queue or idx < len(remaining):
        while idx < len(remaining) and remaining[idx].arrival <= time:
            queue.append(remaining[idx]); idx += 1
        if not queue:
            time = remaining[idx].arrival; continue
        p = queue.popleft()
        if p.start == -1: p.start = time
        run = min(quantum, p.remaining)
        time += run; p.remaining -= run
        while idx < len(remaining) and remaining[idx].arrival <= time:
            queue.append(remaining[idx]); idx += 1
        if p.remaining > 0:
            queue.append(p)
        else:
            p.finish = time
            p.wait = p.finish - p.arrival - p.burst
            done.append(p)
    return done

def avg_wait(procs):
    return sum(p.wait for p in procs) / len(procs) if procs else 0

def avg_turnaround(procs):
    return sum(p.finish - p.arrival for p in procs) / len(procs) if procs else 0

def test():
    procs = [Process(1,0,6), Process(2,1,8), Process(3,2,7), Process(4,3,3)]
    # FCFS
    r1 = fcfs([Process(p.pid,p.arrival,p.burst) for p in procs])
    assert r1[0].finish == 6
    assert avg_wait(r1) >= 0
    # SJF
    r2 = sjf(procs)
    assert avg_wait(r2) <= avg_wait(r1) + 0.01  # SJF optimal for non-preemptive
    # Round Robin
    r3 = round_robin(procs, 4)
    assert len(r3) == 4
    assert all(p.finish > 0 for p in r3)
    # Simple case
    simple = [Process(1,0,3), Process(2,0,3)]
    r4 = fcfs(simple)
    assert r4[0].wait == 0 and r4[1].wait == 3
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: proc_sched.py test")
