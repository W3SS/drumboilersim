#include <bits/stdc++.h>

using namespace std;

/*
 * Programa para transformar as tabelas copiadas de outros trabalhos
 * para lists lidas pelo script de testes do Python
 */

int main(){
  double P, T, h, D, dummy;

  bool agua = 1;
  
  vector<double> Ps, Ts;
  vector<double> h_ls, D_ls;
  vector<double> h_gs, D_gs;

  while(cin >> P >> T >> dummy >> h >> D){
    if(agua){
      Ps.push_back(P/1e6); Ts.push_back(T);

      h_ls.push_back(h);
      D_ls.push_back(D);
    }    
    else{
      h_gs.push_back(h);
      D_gs.push_back(D);
    }
    agua = !agua;
  }
  bool first;
  
  cout << "Ps= [";
  first = 1;
  for(size_t i = 0; i < Ps.size(); i++){
    if(!first) cout << ", ";
    first = 0;
    cout << Ps[i];
  }
  cout << "]\n";
  
  cout << "T_sats = [";
  first = 1;
  for(size_t i = 0; i < Ps.size(); i++){
    if(!first) cout << ", ";
    first = 0;
    cout << Ts[i];
  }
  cout << "]\n";
  
  cout << "h_ls = [";
  first = 1;
  for(size_t i = 0; i < Ps.size(); i++){
    if(!first) cout << ", ";
    first = 0;
    cout << h_ls[i];
  }
  cout << "]\n";
  
  cout << "D_ls = [";
  first = 1;
  for(size_t i = 0; i < Ps.size(); i++){
    if(!first) cout << ", ";
    first = 0;
    cout << D_ls[i];
  }
  cout << "]\n";

  
  cout << "h_gs = [";
  first = 1;
  for(size_t i = 0; i < Ps.size(); i++){
    if(!first) cout << ", ";
    first = 0;
    cout << h_gs[i];
  }
  cout << "]\n";

  
  cout << "D_gs = [";
  first = 1;
  for(size_t i = 0; i < Ps.size(); i++){
    if(!first) cout << ", ";
    first = 0;
    cout << D_gs[i];
  }
  cout << "]";
}
