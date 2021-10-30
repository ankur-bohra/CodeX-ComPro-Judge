#include <bits/stdc++.h>
using namespace std;

int main() {
    // freopen("INPUT.txt", "r", stdin);
    // freopen("ANSWER.txt", "w", stdout);
    int T;
    cin >> T;

    while (T--) {
        int n,t;
        cin >> n >> t;
    
        string queue;
        cin >> queue;

        // Iterate over queue t times
        for (int i=0; i<t; i++) {
            for (int j=0; j<n-1; j++) {
                if (queue[j] == 'B' && queue[j+1] == 'G') {
                    // Replace students
                    queue[j] = 'G';
                    queue[j+1] = 'B';
                    // Skip the next index since we moved the boy there.
                    j++;
                }
            }
        }
        cout << queue << "\n";
    }
}