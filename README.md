# Python JCVIS Journal converter

Python script to convert exported excel file from Microsoft CMT to XML file for import on JCVIS.

## Requirements
```
pip install -r requirements.txt
```
## Steps
1. Export the meta data from Microsoft CMT.
* Note that the first 2 rows will only contain the conference name (For example "CVIS 2023"). Please delete the first two rows.
2. Export the camera ready PDFs from Microsoft CMT.
  * The folder should look something like this:
```
CameraReady 1-37  
│
└───1
│   └───CameraReady
│       └───SomePaper.pdf
└───2
│   └───CameraReady
│       └───SomeOtherPaper.pdf
│ ...
``` 
3. There are some hardcoded variables defined at the top of the python script (such as volumne, number, etc) that needs to be changed to fit your current publication. Once you have all the variables and paths set, activate your virtual environment and run:
```
python main.py
```
4. Since the importing tool does not allow more than 15 articles at once, this script will generate multiple XML files (based on the batch_size variable). Import these XML files one at a time to accumulate the articles for the same issue. 

## Example
If you would like to see an example of the directories of the camera ready files and an Excel file with the meta data, checkout the ep/example branch.
