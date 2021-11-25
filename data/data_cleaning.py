from tqdm import tqdm

import numpy as np
import os



# data directory path (needed to be able to launch the script from anywhere)
data_dir = os.path.dirname(os.path.realpath(__file__))

with open(data_dir + "/missing_skeletons.txt", 'r') as missing_skeletons_file:
    
    # only the file with non-missing skeletons are considered
    file_names = list(set(os.listdir(data_dir + "/nturgb+d_skeletons")) - set([file_name.replace('\n','') + ".skeleton" for file_name in missing_skeletons_file.readlines()]))
    missing_skeletons_file.close()

nb_files = len(file_names)



for i in tqdm(range(nb_files)):

    with open(data_dir + "/nturgb+d_skeletons/" + file_names[i], 'r') as raw_file:
        file_lines = raw_file.readlines()
        raw_file.close()

    number_of_frames = int(file_lines[0][:-1])
    
    if number_of_frames == (len(file_lines)-1)/28:
        
        try:

            # we only keep the spatial coordinate for each of the 25 joints at each frame 
            file_data = np.array([[file_lines[j].split(' ')[:3] for j in range(4+28*i,1+28*(i+1))] for i in range(number_of_frames)], dtype=float)

            # we save the data as a numpy array of shape (number_of_frames, number_of_joints, number_of_spatial_coordinates) = (number_of_frame, 25, 3) 
            with open(data_dir + "/nturgb+d_skeletons_cleaned/" + file_names[i].replace(".skeleton", ".npy"), 'wb') as cleaned_file:
                np.save(cleaned_file, file_data)
                cleaned_file.close()
        
        except:
            print(file_lines)
            break