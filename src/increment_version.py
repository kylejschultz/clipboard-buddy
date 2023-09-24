def increment_version(version: str) -> str:
    major, minor, patch = map(int, version.split('.'))
    patch += 1
    return f"{major}.{minor}.{patch}"

with open("version.txt", "r") as file:
    current_version = file.readline().strip()

new_version = increment_version(current_version)

with open("version.txt", "w") as file:
    file.write(new_version)
    
print(new_version) 
