import numpy as np

class Job:
    def __init__(self, job_name, processing_max, processing_min, cost_max, cost_min, successors, predecessors, index):
        self.job_name = job_name
        self.processing_max = processing_max
        self.processing_min = processing_min
        self.cost_max = cost_max
        self.cost_min = cost_min
        self.successors = successors
        self.predecessors = predecessors
        self.index = index
        self.marginal_cost = 0

def parse_data(filename):
    with open(filename) as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    data = data[1:]
    job_list = []
    index = 0
    for line in data:
        split = line.split(" ")
        job_name, processing_max, processing_min, cost_max, cost_min, successors, predecessors = split[0], int(split[1]),\
         int(split[2]), int(split[3]), int(split[4]), split[5], split[6]
        predecessors = predecessors.split(",")
        successors = successors.split(",")
        new_job = Job(job_name, processing_max, processing_min, cost_max, cost_min, successors, predecessors, index)
        index += 1
        job_list.append(new_job)
    return job_list

def compute_marginal_cost(job_list):
    for job in job_list:
        print(job.cost_min > job.cost_max)
        job.marginal_cost = (job.cost_min - job.cost_max)/(job.processing_max - job.processing_min)

def find_index_of_job(name):
    index = 0
    for job in job_list:
        if job.job_name == name:
            return index
        index += 1

def count_number_of_equations(job_list):
    eqn_counter = 0
    for job in job_list:
        if job.successors != ['e']:
            eqn_counter += len(job.successors)
    return eqn_counter

def build_linear_program(job_list, c0):
    num_slack_variables = count_number_of_equations(job_list)
    num_jobs = len(job_list)
    num_decision_variables = 2*num_jobs
    print(num_decision_variables)
    #build A matrix
    A = []
    eqn_counter = 0
    for job in job_list:
        if job.successors != ['e']:
            for successor in job.successors:
                successor_job = job_list[find_index_of_job(successor)]
                row = np.zeros(num_decision_variables + num_slack_variables+1)
                row[successor_job.index] = 1
                row[job.index] = -1
                row[job.index+num_jobs] = -1
                row[num_decision_variables + eqn_counter] = -1
                eqn_counter += 1
                A.append(row)
        c_row = np.zeros(num_decision_variables + num_slack_variables+1)
        c_row[-1] = 1
        c_row[job.index] = -1
        c_row[job.index+num_jobs] = -1
        A.append(c_row)
    #build objective function coefficients
    obj_func = np.zeros(num_decision_variables + num_slack_variables+1)
    obj_func[-1] = c0
    for job in job_list:
        obj_func[job.index+num_jobs] = -job.marginal_cost

    print(obj_func)


if __name__ == '__main__':
    job_list = parse_data('linear_costs.txt')
    compute_marginal_cost(job_list)
    build_linear_program(job_list, 6)
