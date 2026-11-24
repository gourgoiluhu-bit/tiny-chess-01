import sys
class B:
 def __init__(self,f="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
  p=f.split();self.b={};r=0
  for row in p[0].split('/'):
   c=0
   for ch in row:
    if ch.isdigit():c+=int(ch)
    else:self.b[(r,c)]=ch;c+=1
   r+=1
  self.t=p[1]
 def f(self):
  l=[]
  for r in range(8):
   e=0;s=""
   for c in range(8):
    p=self.b.get((r,c))
    if p:
     if e:s+=str(e);e=0
     s+=p
    else:e+=1
   if e:s+=str(e)
   l.append(s)
  return "/".join(l)+f" {self.t} - - 0 1"
 def e(self):
  v={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000,'p':-100,'n':-320,'b':-330,'r':-500,'q':-900,'k':-20000}
  s=sum(v.get(p,0) for p in self.b.values())
  return s if self.t=='w' else -s
 def m(self):
  ms=[];w=self.t=='w'
  for (r,c),p in list(self.b.items()):
   if (w and p.isupper()) or (not w and p.islower()):
    pl=p.lower()
    if pl=='p':
     dr=-1 if w else 1
     if (r+dr,c) not in self.b:ms.append(((r,c),(r+dr,c)))
     for dc in (-1,1):
      if (r+dr,c+dc) in self.b and self.b[(r+dr,c+dc)].isupper()!=w:ms.append(((r,c),(r+dr,c+dc)))
    elif pl in ('n','k'):
     ds=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)) if pl=='n' else ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
     for dr,dc in ds:
      tr,tc=r+dr,c+dc
      if 0<=tr<8 and 0<=tc<8 and ((tr,tc) not in self.b or self.b[(tr,tc)].isupper()!=w):ms.append(((r,c),(tr,tc)))
    else:
     ds=(( -1,-1),(-1,1),(1,-1),(1,1)) if pl=='b' else ()
     if pl in ('r','q'):ds+=((-1,0),(1,0),(0,-1),(0,1))
     for dr,dc in ds:
      tr,tc=r+dr,c+dc
      while 0<=tr<8 and 0<=tc<8:
       tp=self.b.get((tr,tc))
       if not tp:ms.append(((r,c),(tr,tc)))
       else:
        if tp.isupper()!=w:ms.append(((r,c),(tr,tc)))
        break
       tr,tc=tr+dr,c+dc
  return ms
 def x(self,m):
  nb=B(self.f());p=nb.b.pop(m[0],None);nb.b[m[1]]=p;nb.t='b' if self.t=='w' else 'w';return nb
def search(b,d,a,beta,mx):
 if d==0:return b.e(),None
 ms=b.m()
 if not ms:return b.e(),None
 best=None
 if mx:
  v=-99999
  for m in ms:
   ev,_=search(b.x(m),d-1,a,beta,0)
   if ev>v:v=ev;best=m
   a=max(a,ev)
   if beta<=a:break
  return v,best
 else:
  v=99999
  for m in ms:
   ev,_=search(b.x(m),d-1,a,beta,1)
   if ev<v:v=ev;best=m
   beta=min(beta,ev)
   if beta<=a:break
  return v,best
def main():
 b=B()
 for line in sys.stdin:
  l=line.strip()
  if l=="uci":print("id name Tiny\nuciok")
  elif l=="isready":print("readyok")
  elif l.startswith("position"):
   p=l.split("fen ")
   b=B(p[1]) if len(p)>1 else B()
  elif l.startswith("go"):
   _,bm=search(b,2,-99999,99999,1)
   cols="abcdefgh"
   print(f"bestmove {cols[bm[0][1]]}{8-bm[0][0]}{cols[bm[1][1]]}{8-bm[1][0]}" if bm else "bestmove a1a1")
  elif l=="quit":break
  sys.stdout.flush()
if __name__=="__main__":main()
