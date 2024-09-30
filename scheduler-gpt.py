# Justin Wu
# Gavin Mortensen


import sys  # For command-line arguments
import os  # To handle file name manipulations

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

def parse_input_file(file_path):
    processes = []
    quantum = None  # Initialize quantum to None

    with open(file_path, 'r') as file:
        lines = file.readlines()
        process_count = int(lines[0].split()[1])
        run_for = int(lines[1].split()[1])
        algorithm = lines[2].split()[1]
        
        # If the algorithm is round robin, we expect a quantum value
        if algorithm == "rr":
            quantum = int(lines[3].split()[1])
            for i in range(4, 4 + process_count):  # Adjusting to start after the quantum line
                parts = lines[i].split()
                process_id = parts[2]
                arrival_time = int(parts[4])
                burst_time = int(parts[6])
                processes.append(Process(process_id, arrival_time, burst_time))

        else:
            for i in range(3, 3 + process_count):  # No adjustments for the quantum line
                parts = lines[i].split()
                process_id = parts[2]
                arrival_time = int(parts[4])
                burst_time = int(parts[6])
                processes.append(Process(process_id, arrival_time, burst_time))

    return processes, run_for, algorithm, quantum

def calculate_metrics(processes):
    for process in processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time

    return processes

def fcfs_scheduling(processes, run_for):
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
    last_selected_process = None  # Keep track of the last selected process

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
            
            # Log the selection only if the current process is different from the last selected process
            if current_process != last_selected_process:
                log.append(f"Time {time} : {current_process.process_id} selected (burst {current_process.burst_time})")
                last_selected_process = current_process  # Update the last selected process
            
            # If this is the first time the process is being executed, set the start time.
            if current_process.start_time is None:
                current_process.start_time = time

            # Execute the process for one time unit
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
            # If no process is ready to run, the CPU is idle.
            log.append(f"Time {time} : Idle")
            time += 1  # If no process is ready, increment the time

    log.append(f"Finished at time {time}")
    return log, processes

def round_robin_scheduling(processes, run_for, quantum):
    # Sort the processes by their arrival time before starting the simulation
    processes.sort(key=lambda x: x.arrival_time)

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

def generate_output(log, processes, input_file):
    # Create the output file name by replacing .in with .out
    output_file = os.path.splitext(input_file)[0] + ".out"

    with open(output_file, 'w') as f:
        # Write the log entries
        for line in log:
            f.write(line + '\n')

        f.write('\n')  # Empty line before summary

        # Write process metrics
        for process in processes:
            f.write(f"{process.process_id} wait {process.waiting_time} "
                    f"turnaround {process.turnaround_time} "
                    f"response {process.start_time - process.arrival_time}\n")
    
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py inputFile.in")
        sys.exit(1)

    input_file = sys.argv[1]
    log = None

    processes, run_for, algorithm, quantum = parse_input_file(input_file)

    print(f"{len(processes)} processes")
    
    if algorithm == "sjf":
        print(f"Using preemptive Shortest Job First")
        log, processes = sjf_preemptive_scheduling(processes, run_for)
    elif algorithm == "fcfs":
        print(f"Using First-Come First-Serve")
        log, processes = fcfs_scheduling(processes, run_for)
    elif algorithm == "rr":
        if quantum is None:
            print("Error: Quantum not specified for Round Robin algorithm.")
            sys.exit(1)
        print(f"Using Round Robin with quantum {quantum}")
        log, processes = round_robin_scheduling(processes, run_for, quantum)

    # Means algorithm not found
    if log == None:
        print(f"Error: Algorithm not specified/valid.")
    else:
        generate_output(log, processes, input_file)