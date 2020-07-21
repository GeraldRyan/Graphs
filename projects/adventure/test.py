l = 'haha'

if 'l' in locals():
  print("True")
else:
  print("False")

path = [1,2,3,4,5,6,7]
print(path)
print([i*2 for i in path])

test = {  
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

running = 0
asdf = test.values()
for i in asdf:
  try:
    running += i
  except Exception as e:
    print(e)
print(running)