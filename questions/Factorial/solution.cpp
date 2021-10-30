#include <bits/stdc++.h>
using namespace std;

int main() {
    // freopen("INPUT.txt", "r", stdin);
    // freopen("OUTPUT.txt", "w", stdout);
    int T;
    cin >> T;
    
    while (T--) {
        long long n;
        cin >> n;
    
        /*
        n! = n * n-1 * n-2 * ... * 1
        Multiply each number from n-1 to 1 (inclusive) successively.
        */
        for (long long i=n-1; i>0; i--) {
            n *= i;
        }
        cout << n << "\n";
    }
}