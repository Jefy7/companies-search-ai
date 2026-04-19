## Instruction To Run


python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
Install dependencies
pip install -r requirements.txt
Run FastAPI server
uvicorn main:app --reload --port 8000

FastAPI runs at:

http://localhost:8000