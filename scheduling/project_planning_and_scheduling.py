import math
import networkx as nx

class Job:
    def __init__(self, job_name, duration, successors, predecessors):
        self.job_name = job_name
        self.duration = duration
        self.successors = successors
        self.predecessors = predecessors


class JobProb:
    def __init__(self, job_name, duration, successors, predecessors,variance):
        self.job_name = job_name
        self.duration = duration
        self.successors = successors
        self.predecessors = predecessors
        self.variance = variance

class JobSchedule:
    def __init__(self, job_name):
        self.job_name = job_name
        self.earliest_starting_time = 0
        self.latest_starting_time = 0
        self.earliest_completion_time = 0
        self.latest_completion_time = 0
    def set_earliest_starting_time(self,earliest_starting_time):
        self.earliest_starting_time = earliest_starting_time
    def set_latest_starting_time(self,latest_starting_time):
        self.latest_starting_time = latest_starting_time
    def set_earliest_completion_time(self,earliest_completion_time):
        self.earliest_completion_time = earliest_completion_time
    def set_latest_completion_time(self,latest_completion_time):
        self.latest_completion_time = latest_completion_time

def parse_data(filename):
    with open(filename) as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    data = data[1:]
    job_list = []
    for line in data:
        split = line.split(" ")
        job_name, duration, successors, predecessors = split[0], int(split[1]),\
         split[2], split[3]
        predecessors = predecessors.split(",")
        successors = successors.split(",")
        new_job = Job(job_name, duration, successors, predecessors)
        job_list.append(new_job)
    return job_list

def compute_expected_processing_time(durations_list):
    optimistic_processing_time = durations_list[0]
    most_like_processing_time = durations_list[1]
    pessimistic_processing_time = durations_list[2]
    return (optimistic_processing_time+4*most_like_processing_time+pessimistic_processing_time)/6

def compute_expected_variance(durations_list):
    optimistic_processing_time = durations_list[0]
    pessimistic_processing_time = durations_list[2]
    return ((pessimistic_processing_time-optimistic_processing_time)/6)**2

def parse_probabilistic_data(filename):
    with open(filename) as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    data = data[1:]
    job_list = []
    for line in data:
        split = line.split(" ")
        job_name, durations_list, successors, predecessors = split[0], split[1],\
         split[2], split[3]
        durations_list = [int(x) for x in durations_list.split(",")]
        expected_duration = compute_expected_processing_time(durations_list)
        predecessors = predecessors.split(",")
        successors = successors.split(",")
        expected_variance = compute_expected_variance(durations_list)
        new_job = JobProb(job_name, expected_duration, successors, predecessors, expected_variance)
        job_list.append(new_job)
    return job_list

def forward_procedure(job_list):
    job_schedule_list = []
    earliest_completion_time_dict = {}
    for job in job_list:
        if job.predecessors == ['e']:
            new_js = JobSchedule(job.job_name)
            new_js.set_earliest_starting_time(0)
            new_js.set_earliest_completion_time(job.duration)
            job_schedule_list.append(new_js)
            earliest_completion_time_dict[job.job_name] = job.duration

    def find_index_of_job(name):
        print(name)
        index = 0
        for job in job_list:
            if job.job_name == name:
                return index
            index += 1

    def forward_procedure_rec(job):
        max_previous_completion_time = 0
        for predecessor in job.predecessors:
            if predecessor not in earliest_completion_time_dict:
                index = find_index_of_job(predecessor)
                print(index)
                predecessor_job = job_list[index]
                forward_procedure_rec(predecessor_job)

            if earliest_completion_time_dict[predecessor] > max_previous_completion_time:
                max_previous_completion_time = earliest_completion_time_dict[predecessor]
        earliest_completion_time_dict[job.job_name] = max_previous_completion_time + job.duration
        new_js = JobSchedule(job.job_name)
        new_js.set_earliest_starting_time(max_previous_completion_time)
        new_js.set_earliest_completion_time(max_previous_completion_time+job.duration)
        job_schedule_list.append(new_js)

    for job in job_list:
        if job.predecessors != ['e']:
            forward_procedure_rec(job)

    return job_schedule_list, max(list(earliest_completion_time_dict.values()))



