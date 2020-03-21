import pyomo.environ as pyo
from pyomo.opt import SolverFactory

'''
model = pyo.ConcreteModel()
model.x = pyo.Var([1,2], domain=pyo.NonNegativeReals)
model.OBJ = pyo.Objective(expr = 2*model.x[1] + 3*model.x[2])
model.Constraint1 = pyo.Constraint(expr = 3*model.x[1] + 4*model.x[2] >= 1)

print(f'x1 = {pyo.value(model.x[1])}')
print(f'x2 = {pyo.value(model.x[2])}')
print(f'Obj = {pyo.value(model.OBJ)}')

# display all duals
print ("Duals")
for c in model.component_objects(pyo.Constraint, active=True):
    print ("   Constraint",c)
    for index in c:
        print(c,index)
        #print ("      ", index, model.dual[c[index]])
#for i in dir(model):
#    print(i)
'''

model = pyo.ConcreteModel()


# for access to dual solution for constraints
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# declare decision variables
model.P1 = pyo.Var(domain=pyo.NonNegativeReals,bounds=(200,450))
model.P2 = pyo.Var(domain=pyo.NonNegativeReals,bounds=(150,350))
model.P3 = pyo.Var(domain=pyo.NonNegativeReals,bounds=(100,225))

# declare objective
model.profit = pyo.Objective(
    expr = 500 + 5.3*model.P1 + 0.004*model.P1**2 + \
           400 + 5.5*model.P2 + 0.006*model.P2**2 + \
           200 + 5.8*model.P3 + 0.009*model.P3**2,
    sense = pyo.minimize)

# declare constraints
#model.demand = pyo.inequality(975, model.P1 + model.P2 + model.P3, 975)
model.demand = pyo.Constraint(expr = (975, model.P1 + model.P2 + model.P3, 975))
#model.laborA = pyo.Constraint(expr = model.x + model.y <= 80)
#model.laborB = pyo.Constraint(expr = 2*model.x + model.y <= 100)

opt = SolverFactory('cplex')
results = opt.solve(model) 

print('*********MODEL DISPLAY*************')
model.display()
print('*********MODEL PPRINT**************')
model.pprint()
print('*********MODEL RESULTS*************')
print(results.write())
print('*********INCREMENTAL COST**********')
print("Constraint  value  lslack  uslack    dual")
print(model.demand,model.demand(),model.demand.lslack(),model.demand.uslack(),model.dual[model.demand])

#for c in (model.demand):
#     print(f'{c}, {c()}, {c.lslack()}, {c.uslack()}, {model.dual[c]}')
