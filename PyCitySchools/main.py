#!/usr/bin/env python
# coding: utf-8


# Dependencies and Setup
import pandas as pd
import numpy as np
from IPython.display import display

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)
# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

def summarize_district(school_data_complete, school_data, student_data):
# TODO: improve this code like with schools summary
    total_schools = school_data.shape[0]
    total_students = student_data.shape[0]
    total_budget = school_data['budget'].sum()
    total_math_pass = dict((student_data["math_score"]>70).value_counts())[True]
    total_reading_pass = dict((student_data["reading_score"]>70).value_counts())[True]
    average_math_score = student_data['math_score'].mean()
    average_reading_score = student_data['reading_score'].mean()
    percent_math_pass = round(total_math_pass/total_students*100, 2)
    percent_reading_pass = round(total_reading_pass/total_students*100, 2)

    district_summary = pd.DataFrame(
        {'Total Schools' : [total_schools],
        'Total Students' : [total_students],
        'Total Budget' : [total_budget],
        'Per Student Budget' : [round(total_budget/total_students, 2)],
        'Average Math Score' : [round(average_math_score, 2)],
        'Average Reading Score': [round(average_reading_score,2)],
        '% Students Pass Math' : [percent_math_pass],
        '% Students Pass Reading' : [percent_reading_pass],
        'Average Pass Rate' : [(percent_math_pass+percent_reading_pass)/2]})

    return district_summary

def summarize_schools(school_data_complete, school_data, student_data):
    schools = []
    for high_school in school_data['school_name']:
        this_school_table = school_data_complete[school_data_complete['school_name'] == high_school]
        _, _, _, _, school_name, _, _, id, type, students, budget = this_school_table.iloc[0]
        percent_math_pass = round(this_school_table[this_school_table['math_score']>70].shape[0]/students*100, 2)
        percent_reading_pass = round(this_school_table[this_school_table['math_score']>70].shape[0]/students*100, 2)

        schools.append (
            {'School Name' : school_name,
            'School Type' : type,
            'Total Students' : students,
            'Total School Budget' : budget,
            'Per Student Budget' : budget/students,
            'Average Math Score' : round(this_school_table['math_score'].mean(), 2),
            'Average Reading Score' : round(this_school_table['reading_score'].mean(), 2),
            '% Passing Math' : percent_math_pass,
            '% Passing Reading' : percent_reading_pass,
            'Overall Passing Rate': (percent_math_pass + percent_reading_pass)/2
            })
    schools_summary = pd.DataFrame (schools)
    schools_summary = schools_summary[['School Name', 'School Type', "Total Students", 'Total School Budget', 'Per Student Budget', 'Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading', 'Overall Passing Rate']]
    return schools_summary


district_summary = summarize_district(school_data_complete, school_data, student_data)
schools_summary = summarize_schools(school_data_complete, school_data, student_data)

# Display only relevant columns
display(schools_summary [['Per Student Budget', 'Total Students', 'Overall Passing Rate']])
display(district_summary [['Total Schools', 'Total Students', 'Per Student Budget', '% Students Pass Math', '% Students Pass Reading', 'Average Pass Rate']])

print ("--------------- Top 5 best performing schools -----------------------------------")
display(schools_summary.nlargest(5, 'Overall Passing Rate'))
print ("--------------- Bottom 5 worst performing schools -----------------------------------")
display(schools_summary.nsmallest(5, 'Overall Passing Rate'))

# spending_bins = [0, 585, 615, 645, 675]
# group_names = ["<$585", "$585-615", "$615-645", "$645-675"]
#
#
# size_bins = [0, 1000, 2000, 5000]
# group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
