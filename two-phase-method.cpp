#include <iostream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

int main() 
{
    //Objective function
    vector<int> Z;

    //taking objective function as input
    string str;
    cout << "Enter the objective function : ";
    getline(cin, str);
    stringstream stream(str);
    while (stream >> str)
        Z.push_back(stoi(str));

    
    return 0;
}