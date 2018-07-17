# Table of Contents

1.  [Problem](README.md#problem)
2.  [Solution](README.md#solution)

# Problem

Generate a list of all drugs, the total number of UNIQUE individuals who prescribed the medication, and the total drug cost, which must be listed in descending order based on the total drug cost and if there is a tie, drug name(Ascending Order).

# Solution

1.  _Distinct Count individuals who prescribed the medication:_ Grouping on drug_name, counting unique individuals (based on their id) using hashset to check uniqueness. Used python's groupby() function from itertools package for efficient looping.

2.  _Total cost per drug:_ Sum up costs for grouped data in the previous step. Null values and other noise is handled by filling in with the average.

Note: The total sum might not matchup exactly with true value if the values are floats, compare by having a tolerance or rounding the decimals.

# Instructions

`python3 ./src/pharmacy_counting.py ./input/itcont.txt ./output/top_cost_drug.txt`

# Output

Your program needs to create the output file, `top_cost_drug.txt`, that contains comma (`,`) separated fields in each line.

Each line of this file should contain these fields:

-   drug_name: the exact drug name as shown in the input dataset
-   num_prescriber: the number of unique prescribers who prescribed the drug. For the purposes of this challenge, a prescriber is considered the same person if two lines share the same prescriber first and last names
-   total_cost: total cost of the drug across all prescribers

For example

If your input data, **`itcont.txt`**, is

    id,prescriber_last_name,prescriber_first_name,drug_name,drug_cost
    1000000001,Smith,James,AMBIEN,100
    1000000002,Garcia,Maria,AMBIEN,200
    1000000003,Johnson,James,CHLORPROMAZINE,1000
    1000000004,Rodriguez,Maria,CHLORPROMAZINE,2000
    1000000005,Smith,David,BENZTROPINE MESYLATE,1500

then your output file, **`top_cost_drug.txt`**, would contain the following lines

    drug_name,num_prescriber,total_cost
    CHLORPROMAZINE,2,3000
    BENZTROPINE MESYLATE,1,1500
    AMBIEN,2,300
