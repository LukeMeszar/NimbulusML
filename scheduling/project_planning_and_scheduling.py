import math
import networkx as nx

class Job:
    def __init__(self, job_name, duration, successors, predecessors):
        self.job_name = job_name
        self.duration = duration
        self.successors = successors
        self.predecessors = predecessors

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

def parse_data():
    with open("precedence_constraints.txt") as f:
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

def find_critical_jobs(job_schedule_list):
    critical_jobs_list = []
    time_zero_critical_jobs = []
    for js in job_schedule_list:
        if js.earliest_starting_time == js.latest_starting_time:
            critical_jobs_list.append(js)
            if js.earliest_starting_time == 0:
                time_zero_critical_jobs.append(js)
    return critical_jobs_list, time_zero_critical_jobs

def find_critical_paths(critical_jobs_list, time_zero_critical_jobs, job_list):
    def find_job_predecessors(job):
        for j in job_list:
            if j.job_name == job.job_name:
                return j.successors

    critical_jobs_graph = nx.DiGraph()
    for job in critical_jobs_list:
        critical_jobs_graph.add_node(job.job_name)
    for job in critical_jobs_list:
        successors = find_job_predecessors(job)
        for successor in successors:
            if successor != 'e' and successor in critical_jobs_graph.nodes():
                critical_jobs_graph.add_edge(job.job_name, successor)
    start_node = time_zero_critical_jobs[0].job_name
    T = nx.dfs_tree(critical_jobs_graph,start_node)
    print(T.edges())

def test_graph():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3,4,5,6])
    G.add_edges_from([(1,2),(1,3),(3,2), (2,4), (3,4), (3,5), (4,6), (5,6)])
    T = nx.dfs_tree(G,1)
    print(T.edges())

if __name__ == '__main__':
    job_list = parse_data()
    job_schedule_list, c_max = forward_procedure(job_list)
    job_schedule_list = backward_procedure(job_list, job_schedule_list,c_max)
    critical_jobs_list, time_zero_critical_jobs = find_critical_jobs(job_schedule_list)
    find_critical_paths(critical_jobs_list, time_zero_critical_jobs, job_list)
    test_graph()
