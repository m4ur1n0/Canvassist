import gpt_conduit
import priority_maker
import config
import parse_assignments
import json
from datetime import datetime

api_token = config.canvas_api_token
domain = config.canvas_domain
NUM_THREADS = 7

# generate the big files
parse_assignments.get_all_assignments_from_all_courses(api_token=api_token, domain=domain)


# now get gpt's input on the matter
assignment_ids = []
with open("json_out/assignment_ids_to_info.json", "r") as f:
    assignment_ids = list(json.load(f).keys())
``
for id in assignment_ids:
    gpt_conduit.get_json_from_assignment_id(id)

# num_assignments = len(assignment_ids)
# avg_as_per_thread = num_assignments / NUM_THREADS
# remainder = num_assignments % NUM_THREADS
# thread_set = set()
# index = 0


# for i in range(NUM_THREADS):
#     if i >= num_assignments - remainder:
#         sect = assignment_ids[index : index + avg_as_per_thread + 1]
#     else:
#         sect = assignment_ids[index : index + avg_as_per_thread]
    
#     if sect:
#         t = threading.Thread(target=gpt_conduit.fulfill_thread_list, args=sect)
#         thread_set.add(t)

# for thread in thread_set:
#     thread.join()


# now create our priority list
priority_maker.run()

# now to make the new list
# doesn't need to be in a try-except, because if this read fails then its over
new_pri_list = {}


with open("priority_list.json", "r") as pl:
    pri = json.load(pl)

    
    for entry in pri:
        entry_dict = pri[entry]
        time_est = "No time estimate"
        try:
            min = entry_dict['time_estimate']
            if min:
                time_est = str(int((int(min) / 60))) + " hrs, " + str(int(min) % 60) + " mins"
        except:
            pass

        new_pri_list[entry] = {
            'assignment_name' : entry_dict['name_x'],
            'course_name' : entry_dict['name_y'],
            'due_date' : datetime.strptime(str(datetime.fromtimestamp(entry_dict['due_date'] / 1000)), "%Y-%m-%d %H:%M:%S").strftime("%b %d, %H:%M"),
            'time_estimate' : time_est,
            'points' : entry_dict['points'],
            'steps' : list(entry_dict['steps'].values()),
            'links' : entry_dict['urls']
        }

    with open("src/to_frontend.json", "w") as f:
        json.dump(new_pri_list, f, indent=4)


