import pandas as pd
import numpy as np
from datetime import datetime

import json

def run():
    # Load the JSON file
    with open('json_out/assignment_ids_to_info.json') as f:
        assignment_data = json.load(f)
    with open('json_out/course_ids_to_info.json') as f:
        course_data = json.load(f)

    # Convert JSON data to DataFrame
    assignment_df = pd.DataFrame(assignment_data).T
    course_df = pd.DataFrame(course_data).T

    assignment_df['due_date'] = assignment_df['due_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    assignment_df['course_id'] = assignment_df['course_id'].astype(str)
    assignment_df['time_estimate'] = assignment_df['time_estimate'].apply(lambda x: x['time'])

    course_df['st_dv'] = course_df['grade_values'].apply(lambda x: np.std(x))
    course_df['mean'] = course_df['grade_values'].apply(lambda x: np.mean(x))

    df = pd.merge(assignment_df, course_df, left_on = 'course_id', right_index = True)


    df['points_z'] = (df['points'] - df['mean'])/ np.std(df['st_dv'])
    df['time_left'] = df['due_date'].apply(lambda x: int((x - datetime.now()).total_seconds()/60))

    df = df.drop(['mean', 'st_dv', 'grade_values', 'assignment_ids'], axis = 1)

    df['time_left_z'] = (df['time_left'] - df['time_left'].mean())/df['time_left'].std()
    df['time_estimate_z'] = (df['time_estimate'] - df['time_estimate'].mean())/df['time_estimate'].std()
    #df['time_estimate_z'] = (df['time_estimate'] - dt['time_estimate'].mean())/df['time_estimate'].std()

    df['priority'] = df['points_z'] - df['time_left_z'] + 0.5*df['time_estimate_z']


    df = df.sort_values(by = 'priority', ascending = False).reset_index()
    df = df.drop(['points_z', 'time_left', 'time_left_z', 'time_estimate_z','priority'], axis = 1).T

    #print(df.T)

    df.to_json("priority_list.json", indent=4)