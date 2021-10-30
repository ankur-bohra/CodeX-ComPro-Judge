#include <bits/stdc++.h>
using namespace std;

int main() {
    freopen("INPUT.txt", "r", stdin);
    freopen("OUTPUT.txt", "w", stdout);
    int T;
    cin >> T;
    
    while (T--) {
        int n;
        cin >> n;
    
        string stones;
        cin >> stones;
    
        /*
        For n consecutive stones of the same colour, n-1 stones must be taken out from the end. One stone
        must be taken out of each pair.
        e.g.           o  x  x  x  x  x  o
                          |  |  | (x  x)
                          |  |  |  |  ^
                          |  | (x  x)
                          |  |  |  ^
                          | (x  x)
                          |  |  ^
                         (x  x)
                             ^
        */
        int taken = 0;
        for (int i=1; i<n; i++) {
            if (stones[i] == stones[i-1]) {
                taken++;
            }
        }
        cout << taken << "\n";
    }
}