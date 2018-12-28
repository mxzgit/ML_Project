#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef unsigned long long ull;
typedef unsigned int uint;
typedef vector< int> vi;
typedef vector< vi> vvi;
typedef pair<int, int> pi;
typedef vector<pi > vpi;
typedef vector< vpi> vvpi;

#define mp  make_pair
#define pb  push_back
#define eps (1e-9)
#define iseq(a,b) (fabs(a-b)<eps)
#define readfile freopen("in.in","r",stdin)
#define readfiles readfile , freopen("out.out","w",stdout)
#define fastio ios::sync_with_stdio(false);
#define valid(i, t) (0 <= (i) && (i) < (t))
#define OO 0x7fffffff
#define MOD 1000000007
#define MAX_NUM 60000
#define MAX_LEN 300
#define OF 
ll gcd(ll a, ll b) {return b == 0 ? a : gcd(b, a % b);}
ll lcm(ll a, ll b) {return a * (b / gcd(a, b));}

bool del[MAX_NUM];
bool in_storage[MAX_NUM];

double _DP_ROLL[2][MAX_LEN];

double dis[8][8];
	
inline double min3(double x,double y,double z)
{
	return min(x,min(y,z));
}	
int total_dp_call = 0;

double dp_rolling_ed(string s1,string s2)
{
	if(++total_dp_call % 1000000 == 0){
		cerr<<"DP: "<<total_dp_call<<endl;
		cerr.flush();
	}
	int sz1 = s1.size();
	int sz2 = s2.size();
	double cost = 0;
	for (int i=0;i<=sz2;i++)
		_DP_ROLL[0][i] = double(i);
	
	for (int i=1 ; i<=sz1 ; i++)
	{
		_DP_ROLL[i % 2][0] = double(i);
		for (int j = 1 ; j <= sz2 ; j++)
		{
			if(s1[i - 1] == s2[j - 1])
				_DP_ROLL[i % 2][j] = _DP_ROLL[(i + 1) % 2][j - 1];
			else
			{
				if (min(_DP_ROLL[(i + 1) % 2][j], _DP_ROLL[i % 2][j - 1]) < _DP_ROLL[(i + 1) % 2][j - 1])
					cost = 1.0;
				else
					cost = dis[s1[i - 1]][s2[j - 1]];
				_DP_ROLL[i % 2][j] = cost + min3(_DP_ROLL[(i + 1) % 2][j], _DP_ROLL[i % 2][j - 1], _DP_ROLL[(i + 1) % 2][j - 1]);
			}
		}
	}
	return _DP_ROLL[sz1 % 2][sz2];
}

int main(int argc, char** argv)
{
	fastio;
	string s_test = string(argv[1]);
	for (int j=0;j<s_test.size();j++)
		s_test[j] = int(s_test[j]) - int('0');
	const int red_num =2661 ;
	
	for (int i=0; i<8 ; i++)
		for (int j=0; j<8 ; j++)
			dis[i][j] = double(min(abs(i - j), min(i, j) + 8 - max(i, j))) * 0.5;
	
	string s; int x;
	vector<string> X_train_reduced;
	vi Y_train_reduced;
	
	freopen("data/reduced_train.txt","r",stdin);
	for(int i=0;i<red_num;i++)
	{
		cin>>s;
		//cout<<s<<endl;
		//X_train_print.pb(s);
		for (int j=0;j<s.size();j++)
			s[j] = int(s[j]) - int('0');
		X_train_reduced.pb(s);
	}
	
	freopen("distance_res.txt","w",stdout);
	for(int i = 0; i<red_num;i++){
		if(i)
			cout<<' ';
		float d = dp_rolling_ed(s_test,X_train_reduced[i]);
		printf("%.6f", d);
	}
}
