
"""DAA Assignment 5 (CO5): backtracking, complexity, approximation.
Run all: python daa_assignment5.py
Run one: python daa_assignment5.py --task A1|A2|B1|B2|B3|B4
Python standard library only.
"""
import argparse, itertools, math, random, time

# A1: Graph-colouring trace for S1..S5, m=2
def A1():
    n,m=5,2; edges=[(0,2),(2,3),(3,1),(3,4)]
    adj=[set() for _ in range(n)]
    for u,v in edges: adj[u].add(v); adj[v].add(u)
    c=[0]*n; log=[]
    def dfs(i):
        if i==n: log.append("All vertices assigned -> SUCCESS"); return True
        for k in range(1,m+1):
            bad=next((u for u in adj[i] if c[u]==k),None)
            if bad is not None:
                log.append(f"Try S{i+1}={k}: conflict with S{bad+1} -> REJECT"); continue
            log.append(f"Try S{i+1}={k}: safe -> ACCEPT")
            c[i]=k
            if dfs(i+1): return True
            c[i]=0; log.append(f"Undo S{i+1}={k} -> BACKTRACK")
        return False
    print("\nA1 - GRAPH COLOURING TRACE")
    print("Edges: S1-S3, S3-S4, S4-S2, S4-S5; m=2")
    ok=dfs(0)
    for x in log: print(" ",x)
    print("Final colouring:",{f"S{i+1}":c[i] for i in range(n)})
    assert ok and c==[1,2,2,1,2]

# A2: positive-integer subset-sum pruning
def A2():
    a,T=[4,7,9,12,15],20
    suffix=[sum(a[i:]) for i in range(len(a)+1)]
    stats={"nodes":0,"overshoot prunes":0,"cannot-reach prunes":0,"solutions":0}
    log=[]
    def dfs(i,s,chosen):
        stats["nodes"]+=1
        if s==T:
            stats["solutions"]+=1; log.append(f"{chosen} sum={s} -> SOLUTION"); return True
        if s>T:
            stats["overshoot prunes"]+=1; log.append(f"{chosen} sum={s}>20 -> PRUNE"); return False
        if i==len(a): return False
        if s+suffix[i]<T:
            stats["cannot-reach prunes"]+=1
            log.append(f"{chosen} sum={s}, max reachable={s+suffix[i]}<20 -> PRUNE"); return False
        x=dfs(i+1,s+a[i],chosen+[a[i]])
        y=dfs(i+1,s,chosen)
        return x or y
    print("\nA2 - SUBSET SUM PRUNING TRACE")
    print("Set:",a,"Target:",T)
    dfs(0,0,[])
    for x in log: print(" ",x)
    print("Counters:",stats)
    print("The positive-number pruning rules are not valid unchanged when negatives are present.")

# B1/B2: instrumented m-colouring
class Stats:
    def __init__(self): self.nodes=self.attempts=self.rejected=self.backtracks=self.depth=0
def adjlist(n,E):
    a=[set() for _ in range(n)]
    for u,v in E: a[u].add(v); a[v].add(u)
    return a
def input_order(n,a): return list(range(n))
def heuristic_order(n,a):
    rem=set(range(n)); order=[]
    while rem:
        placed=set(order)
        v=max(rem,key=lambda x:(len(a[x]&placed),len(a[x]),-x))
        order.append(v); rem.remove(v)
    return order
def colour(n,E,m,order_fn=input_order):
    a=adjlist(n,E); order=order_fn(n,a); c=[0]*n; st=Stats()
    def dfs(k):
        st.nodes+=1; st.depth=max(st.depth,k)
        if k==n: return True
        v=order[k]
        for col in range(1,m+1):
            st.attempts+=1
            if all(c[u]!=col for u in a[v]):
                c[v]=col
                if dfs(k+1): return True
                c[v]=0; st.backtracks+=1
            else: st.rejected+=1
        return False
    ok=dfs(0)
    return ok,(c[:] if ok else None),st,order
