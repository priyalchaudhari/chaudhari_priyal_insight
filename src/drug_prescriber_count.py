
# coding: utf-8

# In[1]:


import os
import glob
import csv
import operator
import sys


# In[2]:


def getSourceFileContent(sourceFileLocation):
    with open (sourceFileLocation,'r') as myfile:
        full_text = myfile.read().splitlines()
        text_list = [txt.split(',') for txt in full_text]
        return text_list


# In[3]:


def getTotalDrugCost(a):
    Drug_amount={}
    for i in a[1:]:
        if i[3] in Drug_amount:
            Drug_amount[i[3]]=int(Drug_amount[i[3]])+int(i[4])
        else:
            Drug_amount[i[3]]=i[4]
    return Drug_amount


# In[4]:


# Defining a function to compute the total number of unique prescribers of a particular drug
def getUniqueDrugPrescriberCount(b):
    no_of_cust={}
    drug_cust ={}
    for i in b[1:]:
        if i[3] in drug_cust:
            if i[1]+i[2] not in  drug_cust[i[3]]:
                drug_cust[i[3]].append(i[1]+i[2])
        else:
            drug_cust[i[3]] = []
            drug_cust[i[3]].append(i[1]+i[2])
    for x, y in drug_cust.items():
        no_of_cust.update({x:len(y)})
    return no_of_cust


# In[5]:


# Defining a function to combine the output of getUniqueDrugPrescriberCount() and getTotalDrugCost() function
def getUnsortedDrugPrescriberCountAndDrugCost(Drug_amount, drug_cust):
    unsorted_output = dict((k, [drug_cust[k], Drug_amount.get(k)]) for k in drug_cust)
    return unsorted_output


# In[6]:


# Defining a function to sort the result based on the total_cost of a drug
def getSortedDrugPrescriberCountAndDrugCost(unsorted_output):

    sorted_output = sorted(unsorted_output.items(), key=operator.itemgetter(0), reverse = True)

    sorted_output = [[x[0], x[1][0], x[1][1]] for x in sorted_output]

    sorted_output = [['drug_name', 'num_prescriber', 'total_cost']] + sorted_output
    
    return sorted_output


# In[7]:


# Defining a function to write the output to a file
def writeOutputFile(sorted_output,targetFileLocation):
    with open(targetFileLocation,"w") as f:
        wr = csv.writer(f)
        wr.writerows(sorted_output)


# In[8]:


# Defining a main() function which reads the input and output directory from the command line
# and calls all the above functions in sequence and creates output file

def main():
    
    user_input = sys.argv[1:]
    print("----Process Started----", '\n')
    counter = 0
    if len(user_input) == 0:
        print('No Input provided. Process is exiting!!')
        exit(0)
    for ip in user_input:
        if counter == 0:
            sourceFileLocation = str(ip)
        else:
            targetFileLocation = str(ip)
        counter += 1

    print('Reading the source file!!!', '\n')
    text_list = getSourceFileContent(sourceFileLocation)
    
    print('Getting the total cost of each prescribed drug!!!', '\n')
    Drug_amount = getTotalDrugCost(text_list)
    
    print('Getting the count of unique prescribers of each drug!!!', '\n')
    no_of_cust = getUniqueDrugPrescriberCount(text_list)
    
    print('Consolidating the Drug, it\'s unique prescriber count and total cost of the drug!!!', '\n')
    unsorted_output = getUnsortedDrugPrescriberCountAndDrugCost(no_of_cust, Drug_amount)
    
    print('Sorting the content based on total cost of the drug in descending order!!!', '\n')
    sorted_output = getSortedDrugPrescriberCountAndDrugCost(unsorted_output)
    
    print('Writing the content to the output file!!!', '\n')
    writeOutputFile(sorted_output,targetFileLocation)
    
    print('Process finished!!!')


# In[9]:


if __name__ == '__main__':
    main()

