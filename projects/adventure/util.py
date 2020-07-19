
# Note: This Queue class is sub-optimal. Why?
class Queue():

    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() >0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
        
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Python3 program to Remove elements of  
# list that repeated less than k times 
  
def removeElements(A, B): 
    return ', '.join(map(str, A)) in ', '.join(map(str, B)) 
              
# Driver code 
A = ['x', 'y', 'z'] 
B = ['x', 'a', 'y', 'x', 'b', 'z'] 
print(removeElements(A, B)) 

            
C = ['n', 's', 's']
D = ['n', 's', 's', 'n']
print(removeElements(C, D))

def issublist(subList, myList, start=0):
    if not subList: return 0
    lenList, lensubList = len(myList), len(subList)
    try:
        while lenList - start >= lensubList:
            start = myList.index(subList[0], start)
            for i in xrange(lensubList):
                if myList[start+i] != subList[i]:
                    break
            else:
                return start, start + lensubList - 1
            start += 1
        return False
    except:
        return False

print(issublist([1], [1,2]))

d =10
def rK(pat, txt, q=3109): 
    M = len(pat) 
    N = len(txt) 
    i = 0
    j = 0
    p = 0    # hash value for pattern 
    t = 0    # hash value for txt 
    h = 1
  
    # The value of h would be "pow(d, M-1)%q" 
    for i in range(M-1): 
        h = (h*d)%q 
  
    # Calculate the hash value of pattern and first window 
    # of text 
    for i in range(M): 
        p = (d*p + ord(pat[i]))%q 
        t = (d*t + ord(txt[i]))%q 
  
    # Slide the pattern over text one by one 
    for i in range(N-M+1): 
        # Check the hash values of current window of text and 
        # pattern if the hash values match then only check 
        # for characters on by one 
        if p==t: 
            # Check for characters one by one 
            for j in range(M): 
                if txt[i+j] != pat[j]: 
                    break
  
            j+=1
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1] 
            if j==M: 
                if i == 0:
                    print("Pattern found at index ", i) 
                    return True
  
        # Calculate hash value for next window of text: Remove 
        # leading digit, add trailing digit 
        if i < N-M: 
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+M]))%q 
  
            # We might get negative values of t, converting it to 
            # positive 
            if t < 0: 
                t = t+q 
    return False


print(rK(['s','b'], ['s','d'], 7))