def B1():
    print("\nB1 - INSTRUMENTED GRAPH COLOURING")
    tests=[
      ("colourable",6,[(0,1),(1,2),(2,3),(3,4),(4,0),(0,2),(5,3)],3,True),
      ("K4 with 3 colours",4,[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],3,False),
      ("isolated vertices",5,[],1,True),("single vertex",1,[],1,True),
      ("zero colours",3,[(0,1)],0,False),("empty graph",0,[],2,True),
      ("one edge / one colour",2,[(0,1)],1,False)]
    print("B1.1 Validation:")
    for name,n,E,m,expected in tests:
        ok,c,s,_=colour(n,E,m)
        assert ok==expected
        if ok: assert all(c[u]!=c[v] for u,v in E)
        print(f" {name:<24} {'SUCCESS' if ok else 'FAILURE':<8} nodes={s.nodes} backtracks={s.backtracks}")
    print("All validation assertions passed.")
    rim=[(i,(i+1)%7) for i in range(7)]
    outer=[(i,(i+1)%5) for i in range(5)]
    spokes=[(i,i+5) for i in range(5)]
    inner=[(5+i,5+(i+2)%5) for i in range(5)]
    graphs=[
      ("G1 trace",(5,[(0,1),(0,2),(1,2),(1,3),(2,3),(3,4)],3)),
      ("G2 hidden K4",(10,[(0,1),(2,3),(4,5),(6,7)]+[(x,y) for x in range(6,10) for y in range(x+1,10)],3)),
      ("G3 wheel W7",(8,rim+[(i,7) for i in range(7)],3)),
      ("G4 Petersen",(10,outer+spokes+inner,3))]
    print("\nB1.3/B1.4 V1 input order vs V2 most-constrained-first")
    for name,(n,E,m) in graphs:
        results=[colour(n,E,m,f) for f in (input_order,heuristic_order)]
        print(f"{name:<16} V1 nodes={results[0][2].nodes:>6,} attempts={results[0][2].attempts:>7,} "
              f"rejected={results[0][2].rejected:>7,} backtracks={results[0][2].backtracks:>6,} | "
              f"V2 nodes={results[1][2].nodes:>6,} attempts={results[1][2].attempts:>7,} "
              f"rejected={results[1][2].rejected:>7,} backtracks={results[1][2].backtracks:>6,}")
def B2():
    print("\nB2 - ADVERSARIAL GRAPHS (n=12, m=3)")
    A=[(i,i+1) for i in range(11)]
    B=[(0,1),(2,3),(4,5),(6,7)]+[(x,y) for x in range(8,12) for y in range(x+1,12)]
    print("Prediction: B hides an uncolourable K4 after four unconstrained pairs.")
    print(f"{'Graph':<10}{'Order':<14}{'Result':<9}{'Nodes':>9}{'Attempts':>10}{'Rejected':>10}{'Backtracks':>12}")
    for name,E in (("A easy",A),("B hard",B)):
        for label,fn in (("input",input_order),("heuristic",heuristic_order)):
            ok,c,s,_=colour(12,E,3,fn)
            print(f"{name:<10}{label:<14}{'FOUND' if ok else 'NONE':<9}{s.nodes:>9,}{s.attempts:>10,}{s.rejected:>10,}{s.backtracks:>12,}")
    nodes=colour(12,B,3,input_order)[2].nodes
    assert nodes==21772, nodes
    print("Confirmed input-order Graph B node count:",nodes)

# B3: exact and greedy set cover
def exact_cover(U,S):
    names=list(S); count=0
    for r in range(1,len(names)+1):
        for combo in itertools.combinations(names,r):
            count+=1; cov=set()
            for x in combo: cov|=S[x]
            if cov>=U: return r,list(combo),count
    return None,None,count
def greedy_cover(U,S):
    uncovered=set(U); chosen=[]; evals=0; steps=[]
    while uncovered:
        best,gain=None,0
        for name,zones in S.items():
            evals+=1; g=len(zones&uncovered)
            if g>gain: best,gain=name,g
        if best is None: return None,None,evals,steps
        chosen.append(best); uncovered-=S[best]; steps.append((best,gain,sorted(uncovered)))
    return len(chosen),chosen,evals,steps
