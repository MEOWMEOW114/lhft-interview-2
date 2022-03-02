def gen_seq(th = 29):
   initial = 1
   while True:
      
      yield initial
      initial = initial / 2






def first_N(N = 0):
 
   if N == 0:
      return 0
   counter = N
   a = gen_seq()
   result = 0
   try:
      while counter > 0 :
         result = result + next(a)
         counter = counter - 1
   except StopIteration:
      pass
   return result

if __name__ == "__main__":
   xx = first_N(0)
   print(xx)