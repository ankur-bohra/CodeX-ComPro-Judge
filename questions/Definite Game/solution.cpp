#include <bits/stdc++.h>
using namespace std;

int main() {
    freopen("INPUT.txt", "r", stdin);
    freopen("ANSWER.txt", "w", stdout);
    int T;
    cin >> T;
    
    while (T--) {
        int n;
        cin >> n;
    
        if (n==2) {
            // 2 is the only number divisible by the number before it
            cout << 2 << "\n";
        } else {
            // choose n-1. Then intuitively, n isn't divisible by n-1
            // subtract: n - (n - 1) = 1.
            cout << 1 << "\n";
        }
    }
}