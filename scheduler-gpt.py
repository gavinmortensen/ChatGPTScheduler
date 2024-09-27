# Justin Wu

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id    # Process ID
        self.arrival_time = arrival_time    # Arrival Time
        self.burst_time = burst_time    # Total Execution Time
        self.remaining_time = burst_time    # Remaining Execution Time for SJF
        self.start_time = None  # Start Time of the Process
        self.finish_time = None # Finish Time of the Process
        self.waiting_time = 0   # Waiting Time
        self.turnaround_time = 0    # Turnaround Time
        self.response_time = None   # Response Time

def calculate_metrics(processes):
    for process in processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time

    return processes

def fifo_scheduling(processes):
    time = 0
    for process in sorted(processes, key=lambda x: x.arrival_time):
        if time < process.arrival_time:
            time = process.arrival_time  # If the CPU is idle, skip to the arrival time
        process.start_time = time
        process.completion_time = time + process.burst_time
        time = process.completion_time

    return processes

def sjf_scheduling(processes):
    

def round_robin_scheduling(processes, q):
    