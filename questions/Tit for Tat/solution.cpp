#include <bits/stdc++.h>
using namespace std;

int main() {
    // freopen("INPUT.txt", "r", stdin);
    // freopen("ANSWER.txt", "w", stdout);
    int t;
    cin >> t;

    for (int c=0; c<t; c++) {
        int n,k;
        cin >> n >> k;
        int arr[n];
        cin >> arr[0];
        int num;
        char ch;
        for (int i=1; i<n; i++) {
            cin >> num;
            arr[i] = num;
        }

        /*
        We know we have to take from the starting of the array to make the array lexicographically
        smaller. In doing this we must not increase elements we might reach at the end of the operations,
        hence the safest bet to increase the array is to always add to the last element.
        */
        int ptr=0;
        while (k>0 && ptr<n-1) {
            if (arr[ptr] == 0) {
                ptr++;
                continue;  // Recheck for next index
            }
            arr[ptr]--;
            arr[n-1]++;
            k--;
        }

        for (int i=0; i<n; i++) {
            cout << arr[i] << " ";
        }
        cout << "\n";
    }
}