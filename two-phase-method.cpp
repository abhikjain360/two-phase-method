#include <iostream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string str;
    stringstream stream(str);

    //Objective function
    vector<int> Z;

    //taking objective function as input
    cout << "Enter the objective function : ";
    getline(cin, str);
    while (stream >> str)
        Z.push_back(stoi(str));

    
    return 0;
}