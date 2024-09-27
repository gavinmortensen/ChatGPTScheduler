# Justin Wu



import heapq

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


    # If wanting better runtime for sjf
    # def __lt__(self, other):
    #     # This is needed for the heap to compare processes based on their remaining time
    #     return self.remaining_time < other.remaining_time

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

def sjf_preemptive_scheduling(processes):
    time = 0
    completed = 0
    current_process = None
    ready_queue = []
    
    while completed != len(processes):
        # Add all arrived processes to the ready queue
        for process in processes:
            if process.arrival_time <= time and process.remaining_time > 0 and process not in ready_queue:
                ready_queue.append(process)
        
        # Select process with shortest remaining time
        if ready_queue:
            current_process = min(ready_queue, key=lambda x: x.remaining_time)
            if current_process.start_time is None:
                current_process.start_time = time
            
            time += 1
            current_process.remaining_time -= 1
            
            if current_process.remaining_time == 0:
                current_process.completion_time = time
                ready_queue.remove(current_process)
                completed += 1
        else:
            time += 1  # If no process is ready, increment the time
            
    return processes

    # If wanting better runtime for sjf
    # time = 0
    # completed = 0
    # ready_queue = []
    # process_index = 0
    # n = len(processes)

    # # Sort processes by arrival time first
    # processes.sort(key=lambda x: x.arrival_time)

    # while completed != n:
    #     # Push all processes that have arrived by the current time into the heap
    #     while process_index < n and processes[process_index].arrival_time <= time:
    #         heapq.heappush(ready_queue, processes[process_index])
    #         process_index += 1

    #     if ready_queue:
    #         # Get the process with the shortest remaining time
    #         current_process = heapq.heappop(ready_queue)

    #         if current_process.start_time is None:
    #             current_process.start_time = time

    #         # Execute the process for 1 time unit
    #         time += 1
    #         current_process.remaining_time -= 1

    #         if current_process.remaining_time == 0:
    #             current_process.completion_time = time
    #             completed += 1
    #         else:
    #             # If the process is not finished, push it back into the heap
    #             heapq.heappush(ready_queue, current_process)
    #     else:
    #         # If no process is ready to execute, advance time
    #         time += 1

    # return processes

def round_robin_scheduling(processes, q):
    