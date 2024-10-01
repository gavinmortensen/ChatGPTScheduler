# Justin Wu
# Gavin Mortensen
# Ashlyn Zimmer

import sys  # For command-line arguments
import os  # To handle file name manipulations

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id          # Process ID
        self.arrival_time = arrival_time      # Arrival Time
        self.burst_time = burst_time          # Total Execution Time
        self.remaining_time = burst_time      # Remaining Execution Time for SJF
        self.start_time = None                # Start Time of the Process
        self.finish_time = None               # Finish Time of the Process
        self.waiting_time = 0                 # Waiting Time
        self.turnaround_time = 0              # Turnaround Time
        self.response_time = None              # Response Time
        self.arrived = False                   # To track whether the arrival has already been logged
        self.finished = False                  # To track if the process has finished

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

def fcfs_scheduling(processes, run_for):
    current_time = 0
    process_queue = sorted(processes, key=lambda x: x.arrival_time)  # Sort by arrival time
    log = []

    completed_processes = []  # Track completed processes

    # Initialize remaining time for each process
    for process in process_queue:
        process.remaining_time = process.burst_time  # Initialize remaining time
        process.finished = False  # Initialize finished status

    while current_time < run_for:
        # Log process arrivals at the current time
        for process in process_queue:
            if process.arrival_time == current_time and not process.arrived:
                log.append(f"Time {current_time:>3} : {process.process_id} arrived")
                process.arrived = True  # Mark this process as arrived to prevent duplicate logging
        
        # Find the next process that has arrived and is ready to run
        arrived_processes = [process for process in process_queue if process.arrival_time <= current_time and process not in completed_processes]
        
        if arrived_processes:
            # Select the first process (FCFS)
            current_process = arrived_processes[0]
            if current_process.start_time is None:  # Set response time if not set
                current_process.start_time = current_time
            
            log.append(f"Time {current_time:>3} : {current_process.process_id} selected (burst {current_process.remaining_time:>3})")
            
            # Simulate process execution
            while current_process.remaining_time > 0 and current_time < run_for:
                current_process.remaining_time -= 1
                current_time += 1
                
                # Log any new arrivals during the execution of this process
                for process in process_queue:
                    if process.arrival_time == current_time and not process.arrived:
                        log.append(f"Time {current_time:>3} : {process.process_id} arrived")
                        process.arrived = True
            
            # Check if the process has finished execution
            if current_process.remaining_time == 0:
                completed_processes.append(current_process)
                current_process.completion_time = current_time
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time  # Calculate waiting time based on original burst time
                current_process.finished = True  # Mark process as finished
                log.append(f"Time {current_time:>3} : {current_process.process_id} finished")
            else:
                # Do not log anything about unfinished processes
                current_process.finished = False  # Mark process as unfinished
            
        else:
            log.append(f"Time {current_time:>3} : Idle")
            current_time += 1
    
    log.append(f"Finished at time {current_time:>3}")
    
    return log, processes

def sjf_preemptive_scheduling(processes, run_for):
    time = 0
    completed = 0
    ready_queue = []
    log = []
    last_selected_process = None  # Keep track of the last selected process

    while time < run_for:
        # Check process arrivals
        for process in processes:
            if process.arrival_time == time and not process.arrived:
                log.append(f"Time {time:>3} : {process.process_id} arrived")
                process.arrived = True  # Mark as arrived to prevent duplicate logging

        # Add all arrived processes to the ready queue
        for process in processes:
            if process.arrival_time <= time and process.remaining_time > 0 and process not in ready_queue:
                ready_queue.append(process)

        # Select the process with the shortest remaining time
        if ready_queue:
            current_process = min(ready_queue, key=lambda x: x.remaining_time)
            
            # Log the selection only if the current process is different from the last selected process
            if current_process != last_selected_process:
                log.append(f"Time {time:>3} : {current_process.process_id} selected (burst {current_process.remaining_time:>3})")
                last_selected_process = current_process  # Update the last selected process
            
            # If this is the first time the process is being executed, set the start time.
            if current_process.start_time is None:
                current_process.start_time = time

            # Execute the process for one time unit
            time += 1
            current_process.remaining_time -= 1

            # Check if any other processes arrive at the new time before logging the process completion
            for process in processes:
                if process.arrival_time == time and not process.arrived:
                    log.append(f"Time {time:>3} : {process.process_id} arrived")
                    process.arrived = True  # Mark as arrived to prevent duplicate logging

            # Check if the process finishes
            if current_process.remaining_time == 0:
                current_process.completion_time = time
                current_process.turnaround_time = time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                current_process.finished = True  # Mark process as finished
                log.append(f"Time {time:>3} : {current_process.process_id} finished")
                ready_queue.remove(current_process)
                completed += 1
        else:
            # If no process is ready to run, the CPU is idle.
            log.append(f"Time {time:>3} : Idle")
            time += 1  # If no process is ready, increment the time

    log.append(f"Finished at time {time:>3}")
    return log, processes

