def call_counter(func):
  times_called = 0
  def func_with_counter(*args, **kwargs):
    nonlocal times_called
    times_called += 1
    print(f'---{func.__name__} called x{times_called}')
    for i, arg in enumerate(args):
      print(f'------arg {i}: {arg}')
    for k, v in kwargs.items():
      print(f'------arg {k}: {v}')
    print('---now running the function:')
    func(*args, **kwargs) # finally call the decorated function
  return func_with_counter

@call_counter
def print_aaa():
  print("aaa")

@call_counter
def print_bbb(a, b="black"):
  print("bbb")

print_aaa()
print_aaa()

print_bbb("yellow")

print_aaa()
print_aaa()

print_bbb(a="green", b="red")
