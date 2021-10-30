#include <bits/stdc++.h>
using namespace std;

#define ll long long

int main() {
    freopen("INPUT.txt", "r", stdin);
    freopen("OUTPUT.txt", "w", stdout);
    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;
    
        if (n==0 || n==1) {
            cout << 1 << "\n";
        } else {
            // m = minus
            ll f_im1 = 1;
            ll f_im2 = 1;
            /*
            fᵢ = fᵢ₋₁ + fᵢ₋₂. The i-th element is at position i-1.
            */
            for (ll i = 2; i < (ll)n; i++) {
                ll f_i = f_im1 + f_im2;
                // Change values for next iteration
                f_im2 = f_im1;
                f_im1 = f_i;
            }
            cout << f_im1 << "\n";
        }
    }
}