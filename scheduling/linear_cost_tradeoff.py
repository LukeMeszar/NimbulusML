class Job:
    def __init__(self, job_name, processing_max, processing_min, cost_max, cost_min, successors, predecessors):
        self.job_name = job_name
        self.processing_max = processing_max
        self.processing_min = processing_min
        self.cost_max = cost_max
        self.cost_min = cost_min
        self.successors = successors
        self.predecessors = predecessors

def parse_data(filename):
    with open(filename) as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    data = data[1:]
    job_list = []
    for line in data:
        split = line.split(" ")
        job_name, processing_max, processing_min, cost_max, cost_min, successors, predecessors = split[0], int(split[1]),\
         int(split[2]), int(split[3]), int(split[4]), split[5], split[6]
        predecessors = predecessors.split(",")
        successors = successors.split(",")
        new_job = Job(job_name, processing_max, processing_min, cost_max, cost_min, successors, predecessors)
        job_list.append(new_job)
    for job in job_list:
        print(job.job_name, job.processing_max, job.processing_min, job.cost_max, job.cost_min, job.successors, job.predecessors)
    return job_list

if __name__ == '__main__':
    parse_data('linear_costs.txt')
