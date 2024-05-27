# Python JCVIS Journal converter

Python script to convert exported excel file from Microsoft CMT to XML file for import on JCVIS.

## Requirements
```
pip install -r requirements.txt
```
## Steps
1. Export the meta data from Microsoft CMT. To download the excel file, users first need to filter submissions (however they want really, but basically make sure to get the ones they want to actually publish), set 'Show: All' (so that all submissions are shown on the same page of the website, since it oddly only exports what is shown), and then use 'Actions'->'Export to Excel'->'Submissions' OR 'Camera Ready Submissions'. 
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
4. Since the importing tool does not allow more than 15 articles at once, this script will generate multiple XML files (based on the batch_size variable). Import these XML files one at a time to accumulate the articles for the same issue. To upload to OJS / JCVIS, first login to jcvis.net. Next, select 'Tools' on the left, then within Import/Export, select 'Native XML Plugin'. Upload the generated XML files one by one. It may take as 15-20 seconds per file (usually a bit more than 1 second per article within the file). Wait until the website confirms the import was successful (or, on subsequent uploads, gives a warning that the issue already exists and that the import was successful).

## Example
If you would like to see an example of the directories of the camera ready files and an Excel file with the meta data, checkout the ep/example branch.
