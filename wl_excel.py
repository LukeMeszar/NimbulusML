import pandas
import sys
from pyomo.environ import *

df = pandas.read_excel(sys.argv[1], 'Delivery Costs', header=0, index_col=0)

N = list(df.index.map(str))
M = list(df.columns.map(str))
d = {(r,c) : df.at[r,c] for r in N for c in M}
P = int(sys.argv[2])

model = ConcreteModel(name=" (WL) ")
model.x = Var(N,M, bounds=(0,1))
model.y = Var(N, within=Binary)

def obj_rule(model):
    return sum(d[n,m]*model.x[n,m] for n in N for m in M)
model.obj = Objective(rule=obj_rule)

def one_per_cust_rule(model, m):
    return sum(model.x[n,m] for n in N) == 1
model.one_per_cust = Constraint(M, rule=one_per_cust_rule)

def warehouse_active_rule(model, n,m):
    return model.x[n,m] <= model.y[n]
model.warehouse_active = Constraint(N,M, rule=warehouse_active_rule)

def num_warehouses_rule(model):
    return sum(model.y[n] for n in N) <= P

model.num_warehouses = Constraint(rule=num_warehouses_rule)
solver = SolverFactory('glpk')
solver.solve(model)
for wl in N:
    if value(model.y[wl] > 0.5):
        customers = [str(cl) for cl in M if value(model.x[wl,cl] > 0.5)]
        print(str(wl) + ' serves customers: ' + str(customers))
    else:
        print(str(wl) + ': do not build')
