#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    cin >> t;

    while (t--) {
        string s;
        cin >> s;

        /*
        1. There MUST be an even number of characters for a balanced string.
        2. There's only one ( and one ):
            Both on boundaries:
                (??...??)
                Clearly each ?? pair can be resolved to () to solve, or outermost ? ? can be
                resolved to ( ).
            Either on boundaries:
                ?(???) / (???)? (Odd number of ?s between brackets)
                Boundary ?s can be resolved to (/) based on side ( '(' for left, ')' for right).
                The closest ? to the boundary ? can be made to balance the new boundary bracket.
                All other pairs can now be solved as before.

                ??(??) / (??)?? (Even number of ?s between rackets)
                Each pair can be resolved.
            Neither on boundaries:
                Outermost resolved to (, ) and it can be simplied to the other cases.                 
        */
        if (s.size()%2==0 && s[0] != ')' && s.back() != '(') {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }
}