def backward_procedure(job_list, job_schedule_list, c_max):
    def find_index_of_job_schedule(name):
        index = 0
        for js in job_schedule_list:
            if js.job_name == name:
                return index
            index += 1
    latest_starting_time_dict = {}
    for job in job_list:
        if job.successors == ['e']:
            js_index = find_index_of_job_schedule(job.job_name)
            current_js = job_schedule_list[js_index]
            current_js.set_latest_completion_time(c_max)
            current_js.set_latest_starting_time(c_max-job.duration)
            latest_starting_time_dict[job.job_name] = c_max-job.duration

    def find_index_of_job(name):
        index = 0
        for job in job_list:
            if job.job_name == name:
                return index
            index += 1

    def backward_procedure_rec(job):
        min_next_starting_time = math.inf
        for successor in job.successors:
            if successor not in latest_starting_time_dict:
                index = find_index_of_job(successor)
                successor_job = job_list[index]
                backward_procedure_rec(successor_job)

            if latest_starting_time_dict[successor] < min_next_starting_time:
                min_next_starting_time = latest_starting_time_dict[successor]
        latest_starting_time_dict[job.job_name] = min_next_starting_time - job.duration
        js_index = find_index_of_job_schedule(job.job_name)
        current_js = job_schedule_list[js_index]
        current_js.set_latest_starting_time(min_next_starting_time - job.duration)
        current_js.set_latest_completion_time(min_next_starting_time)

    for job in job_list:
        if job.successors != ['e']:
            backward_procedure_rec(job)
    return job_schedule_list

def find_critical_jobs(job_schedule_list, job_list, c_max):
    def find_job_for_job_schedule(job_schedule):
        for j in job_list:
            if j.job_name == job_schedule.job_name:
                return j
    critical_jobs_list = []
    time_zero_critical_jobs = []
    time_cmax_critical_jobs = []
    for js in job_schedule_list:
        if js.earliest_starting_time == js.latest_starting_time:
            corresponding_job = find_job_for_job_schedule(js)
            critical_jobs_list.append(corresponding_job)
            if js.earliest_starting_time == 0:
                time_zero_critical_jobs.append(corresponding_job)
            if js.latest_completion_time == c_max:
                time_cmax_critical_jobs.append(corresponding_job)

    return critical_jobs_list, time_zero_critical_jobs, time_cmax_critical_jobs

def build_critical_paths_graph(critical_jobs_list):
    critical_jobs_graph = nx.DiGraph()
    for job in critical_jobs_list:
        critical_jobs_graph.add_node(job.job_name)
    for job in critical_jobs_list:
        for successor in job.successors:
            if successor != 'e' and successor in critical_jobs_graph.nodes():
                critical_jobs_graph.add_edge(job.job_name, successor)
    return critical_jobs_graph

def find_all_critical_paths(critical_jobs_graph, time_zero_critical_jobs, time_cmax_critical_jobs):

    def find_all_paths(G,current_node,target_node,visited, path):
        visited[current_node] = True
        path.append(current_node)
        if current_node == target_node:
            all_paths.append(path[:])
        else:
            neighboring_nodes = G[current_node]
            for neighbor in neighboring_nodes:
                if visited[neighbor] == False:
                    find_all_paths(G, neighbor, target_node, visited,path)
        path.pop()
        visited[current_node] = False
    all_paths = []
    for t_zero in time_zero_critical_jobs:
        for t_cmax in time_cmax_critical_jobs:
            visited = dict(zip(critical_jobs_graph.nodes(), [False]*critical_jobs_graph.number_of_nodes()))
            path = []
            find_all_paths(critical_jobs_graph, t_zero.job_name, t_cmax.job_name, visited, path)
    return all_paths

def compute_expected_makespan(critical_jobs_list):
    makespan = 0
    for job in critical_jobs_list:
        makespan += job.duration
    return makespan

def compute_variance_makespan(critical_jobs_list):
    variance = 0
    for job in critical_jobs_list:
        variance += job.variance
    print(variance)
    return variance


if __name__ == '__main__':
    # job_list = parse_data("precedence_constraints.txt")
    # job_schedule_list, c_max = forward_procedure(job_list)
    # job_schedule_list = backward_procedure(job_list, job_schedule_list,c_max)
    # critical_jobs_list, time_zero_critical_jobs, time_cmax_critical_jobs = find_critical_jobs(job_schedule_list, c_max)
    # critical_jobs_graph = build_critical_paths_graph(critical_jobs_list, job_list)
    # print(find_all_critical_paths(critical_jobs_graph, time_zero_critical_jobs, time_cmax_critical_jobs))
    job_list = parse_probabilistic_data("pert_data.txt")
    job_schedule_list, c_max = forward_procedure(job_list)
    job_schedule_list = backward_procedure(job_list, job_schedule_list,c_max)
    critical_jobs_list, time_zero_critical_jobs, time_cmax_critical_jobs = find_critical_jobs(job_schedule_list, job_list, c_max)
    critical_jobs_graph = build_critical_paths_graph(critical_jobs_list)
    print(find_all_critical_paths(critical_jobs_graph, time_zero_critical_jobs, time_cmax_critical_jobs))
    compute_expected_makespan(critical_jobs_list)
    compute_variance_makespan(critical_jobs_list)
