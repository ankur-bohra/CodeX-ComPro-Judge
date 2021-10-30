#include <bits/stdc++.h>
using namespace std;

int main() {
    int T;
    cin >> T;

    while (T--) {
        int n, k;
        cin >> n >> k;

        int piles[n];
        for (int i=0; i<n; i++) {
            cin >> piles[i];
        }

        int spells_cast = 0;
        while (true) {
            int i = -1, j = -1;
            for (int a=0; a<n; a++) {
                if ((i == -1) || (piles[a] < piles[i])) {
                    i = a;
                }
            }
            for (int a=0; a<n; a++) {
                if ( ((j == -1) || (piles[a] < piles[j])) && (a != i)){
                    j = a;
                }
            }
            if (piles[i] + piles[j] <= k) {
                piles[j] += piles[i];
                spells_cast++;
            } else {
                break;
            }
        }
        cout << spells_cast << "\n";
    }
}