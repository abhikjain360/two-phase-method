import numpy as np
import matplotlib.pyplot as plt


# method to calculate the profit
def calculateProfit(table, Z, basic_coeff, total_count):
    P = []
    table = np.transpose(table)
    for i in range(total_count):
        Q = 0
        for j in range(len(basic_coeff)):
            Q += basic_coeff[j] * table[i][j]
        P.append(Z[i] - Q)
    
    return np.array(P)


# method to check optimality condition for simplex method
def optimalCondition(P, choice):
    if choice == 'min':
        for i in P:
            if i < 0:
                return True
        return False
    else:
        for i in P:
            if i > 0:
                return True
        return False
    

# method to perform Gauss-Jordan Elimination on the simplex table
def gauss_jordan_elimination(table, row_index, column_index):
    
    # first converting the coefficient to 1
    table[row_index] = table[row_index]/table[row_index][column_index]

    # eliminating from rest of the constraints
    for i in range(row_index):
        table[i] -= table[row_index] * table[i][column_index]
    
    for i in range(row_index+1, len(table)):
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
            inequalities[i] *= -1
            B[i] *= -1
            a_count_1 += 1
            S_coeff[i] = -1
    
    a_count = a_count_1 + a_count_2

    # count of all variables introduced seperately
    extra_count = a_count + S_count

    # padding equations with zeroes for new variables
    Z = np.pad(Z, (0, S_count), 'constant', constant_values=0)
    if n1 != 0:
        inequalities = np.pad(inequalities, ((0,0), (0,extra_count)), 'constant', constant_values=0)
    
    if n2 != 0:
        equalities = np.pad(equalities, ((0,0), (0,extra_count)), 'constant', constant_values=0)

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
            basic_index.append(temp)
            temp += 1
        else:
            basic_index.append(var_count + i)

    # adding artificial variables to equalities
    for i in range(n2):
        equalities[i][var_count + n1 + a_count_1 + i] = 1
        basic_index.append(var_count + n1 + a_count_1 + i)

    # generating the simplex table
    if n1 == 0:
        table = equalities
    elif n2 == 0:
        table = inequalities
    else:
        table = np.append(inequalities, equalities, axis=0)
    B = np.reshape(B, (n1+n2, 1))
    table = np.append(table, B, axis=1)
    table = table.astype('float')

    '''
    phase 1
    '''

    # objective function for phase 1
    Z_ = np.zeros(var_count + S_count)
    Z_ = np.pad(Z_, (0, a_count), 'constant', constant_values=1)

    # getting coefficients for the basic variables
    for i in basic_index:
        basic_coeff.append(Z_[i])

    # calculating profit initially
    P = calculateProfit(table, Z_, basic_coeff, extra_count+var_count)

    print(table)
    print(P)

    # applying simplex method repititively
    while optimalCondition(P, 'min'):

        # getting the entering variable
        # no need to worry about positive profit
        # as already eliminated in looping condition
        column_index = np.argmin(P)

        T = table.transpose()

        # calculating the ratios
        ratios = np.divide(T[-1],T[column_index])

        # finding the leaving variable
        row_index = -1
        temp = max(ratios) + 1
        for i in range(n1 + n2):
            if ratios[i] > 0 and temp > ratios[i]:
                temp = ratios[i]
                row_index = i

        # changing the list of basic variables
        basic_index[row_index] = column_index
        basic_coeff[row_index] = Z_[column_index]

        # when no leaving variable is found
        if row_index == -1:
            print("No Solutions!!")
            exit(0)
        
        table = gauss_jordan_elimination(table, row_index, column_index)
        
        P = calculateProfit(table, Z_, basic_coeff, extra_count+var_count)
        print(table)
        print(P)

    # in case artificial variables are not eliminated
    for i in range(var_count+S_count, var_count+extra_count):
        if i in basic_index:
            print(table)
            print(P)
            print("Artificial Variables can't be eliminated!\nNo Solution!!")
            exit(0)

        print(table)
        print(P)


    '''
    phase 2
    '''

    # removing all artificial variables from table
    B = table[:, -1]
    B = B.reshape((n1+n2, 1))
    table = table[:, :-a_count-1]
    table = np.append(table, B, axis=1)

    # getting coefficients for the basic variables
    for i in range(n1+n2):
        basic_coeff[i] = Z[basic_index[i]]

    # calculating profit initially
    P = calculateProfit(table, Z, basic_coeff, S_count+var_count)

    print(table)
    print(P)

    # applying simplex method repititively
    while optimalCondition(P, 'max'):

        # getting the entering variable
        # no need to worry about positive profit
        # as already eliminated in looping condition
        column_index = np.argmax(P)

        T = table.transpose()

        # calculating the ratios
        ratios = T[-1]/T[column_index]
        # finding the leaving variable
        row_index = -1
        temp = max(ratios) + 1
        for i in range(n1 + n2):
            if ratios[i] > 0 and temp > ratios[i]:
                temp = ratios[i]
                row_index = i

        # changing the list of basic variables
        basic_index[row_index] = column_index
        basic_coeff[row_index] = Z[column_index]

        # when no leaving variable is found
        if row_index == -1:
            print("No Solutions!!")
            exit(0)
        
        table = gauss_jordan_elimination(table, row_index, column_index)
        
        P = calculateProfit(table, Z, basic_coeff, S_count+var_count)

        print(table)
        print(P)
        print(basic_index)