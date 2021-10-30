#include <bits/stdc++.h>
using namespace std;

int main() {
    freopen("INPUT.txt", "r", stdin);
    freopen("ANSWER.txt", "w", stdout);
    int t;
    cin >> t;

    while (t--) {
        int n, k;
        cin >> n >> k;

        int a[n], b[n];
        for (int i=0; i<n; i++) {
            cin >> a[i];
        }
        for (int i=0; i<n; i++) {
            cin >> b[i];
        }

        /*
        To maximize the sum in a, we need to replace the smallest numbers in a with the largest
        numbers in b.
        If both are sorted in ascending order, we need to pick off numbers from the end of b to
        the start of a.
        */
        sort(a, a+n);
        sort(b, b+n);

        int ptr_a=0, ptr_b=n-1;
        while (ptr_a<n && ptr_b<n && k--) {
            if (a[ptr_a] < b[ptr_b]) {
                a[ptr_a] = b[ptr_b];
                ptr_a++;
            }
            ptr_b--;
        }

        int sum = 0;
        for (int i=0; i<n; i++) {
            sum += a[i];
        }

        cout << sum << "\n";
    }
}