import pickle

def save_object_as_text(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_object_from_text(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj

# Example class definition
class MyClass:
    def __init__(self, name):
        self.name = name
        self.data = []
        print(dir(self))
    def __repr__(self):
        attrs = ', '.join(f"{key}={value}" for key, value in vars(self).items())
        return f"MyClass({attrs})"

    def run(self):
        for i in range(10):
            self.data.append(i)

# Example object
my_object = MyClass("John")
my_object.run()
# Save object to a text file
save_object_as_text(my_object, 'object_data.txt')

# Load object from the saved text file
loaded_object = load_object_from_text('object_data.txt')

loaded_object.run()
# Print the loaded object
print("Loaded object:", loaded_object)
