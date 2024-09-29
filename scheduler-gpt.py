# Justin Wu
# Gavin Mortensen


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

def parse_input_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        process_count = int(lines[0].split()[1])
        run_for = int(lines[1].split()[1])
        algorithm = lines[2].split()[1]
        
        for i in range(3, 3 + process_count):
            parts = lines[i].split()
            process_id = parts[2]
            arrival_time = int(parts[4])
            burst_time = int(parts[6])
            processes.append(Process(process_id, arrival_time, burst_time))

    return processes, run_for, algorithm

def calculate_metrics(processes):
    for process in processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time

    return processes

def fifo_scheduling(processes, run_for):
    time = 0
    log = []
    processes_sorted = sorted(processes, key=lambda x: x.arrival_time)
    
    for process in processes_sorted:
        if time < process.arrival_time:
            while time < process.arrival_time:
                log.append(f"Time {time} : Idle")
                time += 1
                
        log.append(f"Time {time} : {process.process_id} arrived")
        process.start_time = time
        log.append(f"Time {time} : {process.process_id} selected (burst {process.burst_time})")
        time += process.burst_time
        process.completion_time = time
        process.turnaround_time = time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        log.append(f"Time {time} : {process.process_id} finished")
    
    while time < run_for:
        log.append(f"Time {time} : Idle")
        time += 1

    log.append(f"Finished at time {time}")
    return log, processes

def sjf_preemptive_scheduling(processes, run_for):
    time = 0
    completed = 0
    ready_queue = []
    log = []

    while completed != len(processes) or time < run_for:
        # Check process arrivals
        for process in processes:
            if process.arrival_time == time:
                log.append(f"Time {time} : {process.process_id} arrived")

        # Add all arrived processes to the ready queue
        for process in processes:
            if process.arrival_time <= time and process.remaining_time > 0 and process not in ready_queue:
                ready_queue.append(process)

        # Select the process with the shortest remaining time
        if ready_queue:
            current_process = min(ready_queue, key=lambda x: x.remaining_time)
            
            if current_process.start_time is None:
                current_process.start_time = time
                log.append(f"Time {time} : {current_process.process_id} selected (burst {current_process.burst_time})")
            
            # Execute the process
            time += 1
            current_process.remaining_time -= 1

            # Check if the process finishes
            if current_process.remaining_time == 0:
                current_process.completion_time = time
                current_process.turnaround_time = time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                log.append(f"Time {time} : {current_process.process_id} finished")
                ready_queue.remove(current_process)
                completed += 1
        else:
            log.append(f"Time {time} : Idle")
            time += 1  # If no process is ready, increment the time

    log.append(f"Finished at time {time}")
    return log, processes

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

def round_robin_scheduling(processes, run_for, quantum):
    time = 0
    ready_queue = []
    log = []
    index = 0
    while index < len(processes) or ready_queue:
        # Add arrived processes to ready_queue
        while index < len(processes) and processes[index].arrival_time <= time:
            log.append(f"Time {time} : {processes[index].process_id} arrived")
            ready_queue.append(processes[index])
            index += 1
        
        if ready_queue:
            current_process = ready_queue.pop(0)
            
            if current_process.start_time is None:
                current_process.start_time = time
                log.append(f"Time {time} : {current_process.process_id} selected (burst {current_process.burst_time})")
            
            execute_time = min(quantum, current_process.remaining_time)
            time += execute_time
            current_process.remaining_time -= execute_time
            
            if current_process.remaining_time == 0:
                current_process.completion_time = time
                current_process.turnaround_time = time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                log.append(f"Time {time} : {current_process.process_id} finished")
            else:
                # If the process isn't finished, put it back into the queue
                ready_queue.append(current_process)
        
        else:
            log.append(f"Time {time} : Idle")
            time += 1  # CPU is idle, increment time

    log.append(f"Finished at time {time}")
    return log, processes

def generate_output(log, processes):
    for line in log:
        print(line)

    print()  # Empty line before summary
    for process in processes:
        print(f"{process.process_id} wait {process.waiting_time} turnaround {process.turnaround_time} response {process.start_time - process.arrival_time}")

if __name__ == "__main__":
    processes, run_for, algorithm = parse_input_file("input.txt")

    print(f"{len(processes)} processes")
    
    if algorithm == "sjf":
        print(f"Using preemptive Shortest Job First")
        log, processes = sjf_preemptive_scheduling(processes, run_for)
    elif algorithm == "fifo":
        print(f"Using First-Come First-Serve")
        log, processes = fifo_scheduling(processes, run_for)
    elif algorithm == "rr":
        quantum = int(input("Enter quantum: "))  # Example of how to pass quantum
        print(f"Using Round Robin with quantum {quantum}")
        log, processes = round_robin_scheduling(processes, run_for, quantum)
    
    generate_output(log, processes)