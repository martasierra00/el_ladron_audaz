import pandas as pd
import time
from pyomo.environ import *

# Lectura de datos
file_path = "data/ks_45_0"
data = pd.read_csv(file_path, header=None, delimiter=' ')
print(data)
No_Objets = data[0][0]
pTotalSpace = data[1][0]
pObjets_Space = {(j, i): data[j][i + 1] for i in range(No_Objets) for j in range(2)}

input_data = {None: {
    'sObjets': {None: list(range(No_Objets))},
    'pObjets_Space': pObjets_Space,
    'pTotalSpace': {None: pTotalSpace}
}}

# Crea el modelo
model = AbstractModel()

model.sObjets = Set()

# Define los parámetros
model.pObjets_Space = Param(model.sObjets, model.sObjets, mutable=True)
model.pTotalSpace = Param()

# Define las variables
model.vAlpha = Var(model.sObjets, domain=Binary)


# Define la función objetivo
def f_obj(model):
    return sum(model.pObjets_Space[(0, i)] * model.vAlpha[i] for i in model.sObjets)


model.obj_func = Objective(rule=f_obj, sense=pyomo.core.maximize)


# Define las restricciones
def c1(model):
    return sum(pObjets_Space[(1, i)] * model.vAlpha[i] for i in model.sObjets) <= model.pTotalSpace


model.const = Constraint(rule=c1)

# Crea una instancia del modelo con los datos
instance = model.create_instance(input_data)

start_time = time.time()

# Resuelve el modelo
opt = SolverFactory('cbc', executable=r'C:\cbc\bin\cbc.exe')
results = opt.solve(instance)

end_time = time.time()
execution_time = end_time - start_time

# Imprime el estado de la solución
print("Estado de la solución:", results.solver.termination_condition)

# Imprime el valor óptimo de las variables de decisión
for i in instance.sObjets:
    if value(instance.vAlpha[i] == 1):
        print("objeto {}: {}".format(i, value(instance.vAlpha[i])))

print("Valor objetivo óptimo:", value(instance.obj_func))

print("Tiempo de ejecución:", execution_time, "segundos")
