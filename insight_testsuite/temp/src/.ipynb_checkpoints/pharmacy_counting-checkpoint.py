"""
Generates a list of all drugs, the total number of UNIQUE individuals who prescribed the medication, and the total drug cost, which must be listed in descending order based on the total drug cost and if there is a tie, drug name (ascending order of drug_name).

"""

import csv
from itertools import groupby
import gc
import argparse


OUTPUT_HEADER = ["drug_name", "num_prescriber", "total_cost"]

def get_count_and_sum(drug_name, drugs_group):
    """Get Unique Count and Total Sum for a particular drug
    
    Args:
        drug_name: Name of the drug.
        drugs_group: Collection of records(dict) for the given drug_name
    Returns:
        A dict type with 'total_cost' (Total cost of that drug) and 'num_prescriber' (Number of unique prescribers)
    """

    unique_count = 0 # tracks unique count
    total_sum = 0 # tracks total sum
    
    null_count = 0
    total_count = 0
    
    unique_ids = set() # hashset for efficiency, maintains unique set of records

    for record in drugs_group:
        
        total_count += 1
        try:
            dc = float(record["drug_cost"]) if '.' in record["drug_cost"] else int(record["drug_cost"])
        
        except ValueError as e: # Handling NULL Values or Any Non Number value
            dc = 0
            null_count += 1
        
        total_sum += dc
        
        rid = record["id"]

        if rid not in unique_ids: # check if id of prescriber is unique
            unique_ids.add(rid)
            unique_count += 1

    avg_sum = total_sum // total_count
    
    total_sum = total_sum + avg_sum * null_count # NULL VALUES REPLACED WITH AVERAGE
    
    new_record = {"drug_name": drug_name,
                  "num_prescriber": unique_count,
                  "total_cost": total_sum}
    
    return new_record


def groupby_count_and_sum(data_path):
    """Reads a csv from the given path, groups by drug_name and returns unique count and total cost for each drug.
    
    Args:
        data_path: String path to input csv file (Example: "../input/de_cc_data.txt")
    Returns:
        A List type, where each element is a dictionary of format {"drug_name": NAME OF THE DRUG, 
                                                                   "num_prescriber": UNIQUE PRESCRIBER COUNT,                  
                                                                   "total_cost": TOTAL COST OF THAT DRUG}
    """
    new_records = []
    print("..reading input from {}".format(data_path))
    with open(data_path, newline='') as in_file:
        
        records = csv.DictReader(in_file) # Reader that maps the information read into a dict
        
        # Sort records based on drug_name, required for python groupby
        print("Sorting..")
        drug_sorted_records = sorted(records, key = lambda r: r["drug_name"])
        
        # Groups based on drugname
        print("Grouping..")
        drugs_key_group = groupby(drug_sorted_records, key = lambda r: r["drug_name"])
        del records, drug_sorted_records; gc.collect()    
        
        # iterate over groups
        print("Creating desired records..")
        for drug_name, drugs_group in drugs_key_group:
            result = get_count_and_sum(drug_name, drugs_group)
            new_records.append(result)
        
        # free some memory, remove useless data
        del drugs_key_group; gc.collect()
    
    return new_records


def main(input_filepath, output_filepath):
    """Reads I/P, count unique, sum cost, Writes O/P"""
    
    # get desired result of unique counts and total cost from data in the file
    new_records = groupby_count_and_sum(input_filepath)
    
    # stable sort in reverse order on total_cost, names are already sorted, breaks the tie
    new_records = sorted(new_records, key = lambda r: r["total_cost"], reverse=True)
    
    # write records
    print("..writing output to {}".format(output_filepath))
    with open(output_filepath, 'w') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=OUTPUT_HEADER)
        writer.writeheader()
        
        for record in new_records:
            writer.writerow(record)

        print("Finished!")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Pharmacy Counting Problem: Input and Output Paths..')
    
    parser.add_argument('input_filepath', metavar='INPUT',
                        type=str, help='path to input csv file')
    parser.add_argument('output_filepath', metavar='OUTPUT', 
                        type=str, help='path to input csv file')
    
    
    args = parser.parse_args()
    main(args.input_filepath, args.output_filepath)
