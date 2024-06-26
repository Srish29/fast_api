# 1. CREATE VIRTUAL ENVIRONMENT
--install 
py -m pip install --user virtualenv
pip install venv
-- create
py -m venv venv
-- activate
venv\Scripts\activate(windows)
-- deactivate
deactivate

# 2. INSTALL REQUIRED LIBRARY
pip install -r requirements.txt

# 3. Steps
 python -m uvicorn main:app --reload
