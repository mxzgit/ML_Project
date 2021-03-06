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
#define MAX_NUM 63497
#define MAX_LEN 300
#define OF 
ll gcd(ll a, ll b) {return b == 0 ? a : gcd(b, a % b);}
ll lcm(ll a, ll b) {return a * (b / gcd(a, b));}
inline float min3(float x,float y,float z){return min(x,min(y,z));}	
// hash function for the pairs of int
#define mph(i,j) ( ll(i)*MAX_NUM + j )

unordered_map<ll,float> dists;
bool del[MAX_NUM];
bool in_storage[MAX_NUM];
float _DP_ROLL[2][MAX_LEN];
float dis[8][8];
int total_dp_call = 0;

float dp_rolling_ed(string s1,string s2)
{
	if(++total_dp_call % 1000000 == 0){
		cerr<<"DP: "<<total_dp_call<<endl;
		cerr.flush();
	}
	int sz1 = s1.size();
	int sz2 = s2.size();
	float cost = 0;
	for (int i=0;i<=sz2;i++)
		_DP_ROLL[0][i] = float(i);
	
	for (int i=1 ; i<=sz1 ; i++)
	{
		_DP_ROLL[i % 2][0] = float(i);
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

vi bayesianReduction(vector<string> X,vi y)
{
	int m = X.size();
	int mid = m/2;
	vi S1,S2,XX;
	
	for (int i=0;i<m;i++)
		XX.pb(i);
    random_shuffle(XX.begin(),XX.end());
	for (int i=0;i<mid;i++)
		S1.pb(XX[i]);
	for (int i=mid;i<m;i++)
		S2.pb(XX[i]);

    bool converged = false;
    int rounds = 0;
	
    while (!converged)
	{
        converged = true;
        rounds += 1;
        
        for (int ii=0; ii < S1.size();ii++)
		{
			int i = S1[ii];
            int predindex = -1;
            float mindist = OO;
            
            for (int jj=0; jj < S2.size() ; jj++)
			{
				int j = S2[jj];
				unordered_map<ll,float>::iterator it = dists.find(mph(i,j));
                if (it == dists.end()){
                    float ij_dis = dp_rolling_ed(X[i], X[j]);
					dists.insert(mp(mph(i,j),ij_dis));
					it = dists.insert(mp(mph(j,i),ij_dis)).first;
				}
                if (it->second < mindist)
                    predindex = j, mindist = it->second;
			}
            if (y[i] != y[predindex]){
                converged = false;
				int tmp_sz = S1.size();
				S1[ii] = S1[tmp_sz-1];
				S1.pop_back();
				ii--;
			}
        }
		
		if(rounds == 1){
			cerr<<"half first round is done!\n";
			cerr.flush();
		}
        
        for (int jj=0; jj < S2.size();jj++)
		{
			int j = S2[jj];
            int predindex = -1;
            float mindist = (1 << 30);
            
            for (int ii=0; ii < S1.size();ii++)
			{
				int i = S1[ii];
				unordered_map<ll,float>::iterator it = dists.find(mph(i,j));
                if (it == dists.end()){
                    float ij_dis = dp_rolling_ed(X[i], X[j]);
					dists.insert(mp(mph(i,j),ij_dis));
					it = dists.insert(mp(mph(j,i),ij_dis)).first;
				}
                if (it->second < mindist)
                    predindex = i, mindist = it->second;
			}
			if (y[j] != y[predindex]){
                converged = false;
				int tmp_sz = S2.size();
				S2[jj] = S2[tmp_sz-1];
				S2.pop_back();
				jj--;
			}
        }
		
		if(rounds == 1){
			cerr<<"first round is done!\n";
			cerr.flush();
		}
		
	}
	
	vi ret_ind;
	for (int i=0;i<S1.size();i++)
			ret_ind.pb(S1[i]);
	for (int i=0;i<S2.size();i++)
			ret_ind.pb(S2[i]);
	sort(ret_ind.begin(),ret_ind.end());
	cerr<<"ret_ind: "<<ret_ind.size()<<endl;
	return ret_ind;
}

// pop function for the sparse sets
void swap_pop(vi& vec,int idx)
{
	int sz = vec.size();
	if (!sz)
		return;
	vec[idx] = vec[sz-1];
	vec.pop_back();
}

vi condensedNN(vector<string> X,vi y,vi ind)
{
	memset(in_storage,0,sizeof in_storage );
    int m = ind.size();
    vi storage;
	storage.pb(ind[0]);
	in_storage[ind[0]] = 1;
	swap_pop(ind,0);
	
    bool converged = false;
    while (!converged)
	{
		converged = true;
        for(int ii=0; ii<ind.size() ; ii++)
		{
			int i = ind[ii];
            if( !in_storage[i])
			{
                int predindex = -1;
                float mindist = (1<<30);
                for (int jj = 0; jj< storage.size(); jj++)
				{
					int j = storage[jj];
					unordered_map<ll,float>::iterator it = dists.find(mph(i,j));
					if (it == dists.end()){
						float ij_dis = dp_rolling_ed(X[i], X[j]);
						dists.insert(mp(mph(i,j),ij_dis));
						it = dists.insert(mp(mph(j,i),ij_dis)).first;
					}
					if (it->second < mindist)
						predindex = j, mindist = it->second;
					
				}
                if (y[i] != y[predindex])
				{
					storage.pb(i);
					converged = false; 
					in_storage[i] = 1;
					swap_pop(ind,ii); 
					ii--;
				}
			}
			else{
				cerr<<"This should never be executed!\n";
				exit(1);
			}
		}
	}
	
	sort(storage.begin(),storage.end());
    return storage;
}

int main(int argc, char** argv)
{
	cerr<<"start\n";
	cerr.flush();
	fastio;
	const int test_sz = 10000;
	for (int i=0; i<8 ; i++)
		for (int j=0; j<8 ; j++)
			dis[i][j] = float(min(abs(i - j), min(i, j) + 8 - max(i, j))) * 0.5;
		
	freopen("data/train_code_with_GANs.txt","r",stdin);
	
	string s;
	vector<string> X_train,X_test;
	
	for(int i=0;i<MAX_NUM;i++)
	{
		cin>>s;
		for (int j=0;j<s.size();j++)
			s[j] = int(s[j]) - int('0');
		X_train.pb(s);
	}
		
	cerr<<"size X_train "<<X_train.size()<<endl;
		
	freopen("data/test_code.txt","r",stdin);
	
	for(int i=0; i < test_sz ; i++)
	{
		cin>>s;
		for (int j=0;j<s.size();j++)
			s[j] = int(s[j]) - int('0');
		X_test.pb(s);		
	}
	
	cout<<"size X_test "<<X_test.size()<<endl;
	
	freopen("train_test_dis_array_GANs_no_reduce.txt","w",stdout);
	
	for(int i = 0; i<MAX_NUM;i++)
	{
		for (int j=0;j<test_sz;j++){
			if(j)
				cout<<',';
			cout<<dp_rolling_ed(X_train[i],X_test[j]);
		}
		cout<<'\n';
	}
	
    
}
