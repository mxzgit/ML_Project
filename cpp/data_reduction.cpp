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
#define MAX_NUM 1000
#define MAX_LEN 70
#define OF 
ll gcd(ll a, ll b) {return b == 0 ? a : gcd(b, a % b);}
ll lcm(ll a, ll b) {return a * (b / gcd(a, b));}

double dists[MAX_NUM][MAX_NUM];
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
	if(++total_dp_call % 1000 == 0){
		cout<<"DP: "<<total_dp_call<<endl;
		cout.flush();
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

vi bayesianReduction(vector<string> X,vi y)
{
	int m = X.size();
	int mid = m/2;
	vi S1,S2,XX;
	for (int i=0;i<m;i++)
		XX.pb(i);
    random_shuffle(XX.begin(),XX.end());
	for (int i=0;i<mid;i++){
		S1.pb(XX[i]);
		//cout<<XX[i]<<' ';
	}
	//cout<<'\n';
	for (int i=mid;i<m;i++){
		S2.pb(XX[i]);
		//cout<<XX[i]<<' ';
	}
	//cout<<'\n';
    bool converged = false;
    int rounds = 0;
	
    while (!converged)
	{
        converged = true;
        rounds += 1;
        
        for (int ii=0; ii < S1.size();ii++)
		{
			//if(ii%100==0)
			//	cout<<ii<<endl;
			int i = S1[ii];
            int predindex = -1;
            double mindist = OO;
            
            for (int jj=0; jj < S2.size() ; jj++)
			{
				int j = S2[jj];
                if (dists[i][j] < 0)
                    dists[i][j] = dists[j][i] = dp_rolling_ed(X[i], X[j]);
                if (dists[i][j] < mindist)
                    predindex = j, mindist = dists[i][j];
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
			cout<<"half first round is done!\n";
			cout.flush();
		}
        
        for (int jj=0; jj < S2.size();jj++)
		{
			int j = S2[jj];
            int predindex = -1;
            double mindist = (1 << 30);
            
            for (int ii=0; ii < S1.size();ii++)
			{
				int i = S1[ii];
                if (dists[i][j] < 0)
                    dists[i][j] = dists[j][i] = dp_rolling_ed(X[i], X[j]);
                if (dists[i][j] < mindist)
                    predindex = i, mindist = dists[i][j];
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
			cout<<"first round is done!\n";
			cout.flush();
		}
		
	}
	
	vi ret_ind;
	for (int i=0;i<S1.size();i++)
			ret_ind.pb(S1[i]);
	for (int i=0;i<S2.size();i++)
			ret_ind.pb(S2[i]);
	sort(ret_ind.begin(),ret_ind.end());
	cout<<"ret_ind: "<<ret_ind.size()<<endl;
	return ret_ind;
}

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
			//if(ii%100==0)
			//	cout<<ii<<endl;
			int i = ind[ii];
            if( !in_storage[i])
			{
                int predindex = -1;
                double mindist = (1<<30);
                for (int jj = 0; jj< storage.size(); jj++)
				{
					int j = storage[jj];
                    if (dists[i][j] == -1)
                        dists[i][j] = dists[j][i] = dp_rolling_ed(X[i], X[j]);
                    if (mindist > dists[i][j])
                        predindex = j, mindist = dists[i][j];
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
				cout<<"baaaaaaaaaad\n";
				exit(1);
			}
		}
	}
	
	sort(storage.begin(),storage.end());
    return storage;
}

int main(int argc, char** argv)
{
	cout<<"start\n";
	cout.flush();
	for (int i=0; i<8 ; i++)
		for (int j=0; j<8 ; j++)
			dis[i][j] = double(min(abs(i - j), min(i, j) + 8 - max(i, j))) * 0.5;
		
	freopen("train_code_scaled_half.txt","r",stdin);
	for (int i=0;i<MAX_NUM ; i++)
		for (int j=0;j<MAX_NUM ; j++)
			dists[i][j] = -1;
	string s;
	vector<string> X;
	vi y;
	
	for(int i=0;i<MAX_NUM;i++)
	{
		cin>>s;
		for (int j=0;j<s.size();j++)
			s[j] = int(s[j]) - int('0');
		X.pb(s);
	}	
	cout<<"size X "<<X.size()<<endl;
    freopen("train_labels.txt","r",stdin);
	for(int i=0;i<MAX_NUM;i++)
	{
		int tmp;
		cin>>tmp;
		y.pb(tmp);
	}
	cout<<"size y "<<y.size()<<endl;
	cout<<"done reading\n";
	cout.flush();
    vi ind = bayesianReduction(X, y);
    cout<<"done bayesianReduction\n";
	cout.flush();
	ind = condensedNN(X, y, ind);
    cout<<"done condensedNN. Ind size: "<<ind.size()<<"\n";
	cout.flush();
	freopen("res.out","w",stdout);
    for(int i = 0;i < ind.size(); i++)
		cout<<ind[i]<<endl;
	cout.flush();
}
