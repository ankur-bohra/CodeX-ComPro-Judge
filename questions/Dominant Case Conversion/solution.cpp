#include <bits/stdc++.h>
using namespace std;

int main() {
    // freopen("INPUT.txt", "r", stdin);
    // freopen("OUTPUT.txt", "w", stdout);
    int T;
    cin >> T;
    while (T--) {
        string word;
        cin >> word;
        // Letters can be either uppercase or lowercase, counting one allows us to calculate the other.
        // lowercase letters = total letters - uppercase letters
        int upper = 0;
        for (int i=0; i<word.size(); i++) {
            if (isupper(word[i])) {
                upper++;
            }
        }

        for (int i=0; i<word.size(); i++) {
            /*
            If the number of uppercase characters is strictly greather than the number of lowercase 
            characters (total - upper), then the string is neither lowercase dominant and neither is
            the number of lowercase characters = uppercase characters
            */
            if (upper > word.size() - upper) {
                word[i] = toupper(word[i]);
            } else {
                // The word is either lowercase dominant or lowercase = uppercase, either way convert
                // to lowercase
                word[i] = tolower(word[i]);
            }
        }
        cout << word << "\n";
    }
}