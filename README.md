# ServiceNow Attachment Sender in Python

### Purpose

Sends attachments to ServiceNow. The name of the attachment must correspond to a unique value on the record.

### Example Prerequisites

- Attachment names in example must contain the number of a corresponding record. EX: INC12345.html
- Attachments are all contained in the same folder
- Attachments are all .html
- dir_loc, instance, and Authorization header are populated along with table and query in getRecInfo

### Output

- Each send or failure to send is logged to the console in a format that can be easily grep'd
- An attachment magically appears on the record founds in ServiceNow. Ex: INC12345

### Execution

- Ensure Python3 is installed
- Clone project to a folder on your computer
- Activate the virtual environment by navigating to the top folder and typing source bin/activate
- Deactivate the environment when you are finished by typing deactivate
