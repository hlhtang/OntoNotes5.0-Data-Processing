# Ontonote5.0-Data-Processing
Handle Ontonote5.0 Data

## Steps:
### 1. Follow yhcc(https://github.com/yhcc/OntoNotes-5.0-NER)
Change OntoNote5.0 data into conll format.  
Change conll files into txt files.  
  
After u done yhcc tutorial, u will get v4 directory.  
&nbsp;&nbsp;&nbsp;&nbsp;v4/  
&nbsp;&nbsp;&nbsp;&nbsp;├─english/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─train.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─test.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─dev.txt  
&nbsp;&nbsp;&nbsp;&nbsp;├─chinese/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─train.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─test.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─dev.txt  
&nbsp;&nbsp;&nbsp;&nbsp;├─arabic/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─train.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─test.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─dev.txt  
### 2. BIO format 
Here change some codes from fastNLP(https://reurl.cc/ObW7G9): OntoNoteLoader.py.  
This OntoNoteLoader.py uses older fastNLP version.  
Because my fastNLP version is 0.5.0, I import some packages in OntoNoteLoader.py from fastNLP 5.0.  
  
To change to BIO format, just put v4 in the same level as OntoNoteLoader.py.  
After u **run OntoNoteLoader.py**, U will get files in v4_.
### 3. Change Chinese data into character base
**run ch_OntoNote5.0_handle.py** to get chinese character base txt file.
U will get **ch_train_.txt**, **ch_dev_txt in v4_**.
