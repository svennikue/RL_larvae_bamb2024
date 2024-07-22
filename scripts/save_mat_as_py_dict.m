% Load the .mat file
path = '/Users/xpsy1114/Documents/projects/BAMB2024/group_project/data'
Filename = 'motorData_PDM';
file_mat = append(Filename, '.mat')
data = load(fullfile(path, file_mat));

% Convert the structure to JSON
jsonData = jsonencode(data);

% Save the JSON string to a file
% currString = ['# EV ' num2str(currEV) ' title' '\n'];

jsonFile = append(path, Filename, '.json');
fid = fopen(jsonFile, 'w');
if fid == -1, error('Cannot create JSON file'); end
fwrite(fid, jsonData, 'char');
fclose(fid);

disp(['MAT structure saved as a JSON file in ', jsonFile]);
