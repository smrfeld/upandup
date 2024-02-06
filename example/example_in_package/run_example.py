import example_package as ep

data = {"x": 1}
obj = ep.load_data_schema(data, ep.Options())
print(f"Loaded object: {obj}")