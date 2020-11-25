# MEC

MEC.py has the main chunk of the code, Brute Force works perfectly but Welzl has a bug right now where R keeps growing larger than |R|=3 causing trivial() to crash. The Bug is in function welzlR, everything else seems fine. 

There are two examples at the bottom that are run when you run MEC.py . The bug only occurs sometimes due to randomness. If the bug does not occur, Welzl works correctly



tests.py is not complete yet. Right now I'm trying to plot the points along with circles provided by my algorithm vs "Miniball" which claims to also use Welzl's algorithm. 

Full tests still need to be written.


Code adapted from here:

https://www.geeksforgeeks.org/minimum-enclosing-circle-set-1/?ref=rp
https://www.geeksforgeeks.org/minimum-enclosing-circle-set-2-welzls-algorithm/
