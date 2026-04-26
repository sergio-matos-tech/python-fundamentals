def people(**kwargs):
    print(type(kwargs))
    for k, v in kwargs.items():
        print(f"{k} = {v}")


people(name="Carla", age=54, weight=73.3)
