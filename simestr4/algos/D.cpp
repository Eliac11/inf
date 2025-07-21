#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>

using namespace std;

const int MOD = 1e9 + 7;

int main() {
    int n, m, k, l;
    cin >> n >> m >> k >> l;
    
    vector<bool> accepting(n + 1, false);
    for (int i = 0; i < k; i++) {
        int state;
        cin >> state;
        accepting[state] = true;
    }

    vector<vector<int>> transitions(n + 1, vector<int>(26, -1));

    for (int i = 0; i < m; i++) {
        int a, b;
        char c;
        cin >> a >> b >> c;
        transitions[a][c - 'a'] = b; 
    }

    vector<vector<long long>> dp(l + 1, vector<long long>(n + 1, 0));
    dp[0][1] = 1;

    for (int i = 0; i < l; i++) {
        for (int state = 1; state <= n; state++) {
            if (dp[i][state] > 0) {
                for (int ch = 0; ch < 26; ch++) {
                    int next = transitions[state][ch];
                    if (next != -1) {
                        dp[i + 1][next] = (dp[i + 1][next] + dp[i][state]) % MOD;
                    }
                }
            }
        }
    }

    long long result = 0;
    for (int state = 1; state <= n; state++) {
        if (accepting[state]) {
            result = (result + dp[l][state]) % MOD;
        }
    }

    cout << result << endl;

    return 0;
}