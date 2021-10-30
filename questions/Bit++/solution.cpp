#include <bits/stdc++.h>
using namespace std;

int main() {
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;

        int x = 0;
        while (n--) {
            string statement;
            cin >> statement;
            /*
            ++ or -- is *one* operation, so a statement can be of the format ++x, x++, --x or x--.
            For each statement, the second character is enough to infer the operation.
            */
            if (statement[1] == '+') {
                x++;
            } else {
                x--;
            }
        }
        cout << x << "\n";
    }
}