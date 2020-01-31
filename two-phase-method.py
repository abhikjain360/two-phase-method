import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__' :

    '''
    taking input and initializing
    '''

    # taking the objective function as input
    print('Enter the Objective Function Z : ', end='')
    Z = list(map(int, input().split()))
    var_count = len(Z)

    # array for constraints
    inequalities = []
    equalities = []

    # the RHS values/solution column
    B = []

    #initializing the number-of-constraints
    n1, n2 = 0, 0

    # taking inequalities LHS
    print("Enter the number of inequalities : ", end='')
    n1 = int(input())

    print("Enter LHS of inequalities in less-than form : ")
    for i in range(n1):
        inequalities.append(list(map(int, input().split())))

    # taking inequalities RHS
    print("Enter RHS of inequalties : ")
    for i in range(n1):
        B.append(int(input()))
    
    # taking equalities LHS
    print("Enter the number of equalities : ", end='')
    n2 = int(input())

    print("Enter the LHS equalities : ")
    for i in range(n2):
        equalities.append(list(map(int ,input().split())))
    
    # taking equalities RHS
    print("Enter the RHS of inequalities : ")
    for i in range(n2):
        B.append(int(input()))

    equalities = np.array(equalities)
    inequalities = np.array(inequalities)
    B = np.array(B)

    '''
    changing constraints in standard form
    '''
    # count of slack/surplus and artificial variables
    S_count = n1
    a_count_2 = n2
    a_count_1 = 0

    # coefficient of slack/surplus variable in constraints
    S_coeff = np.ones(n1)

    for i in range(n1):
        if B[i] < 0:
            a_count_1 += 1
            S_coeff[i] = -1
    
    a_count = a_count_1 + a_count_2

    # count of all variables introduced seperately
    extra_count = a_count_1 + a_count_2 + S_count

    # padding equations with zeroes for new variables
    Z = np.pad(Z, (0, S_count), 'constant', constant_values=0)
    Z_ = np.zeros(var_count)
    Z_ = np.pad(Z_, (0, a_count), 'constant', constant_values=1)

    inequalities = np.pad(inequalities, ((0,0), (0,extra_count)), 'constant', constant_values=0)
    equalities = np.pad(equalities, ((0,0), (0,extra_count)), 'constant', constant_values=0)

    temp = var_count + n1

    # adding extra variables to inequalities
    for i in range(n1):
        inequalities[i][var_count] = S_coeff[i]
        if S_coeff[i] == -1:
            inequalities[i][temp] = 1
            temp += 1

    # adding extra variables to equalities
    for i in range(n2):
        equalities[i][var_count + n1 + a_count_1 + i] = 1

    