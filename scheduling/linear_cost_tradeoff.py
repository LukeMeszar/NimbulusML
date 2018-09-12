import numpy as np
from scipy.optimize import linprog

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
        job.marginal_cost = (job.cost_max - job.cost_min)/(job.processing_max - job.processing_min)

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
    num_jobs = len(job_list)
    num_slack_variables = count_number_of_equations(job_list) + num_jobs
    num_decision_variables = 2*num_jobs
    #build A matrix
    A = []
    eqn_counter = 0
    for job in job_list:
        if job.successors != ['e']:
            for successor in job.successors:
                index = find_index_of_job(successor)
                successor_job = job_list[index]
                row = np.zeros(num_decision_variables + num_slack_variables+1)
                row[successor_job.index] = 1
                row[job.index] = -1
                row[job.index+num_jobs] = -1
                row[num_decision_variables + eqn_counter] = -1
                eqn_counter += 1
                A.append(row)
    for job in job_list:
        c_row = np.zeros(num_decision_variables + num_slack_variables+1)
        c_row[-1] = 1
        c_row[job.index] = -1
        c_row[job.index+num_jobs] = -1
        c_row[job.index+3*num_jobs] = -1
        #print(c_row)
        A.append(c_row)

    #build objective function coefficients
    obj_func = np.zeros(num_decision_variables + num_slack_variables+1)
    obj_func[-1] = c0
    for job in job_list:
        obj_func[job.index+num_jobs] = -job.marginal_cost
    #compute bounds
    bounds = []
    #bounds for starting time variables
    for i in range(0,num_jobs):
        bounds.append((0,None))
    #bounds for duration variables
    for job in job_list:
        duration_bound = (job.processing_min, job.processing_max)
        bounds.append(duration_bound)
    #bounds for slack variables
    for i in range(num_slack_variables):
        bounds.append((0,None))
    bounds.append((0,None))
    return A, obj_func, bounds

def build_linear_program_no_slack(job_list, c0):
    num_jobs = len(job_list)
    num_decision_variables = 2*num_jobs
    #build A matrix
    A = []
    for job in job_list:
        if job.successors != ['e']:
            for successor in job.successors:
                index = find_index_of_job(successor)
                successor_job = job_list[index]
                row = np.zeros(num_decision_variables +1)
                row[successor_job.index] = 1
                row[job.index] = -1
                row[job.index+num_jobs] = -1
                A.append(-1*row)
    for job in job_list:
        c_row = np.zeros(num_decision_variables + 1)
        c_row[-1] = 1
        c_row[job.index] = -1
        c_row[job.index+num_jobs] = -1
        #print(c_row)
        A.append(-1*c_row)

    #build objective function coefficients
    obj_func = np.zeros(num_decision_variables + 1)
    obj_func[-1] = c0
    for job in job_list:
        obj_func[job.index+num_jobs] = -job.marginal_cost
    #compute bounds
    bounds = []
    #bounds for starting time variables
    for i in range(0,num_jobs):
        bounds.append((0,None))
    #bounds for duration variables
    for job in job_list:
        duration_bound = (job.processing_min, job.processing_max)
        bounds.append(duration_bound)
    #bounds for slack variables
    bounds.append((0,None))
    return A, obj_func, bounds

def solve_linear_program(A, obj_func, bounds, method="simplex"):
    b = np.zeros(len(A))
    res = linprog(obj_func, A_ub=A,b_ub=b)
    print(res)

if __name__ == '__main__':
    job_list = parse_data('linear_costs.txt')
    #compute_minimum_cost(job_list)
    compute_marginal_cost(job_list)
    A, obj_func, bounds = build_linear_program_no_slack(job_list, 6)
    #print(A)
    matrix_form = "{"
    for row in A:
        row_str = "{"
        for a in row[:-1]:
            element_str = str(a)+","
            row_str += element_str
        row_str += str(row[-1])+"}"
        matrix_form += row_str+","
    matrix_form = matrix_form[:-1]
    matrix_form += "}"
    print(matrix_form)
    print("\n\n")
    obj_str = "{"
    for a in obj_func[:-1]:
        element_str = str(a)+","
        obj_str += element_str
    obj_str += str(obj_func[-1])+"}"
    print(obj_str)
    print("\n\n")
    bounds_str = "{"
    for bound in bounds[:-1]:
        bound_s = "{" + str(bound[0]) + "," + str(bound[1]) + "},"
        bounds_str += (bound_s)
    bounds_str += ("{" + str(bounds[-1][0]) + "," + str(bounds[-1][1]) + "}}")
    print(bounds_str)
    b = [0]*len(A)
    print(b)
    solve_linear_program(A, obj_func, bounds)
