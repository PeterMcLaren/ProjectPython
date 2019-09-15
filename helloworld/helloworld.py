msg = "Hello world"
for test in range(0,100,10):
    print("the value is "+str(test)+" in case you were wondering!!")
class Dog:
    # Class Attribute
    species='mammal'
    # initializer
    def __init__(self, name,age):
        self.name=name
        self.age=age
a = Dog("fido",4)
b = Dog("test",5)
c = Dog("blah",6)
print(type(a))
print(a.age)
print("{} is {} years old".format(a.name,a.age))

def get_biggest_number(*args):
    print(type(args))
    return max(args)

print("the oldest dog is {}".format(get_biggest_number(a.age,b.age,c.age,c.age,c.age)))