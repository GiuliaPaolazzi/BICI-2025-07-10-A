from model.category import Category
from model.model import Model

mymodel = Model()
c = Category(5, "Electric Bikes")
mymodel.buildGraph(c)
print(f" n nodi: {mymodel.getNumNodi()}")