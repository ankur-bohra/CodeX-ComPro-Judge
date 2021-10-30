#include <bits/stdc++.h>
using namespace std;

int main() {
    freopen("INPUT.txt", "r", stdin);
    freopen("ANSWER.txt", "w", stdout);
    int T;
    cin >> T;

    while (T--) {
        int n,k;
        cin >> n >> k;

        int piles[n];
        for (int i=0; i<n; i++) {
            cin >> piles[i];
        }

        /*
        If we use only the smallest pile as i, we maximize the number of spells we can apply on all
        other piles. The order of which pile hits its limit first doesn't matter, only that the
        smallest pile is used to do so and that it is preserved for other piles.
        */
        int ptr = 1;
        int smallest_pile_h = *min_element(piles, piles+n);
        int smallest_pile_index = distance(piles, find(piles, piles+n, smallest_pile_h));
        int spells_cast = 0;
        for (int i=0; i<n; i++) {
            if (i != smallest_pile_index) { // Preserve smallest pile
                int new_pile_h = piles[i] + smallest_pile_h;
                while (new_pile_h <= k) {
                    piles[i] = new_pile_h;
                    spells_cast++;
                    // For next iteration
                    new_pile_h += smallest_pile_h;
                }
            }
        }
        cout << spells_cast << "\n";
    }
}