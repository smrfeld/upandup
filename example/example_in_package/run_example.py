import mypackage as mp

# Test the update
data = {"x": 1}
obj = mp.load_data_schema(data, mp.Options())
print("Result:")
print(f"Loaded object: {obj} of type {type(obj).__name__}")