def round_robin_scheduling(processes, run_for, quantum):
    # Sort the processes by arrival time before starting the simulation
    processes.sort(key=lambda x: x.arrival_time)

    time = 0
    ready_queue = []
    log = []
    index = 0  # Track the next process to arrive

    while time < run_for:
        # Check for new arrivals and add them to the ready queue
        while index < len(processes) and processes[index].arrival_time <= time:
            log.append(f"Time {time:>3} : {processes[index].process_id} arrived")
            ready_queue.append(processes[index])
            index += 1
        
        if ready_queue:
            current_process = ready_queue.pop(0)  # Get the next process in the queue
            if current_process.start_time is None:  # Set response time if not set
                current_process.start_time = time
            
            # Log the process selection
            log.append(f"Time {time:>3} : {current_process.process_id} selected (burst {current_process.remaining_time:>3})")
            
            # Determine how long to execute this process
            execute_time = min(quantum, current_process.remaining_time)
            
            for _ in range(execute_time):
                if time < run_for:  # Only execute if within the run_for time
                    time += 1
                    current_process.remaining_time -= 1
                    
                    # Log any new arrivals during the execution of this process
                    while index < len(processes) and processes[index].arrival_time <= time:
                        log.append(f"Time {time:>3} : {processes[index].process_id} arrived")
                        ready_queue.append(processes[index])
                        index += 1
                    
                    # Check if the process has finished
                    if current_process.remaining_time == 0:
                        current_process.completion_time = time
                        current_process.turnaround_time = time - current_process.arrival_time
                        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                        log.append(f"Time {time:>3} : {current_process.process_id} finished")
                        break
            else:
                # If the process didn't finish, add it back to the queue
                ready_queue.append(current_process)
        else:
            # If no process is ready to run, the CPU is idle
            log.append(f"Time {time:>3} : Idle")
            time += 1  # Increment time

    log.append(f"Finished at time {time:>3}")

    # Mark all processes as finished in case they have completed
    for process in processes:
        process.finished = process.remaining_time == 0  # Set finished status

    return log, processes

def generate_output(log, processes, input_file):
    # Create the output file name by replacing .in with .out
    output_file = os.path.splitext(input_file)[0] + ".out"

    with open(output_file, 'w') as f:
        # Write the log entries
        for line in log:
            f.write(line + '\n')

        f.write('\n')  # Empty line before summary

        # Sort processes by process_id before writing to the output
        processes.sort(key=lambda x: x.process_id)

        # Write process metrics
        for process in processes:
            if process.finished:
                f.write(f"{process.process_id} wait {process.waiting_time:>3} "
                        f"turnaround {process.turnaround_time:>3} "
                        f"response {process.start_time - process.arrival_time:>3}\n")
            else:
                f.write(f"{process.process_id} did not finish\n")
    
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py inputFile.in")
        sys.exit(1)

    input_file = sys.argv[1]
    log = []

    # Parse the input file
    processes, run_for, algorithm, quantum = parse_input_file(input_file)

    # Log the number of processes at the start
    log.append(f"{len(processes):>3} processes")

    # Determine which scheduling algorithm to use and log it
    if algorithm == "sjf":
        log.append("Using preemptive Shortest Job First")
        scheduling_log, processes = sjf_preemptive_scheduling(processes, run_for)
        log.extend(scheduling_log)  # Append the scheduling log

    elif algorithm == "fcfs":
        log.append("Using First-Come First-Served")
        scheduling_log, processes = fcfs_scheduling(processes, run_for)
        log.extend(scheduling_log)  # Append the scheduling log

    elif algorithm == "rr":
        if quantum is None:
            print("Error: Quantum not specified for Round Robin algorithm.")
            sys.exit(1)
        log.append(f"Using Round-Robin")
        log.append(f"Quantum {quantum:>3}\n")
        scheduling_log, processes = round_robin_scheduling(processes, run_for, quantum)
        log.extend(scheduling_log)  # Append the scheduling log

    # Check if the algorithm is valid
    if not scheduling_log:  # If no log was generated
        print(f"Error: Algorithm not specified/valid.")
    else:
        generate_output(log, processes, input_file)
