import numpy as np
import matplotlib.pyplot as plt


# method to calculate the profit
def calculateProfit(table, Z, basic_coeff, total_count):
    P = []
    table = np.transpose(table)
    for i in range(total_count):
        print(Z[i] - basic_coeff * table[i])
        P.append(Z[i] - basic_coeff * table[i])
    
    return P


# method to perform Gauss-Jordan Elimination on the simplex table
def gauss_jorad_elimination(table, row_index, column_index):
    
    # first converting the coefficient to 1
    table[row_index] /= table[row_index][column_index]

    # eliminating from rest of the constraints
    for i in range(len(table)):
        table[i] -= table[row_index] * table[i][column_index]

    return table


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

    if n1 != 0:
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

    if n2 != 0:
        print("Enter the LHS equalities : ")
        for i in range(n2):
            equalities.append(list(map(int ,input().split())))
    
        # taking equalities RHS
        print("Enter the RHS of inequalities : ")
        for i in range(n2):
            B.append(int(input()))

    if n1 == 0 and n2 == 0:
        print("No constraints entered!!")
        exit(0)
    
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

    if n1 != 0:
        inequalities = np.pad(inequalities, ((0,0), (0,extra_count)), 'constant', constant_values=0)
    
    if n2 != 0:
        equalities = np.pad(equalities, ((0,0), (0,extra_count)), 'constant', constant_values=0)

    Z = np.pad(Z, (0, S_count), 'constant', constant_values=0)

    # to keep track of index of basic variables and their coefficients
    basic_index = []
    basic_coeff = []

    # variable to add artificial variables in case of surplus variables
    temp = var_count + n1

    # adding extra variables to inequalities
    for i in range(n1):
        inequalities[i][var_count + i] = S_coeff[i]
        if S_coeff[i] == -1:
            inequalities[i][temp] = 1
            temp += 1
        else:
            basic_index.append(var_count + i)

    # adding extra variables to equalities
    for i in range(n2):
        equalities[i][var_count + n1 + a_count_1 + i] = 1
        basic_index.append(var_count + n1 + a_count_1 + i)

    # getting coefficients for the basic variables
    for i in basic_index:
        basic_coeff.append(Z[i])

    # generating the simplex table
    if n1 == 0:
        table = equalities
    elif n2 == 0:
        table = inequalities
    else:
        table = np.append(inequalities, equalities, axis=0)
        B = np.reshape(B, (extra_count, 1))
        table = np.append(table, B, axis=1)

    '''
    phase 1
    '''

    # objective function for phase 1
    Z_ = np.zeros(var_count + S_count)
    Z_ = np.pad(Z_, (0, a_count), 'constant', constant_values=1)

    # calculating profit
    P = calculateProfit(table, Z_, basic_coeff, extra_count+var_count)

    # list to compare profit to
    all_true = np.ones(var_count+extra_count, dtype=bool)

    while (P >= 0) != all_true:

        # getting the entering variable
        # no need to worry about positive profit
        # as already eliminated in looping condition
        column_index = np.argmin(P)

        # calculating the ratios
        ratios = table[column_index]/table[-1]

        # finding the leaving variable
        row_index = -1
        temp = max(ratio)
        for i in range(n1 + n2):
            if ratios[i] > 0 and temp > ratios[i]:
                temp = ratios[i]
                row_index = i

        # when no leaving variable is found
        if row_index == -1:
            print("No Solutions!!")
            exit(0)
        
        table = gauss_jorad_elimination(table, row_index, column_index)
        
        P = calculateProfit(table, Z_, basic_coeff, extra_count+var_count)
