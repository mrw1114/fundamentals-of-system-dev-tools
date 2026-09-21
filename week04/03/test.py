import re
raw = '{"name": "Alyssa P. Hacker", "college": "MIT"}'
result = re.search(r'"name"\s*:\s*"([^"]*)"' , raw).group(1)
print(result)
