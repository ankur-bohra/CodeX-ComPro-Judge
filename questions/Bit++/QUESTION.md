The classic programming language of Bitland is Bit++. This language is so peculiar and complicated.

The language is that peculiar as it has exactly one variable, called *x*. Also, there are two operations:
	•   Operation *++* increases the value of variable *x* by 1.
	•   Operation *--* decreases the value of variable *x* by 1.
	
A statement in language Bit++ is a sequence, consisting of exactly one operation and one variable *x*. The statement is written without spaces, that is, it can only contain characters *"+"*, *"-"*, *"X"*. Executing a statement means applying the operation it contains.

A program in Bit++ is a sequence of statements, each of them needs to be executed. Executing a program means executing all the statements it contains.

You're given a program in language Bit++. The initial value of x is *0*. Execute the program and find its final value (the value of the variable when this program is executed).

**Input**
The first line contains a single integer *T*, the number of test cases you have to solve. All test cases are independent i.e. *X* is 0 at the beginning of each case. 

The first line of each test case contains a single integer *n* (1 ≤ n ≤ 150) — the number of statements in the program.  

The next *n* lines contain a statement each. Each statement contains exactly one operation (*++* or *--*) and exactly one variable x (denoted as letter "*X*"). Thus, there are no empty statements. The operation and the variable can be written in any order.

**Output**
Print a single integer for each test case — the final value of *X*

**Example**
Input
```
2
1
++X
2
X++
--X
```
Output
```
1
0
```
