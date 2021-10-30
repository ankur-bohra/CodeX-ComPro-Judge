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

        int untreated = 0;
        int recruits = 0;
        int i;
        for (int j=0; j<n; j++) {
            cin >> i;
            if (i==-1) {
                if (recruits > 0) {
                    recruits--;
                } else {
                    untreated++;
                }
            } else {
                recruits += i;
            }
        }
        cout << untreated << "\n";
    }
}