def B3():
    print("\nB3 - EXACT VS GREEDY SET COVER")
    Z=lambda *x:set(x)
    cases={
      1:(set(range(1,7)),{"C1":Z(1,2,3),"C2":Z(4,5,6),"C3":Z(1,4),"C4":Z(2,5),"C5":Z(3,6)}),
      2:(set(range(1,9)),{"C1":Z(1,2,3,4),"C2":Z(5,6,7,8),"C3":Z(1,5),"C4":Z(2,6),"C5":Z(3,7,8),"C6":Z(4,8)}),
      3:(set(range(1,10)),{"C1":Z(1,2,3),"C2":Z(3,4,5),"C3":Z(5,6,7),"C4":Z(7,8,9),"C5":Z(1,4,7),"C6":Z(2,5,8),"C7":Z(3,6,9)})}
    print("B3.1 small cases:")
    for k,(U,S) in cases.items():
        e,ec,_=exact_cover(U,S); g,gc,_,_=greedy_cover(U,S)
        print(f" Case {k}: exact={e} {ec}; greedy={g} {gc}; same={e==g}")
    print("\nB3.2 counterexample:")
    U=set(range(1,7)); S={"Big":Z(2,3,4,5),"L":Z(1,2,3),"R":Z(4,5,6)}
    e,ec,_=exact_cover(U,S); g,gc,eff,steps=greedy_cover(U,S)
    print("Universe:",sorted(U),"Sets:",{k:sorted(v) for k,v in S.items()})
    print("Optimal:",e,ec,"| Greedy:",g,gc)
    for i,(name,gain,left) in enumerate(steps,1): print(f" step {i}: pick {name}, gain={gain}, remaining={left}")
    assert (e,g)==(2,3)
    print("\nB3.3 scalability (fixed seeds):")
    def make(nz,ns,seed):
        rnd=random.Random(seed); U=set(range(1,nz+1)); S={}
        for i in range(1,ns+1): S[f"C{i}"]=set(rnd.sample(sorted(U),rnd.randint(2,max(3,nz//4))))
        covered=set().union(*S.values())
        for z in U-covered: S[f"C{rnd.randint(1,ns)}"].add(z)
        return U,S
    print(f"{'Zones':<7}{'Centres':<9}{'Exact combos':>14}{'Greedy evals':>14}{'Exact':>8}{'Greedy':>8}{'Exact s':>10}{'Greedy s':>10}")
    for nz,ns in [(8,8),(10,12),(12,16),(14,20),(16,24),(18,28),(20,32)]:
        U,S=make(nz,ns,nz*100+ns)
        t=time.perf_counter(); e,_,cnt=exact_cover(U,S); te=time.perf_counter()-t
        t=time.perf_counter(); g,_,ev,_=greedy_cover(U,S); tg=time.perf_counter()-t
        print(f"{nz:<7}{ns:<9}{cnt:>14,}{ev:>14,}{e:>8}{g:>8}{te:>10.4f}{tg:>10.6f}")

# B4: First-Fit Decreasing and exact small-instance validation
def ffd(items,C):
    bins=[]
    for w in sorted(items,reverse=True):
        if w>C: raise ValueError("Workload exceeds capacity")
        for b in bins:
            if b[0]>=w: b[0]-=w; b[1].append(w); break
        else: bins.append([C-w,[w]])
    return bins
def exact_bins(items,C):
    a=sorted(items,reverse=True); best=[len(a)]
    def dfs(i,bins):
        if len(bins)>=best[0]: return
        if i==len(a): best[0]=len(bins); return
        w=a[i]; seen=set()
        for j in range(len(bins)):
            if bins[j]+w<=C and bins[j] not in seen:
                seen.add(bins[j]); bins[j]+=w; dfs(i+1,bins); bins[j]-=w
        bins.append(w); dfs(i+1,bins); bins.pop()
    dfs(0,[]); return best[0]
def show_bins(bins,C):
    print(f"Servers used: {len(bins)} (capacity={C})")
    for i,(rem,ws) in enumerate(bins,1): print(f" Server {i}: workloads={ws} load={C-rem} remaining={rem}")
def B4():
    print("\nB4 - FIRST-FIT DECREASING BIN PACKING")
    C=100; demo=[45,70,30,25,60,15,55,20,40,10,35,50]
    print("B4.1 sample:")
    bins=ffd(demo,C); show_bins(bins,C)
    print("Lower bound:",math.ceil(sum(demo)/C),"Exact optimum:",exact_bins(demo,C))
    print("\nB4.2 challenge: C=10, workloads=[7,5,4,4,3,3,2,2]")
    challenge=[7,5,4,4,3,3,2,2]; cb=ffd(challenge,10); show_bins(cb,10)
    opt=exact_bins(challenge,10); print("Exact optimum:",opt,"FFD:",len(cb))
    assert opt==3 and len(cb)==4
    print("\nB4.3 production scale (C=100):")
    print(f"{'Items':<10}{'FFD bins':<12}{'Lower bound':<14}{'Ratio':<9}{'Util %':<10}{'Time s'}")
    rnd=random.Random(1)
    for n in (1000,5000,20000):
        items=[rnd.randint(5,60) for _ in range(n)]
        t=time.perf_counter(); packed=ffd(items,100); dt=time.perf_counter()-t
        lb=math.ceil(sum(items)/100); util=100*sum(items)/(100*len(packed))
        print(f"{n:<10}{len(packed):<12,}{lb:<14,}{len(packed)/lb:<9.4f}{util:<10.2f}{dt:.3f}")
    print("FFD guarantee: FFD(I) <= 11/9 * OPT(I) + 6/9.")

TASKS={"A1":A1,"A2":A2,"B1":B1,"B2":B2,"B3":B3,"B4":B4}
def main():
    p=argparse.ArgumentParser(description="DAA Assignment 5 CO5")
    p.add_argument("--task",choices=TASKS)
    a=p.parse_args()
    print("="*88+"\nDESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 5 (CO5)\nSearch, Complexity and Approximation Engineering\n"+"="*88)
    if a.task: TASKS[a.task]()
    else:
        for fn in TASKS.values(): fn()
    print("\n"+"="*88+"\nASSIGNMENT 5 EXECUTION COMPLETED\n"+"="*88)
if __name__=="__main__": main()
