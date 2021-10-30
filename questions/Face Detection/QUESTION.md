The developers of Looksery have to write an efficient algorithm that detects faces on a picture. Unfortunately, they are currently busy preparing a contest for you, so you will have to do it for them.

In this problem an image is a rectangular table that consists of lowercase Latin letters. A face on the image is a *2 × 2* square, such that from the four letters of this square you can make word "face".

You need to write a program that determines the number of faces on the image. The squares that correspond to the faces can overlap.

**Input**
The first line contains the number of test cases you have to solve, *T*.

The first line of each test case contains two space-separated integers, *n* and *m* (*1 ≤ n, m ≤ 50*) — the height and the width of the image, respectively.

Next *n* lines define the image. Each line contains *m* lowercase Latin letters.

**Output**
Print the number of faces on the image for each test case.

**Examples**
__Example 1__
Input
```
1
4 4
xxxx
xfax
xcex
xxxx
```
Output
```
1
```

__Example 2__
Input
```
1
4 2
xx
cf
ae
xx
```
Output
```
1
```
__Example 3__
Input
```
1
2 3
fac
cef
```
Output
```
2
```
__Example 4__
Input
```
1
1 4
face
```
Output
```
0
```

**Note**

In the first sample the image contains a single face, located in a square with the upper left corner at the second line and the second column:
```
x x x x
x|f a|x
x|c e|x
x x x x
```
In the second sample the image also contains exactly one face, its upper left corner is at the second row and the first column.

In the third sample two faces are shown:
```
|f a|c
|c e|f
```
```
f|a c|
c|e f|
```

In the fourth sample the image has no faces on it.