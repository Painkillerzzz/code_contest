data.jsonl is generated from `scripts/process_data.py`.

Each testcase of it contains the following fields:
- `id`:
  - int
  - the id of the testcase
- `name`: 
  - str
  - the name of the testcase
- `description`: 
  - str
  - the description of the testcase
- `inputs`: 
  - List[str]
  - the inputs of the pulic tests
- `outputs`:
  - List[str]
  - the outputs of the pulic tests