#include <bits/stdc++.h>
using namespace std;

int main() {
    freopen("INPUT.txt", "r", stdin);
    freopen("ANSWER.txt", "w", stdout);

    int T;
    cin >> T;
    while (T--) {
        int n_cols, n_rows;
        cin >> n_rows >> n_cols;

        int image[n_rows][n_cols];

        // Fill the image
        string i;
        for (int row=0; row<n_rows; row++) {
            cin >> i; 
            for (int col=0; col<n_cols; col++) {
                image[row][col] = i[col];
            }
        }

        int faces = 0;
        /*
        Each 2x2 square must be checked. No 2x2 squares can be created if the top-left element of the
        square is on the right or bottom boundaries i.e. in the last column or row.
        */
        for (int i=0; i<n_rows-1; i++) {
            for (int j=0; j<n_cols-1; j++) {
                string letters;
                letters += image[i][j];
                letters += image[i+1][j];
                letters += image[i][j+1];
                letters += image[i+1][j+1];
                // Instead of maintaining some flag for each letter and checking each cell against each
                // letter, add all of them in any order and sort the string.
                sort(letters.begin(), letters.end());
                if (letters == "acef") { // Sorted order of face = acef
                    faces++;
                }
            }
        }
        cout << faces << "\n";
    }
}