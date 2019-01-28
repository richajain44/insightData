"""
This program takes in input file de_cc_data and outputs top_cost_drug.
It calculates for each drug its total unique count of prescribers and
total cost of each drug.

run.sh provides the necessary input and output paths
"""

#Importing necessary libraries
#sys is used for input and output reading
#csv is used to read the input file
import sys
import csv

#Function implementing the core functionalities of the program
#Input: input file i.e. de_cc_data
#Returns : Two dictonaries - count of unique prescribers for the each drug
# and total cost of each drug. 
#It also returns a list of lines which if could not be captured by the program
def costing_counting(input_file):
	prescribers={}#dictionary for unique count of prescribers
	cost_dict={}#dictionay for cost of each drug
	outlier=[] #list for capturing unhandled line
	with open(input_file,'rt') as f:
		next(f) #skip the header
		try:
			l = csv.reader(f,delimiter=',')
			for line in l:
				temp = set() #create a set which which only contain unique list of all the precribers
				
				#since the cost is in str convert it to float and then to int as the output is in interger
				cost = int(float(line[-1].rstrip())) 
				if line[3] not in cost_dict:
					cost_dict.update({line[3]:cost}) #add all the new entries to the dict
				else:
					cost_dict[line[3]]=cost_dict[line[3]]+cost #sum the new and the exisitng entry
            
				if line[3] not in prescribers:
					temp.add(line[0]) #add the unqiue precriber to the set
					prescribers.update({line[3]:temp}) #update the dict
				else:
					prescribers[line[3]].add(line[0]) #add new precriber
		except:
			outlier.append(line) #incase there is any line which is missed in the above code
	return prescribers,cost_dict,outlier

#main function 
if __name__=='__main__':
	print("inside main")
	
	input_file = sys.argv[1]
	output_file =sys.argv[2]
	
	prescribers,cost_dict,outlier=costing_counting(input_file)
	
	print(len(prescribers),len(cost_dict))
	
	prescribers_final = {} #dict to count the number of precribers
	for k ,v  in prescribers.items():
		prescribers_final.update({k:len(v)})
	
	#sorting the dict based on cost and if same cost then on drug name
	sorted_cost = sorted(cost_dict.items(), key = lambda kv:kv[1], reverse=True) 
	
	#writing to the output file, with the header
	with open(output_file, 'a') as f:
		f.write('drug_name'+','+'num_prescriber'+','+'total_cost'+'\n') 
	
	#writing to the output file contents of both the dictionary
	with open(output_file,'a') as f:
		for i in sorted_cost:
			if i[0]  in prescribers_final:
				f.write(i[0]+','+str(prescribers_final[i[0]])+','+str(i[1])+'\n') 
	