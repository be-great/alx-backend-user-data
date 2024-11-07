# alx-backend-user-data


- Examples of Personally Identifiable Information (PII)
PII refers to information that can identify an individual uniquely. Examples include:
    - Full name
    - email address
    - Date of birth
- How to implement a log filter that will obfuscate PII fields
To protected PII in applications logs, a log filter replace those sensitive fields with masked values.Example
    - Define the fields to obfuscate (email, phone numbers)
    - create a log filter class (it search for that feilds in log messages and masks their values)
```python
import re
import logging

class PIIOfuscationFilter(logging.Filter):
    # filter the log with regex patterns
    record.msg = re.sub("", record.msg)
    return True
# set up logging
logger = logging.getLogger('my_logger')
logger.addFilter(PIIOfuscationFilter())
logger.setLevel(logging.INFO)

# log messages
logger.info("User;s ssn is 999-999-888 and email is kdsfdf@gmail.com")

```
- How to authenticate to a database using environment variables

- How to encrypt a password and check the validity of an input password
using hasing function , store the hash not the password, validate input by hashing it and compare the hash with the one that's stored

- How to Authenticate to a Database Using Environment Variables
Storing database credentials in environment variables is a secure practice. For example:

    Set environment variables for database credentials (e.g., DB_USER, DB_PASS, DB_HOST, DB_NAME).
    Access these variables in your code to authenticate.
<img src="imgs/user_data.png">
