# First, install the python-dotenv package
# pip install python-dotenv

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Print all environment variables
for key, value in os.environ.items():
    print(f'{key}: {value}')