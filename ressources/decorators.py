import time

def timer(func):
  def wrapper(*args, **kwargs):
    strt = time.time()
    rv = func()
    total = time.time() - start
    print("Time:", total)
    return rb
  return wrapper

@timer
def test2():
  time.sleep(2)

test2()

#Can be use to time functions, log function calls, validate input, etc
