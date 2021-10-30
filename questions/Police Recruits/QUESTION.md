The police department of your city has just started its journey. Initially, they don’t have any manpower. So, they started hiring new recruits in groups.

Meanwhile, crimes keeps occurring within the city. One member of the police force can investigate only one crime during his/her lifetime.

If there is no police officer free (isn't busy with crime) during the occurrence of a crime, it will go untreated.

Given the chronological order of crime occurrences and recruit hirings, find the number of crimes which will go untreated.

**Input**
The first line contains the number of test cases you have to solve, *T*.

The first line of each test case will contain an integer *n* ( ≤ n ≤ 1000), the number of events. The next line will contain *n* space-separated integers.

If the integer is -1 then it means a crime has occurred. Otherwise, the integer will be positive, the number of officers recruited together at that time. No more than 10 officers will be recruited at a time.

**Output**
Print a single integer, the number of crimes which will go untreated.

**Examples**
__Example 1__
Input
```
2
3
-1 -1 1
11
-1 -1 2 -1 -1 -1 -1 -1 -1 -1 -1
```
Output
```
2
8
```
__Example 2__
Input
```
1
8
1 -1 1 -1 -1 1 1 1
```
Output
```
1
```

**Note**
Lets consider the second example:
    Firstly one person is hired.
    Then crime appears, the last hired person will investigate this crime.
    One more person is hired.
    One more crime appears, the last hired person will investigate this crime.
    Crime appears. There is no free policeman at the time, so this crime will go untreated.
    One more person is hired.
    One more person is hired.
    One more person is hired. 

The answer is one, as one crime (on step 5) will go untreated.