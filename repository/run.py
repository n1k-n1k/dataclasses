from . import MemoryMockRepository

repo = MemoryMockRepository()
data = [
    {"a": 1, "b": 2},
    {"c": 3, "d": 4}
]

repo.add_all(data)
print(repo)
repo.add(data[0])
print(repo)
repo._delete_all()
print(repo)
