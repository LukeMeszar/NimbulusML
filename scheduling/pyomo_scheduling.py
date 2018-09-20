from pyomo.environ import *


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

def build_successors_list(job_list):
    successors_list = []
    for job in job_list:
        if job.successors != ['e']:
            for successor in job.successors:
                successors_list.append((job,job_list[find_index_of_job(successor)]))
    return successors_list

job_list = parse_data('linear_costs.txt')
compute_marginal_cost(job_list)
SL = build_successors_list(job_list)
c0 = 6.0
MC = [job.marginal_cost for job in job_list]
JN = [job for job in job_list]
CMax = ['cmax']

model = ConcreteModel(name=" (LCTO) ")
model.x = Var(JN, bounds=(0,None))
def duration_bounds(model,i):
    return (i.processing_min, i.processing_max)
model.p = Var(JN, bounds=duration_bounds)
model.cmax = Var(CMax, bounds=(0,None))

def obj_rule(model):
    return c0*model.cmax['cmax'] - sum(MC[j]*model.p[job_list[j]] for j in range(len(job_list)))
model.obj = Objective(rule=obj_rule)

def cmax_constraint_rule(model,j):
    return model.cmax['cmax'] - model.x[j] - model.p[j] >= 0
model.cmax_constraint = Constraint(JN,rule=cmax_constraint_rule)

def successors_constraint_rule(model,j):
    return model.x[j[1]] - model.p[j[0]] - model.x[j[0]] >= 0
model.successors_constraint = Constraint(SL, rule=successors_constraint_rule)
