# Justin Wu

class Process:
    def __init__(self, pid, arrival_time, execution_time):
        self.process_id = process_id                # Process ID
        self.arrival_time = arrival_time  # Arrival Time
        self.burst_time = burst_time  # Total Execution Time
        self.remaining_time = burst_time  # Remaining Execution Time for SJF
        self.start_time = None        # Start Time of the Process
        self.finish_time = None       # Finish Time of the Process
        self.waiting_time = 0         # Waiting Time
        self.turnaround_time = 0      # Turnaround Time
        self.response_time = None      # Response Time

def fifo_scheduling(processes):

def sjf_scheduling(processes):

def round_robin_scheduling(processes, q):
