#!/usr/bin/env python3
"""proc_sched - Process scheduler simulator (FCFS, SJF, RR, Priority)."""
import sys
from collections import deque

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.priority = priority
        self.start_time = None
        self.finish_time = None
        self.wait_time = 0

def fcfs(processes):
    procs = sorted(processes, key=lambda p: (p.arrival, p.pid))
    time = 0
    order = []
    for p in procs:
        if time < p.arrival:
            time = p.arrival
        p.start_time = time
        p.wait_time = time - p.arrival
        time += p.burst
        p.finish_time = time
        order.append(p.pid)
    return order

def sjf(processes):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    time = 0
    ready = []
    remaining = list(procs)
    order = []
    while remaining or ready:
        for p in list(remaining):
            if p.arrival <= time:
                ready.append(p)
                remaining.remove(p)
        if not ready:
            time = remaining[0].arrival
            continue
        ready.sort(key=lambda p: (p.burst, p.pid))
        p = ready.pop(0)
        p.start_time = time
        p.wait_time = time - p.arrival
        time += p.burst
        p.finish_time = time
        order.append(p.pid)
    return order

def round_robin(processes, quantum=2):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    procs.sort(key=lambda p: (p.arrival, p.pid))
    time = 0
    queue = deque()
    remaining = list(procs)
    order = []
    arrived = set()
    while remaining or queue:
        for p in list(remaining):
            if p.arrival <= time and p.pid not in arrived:
                queue.append(p)
                arrived.add(p.pid)
                remaining.remove(p)
        if not queue:
            time = remaining[0].arrival
            continue
        p = queue.popleft()
        if p.start_time is None:
            p.start_time = time
        run = min(quantum, p.remaining)
        time += run
        p.remaining -= run
        for r in list(remaining):
            if r.arrival <= time and r.pid not in arrived:
                queue.append(r)
                arrived.add(r.pid)
                remaining.remove(r)
        if p.remaining > 0:
            queue.append(p)
        else:
            p.finish_time = time
            p.wait_time = p.finish_time - p.arrival - p.burst
            order.append(p.pid)
    return order

def test():
    procs = [Process(1, 0, 4), Process(2, 1, 3), Process(3, 2, 1)]
    assert fcfs(procs) == [1, 2, 3]
    procs = [Process(1, 0, 4), Process(2, 1, 3), Process(3, 2, 1)]
    assert sjf(procs) == [1, 3, 2]
    procs = [Process(1, 0, 4), Process(2, 0, 3)]
    order = round_robin(procs, quantum=2)
    assert order == [1, 2]
    procs = [Process(1, 0, 1)]
    assert fcfs(procs) == [1]
    assert sjf(procs) == [1]
    assert round_robin(procs, 2) == [1]
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("proc_sched: Process scheduler. Use --test")
