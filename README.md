# E-commerce Data Loading Project

This project implements the first milestone of setting up a database and loading product data from an e-commerce dataset.

## Project Structure

```
THINK41/
├── data/           # Place your products.csv file here
├── src/            # Source code
├── database/       # SQLite database files
└── requirements.txt
```

## Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Your Data
1. Extract the `products.csv` file from your downloaded archive.zip
2. Place the `products.csv` file in the `data/` directory

### Step 3: Run the Data Loading Pipeline
```bash
python src/data_loader.py
```

## What the Script Does

The `data_loader.py` script performs the following steps:

1. **Analyzes CSV Structure**: Examines the columns, data types, and sample data
2. **Creates Database Table**: Sets up a SQLite database with appropriate table structure
3. **Loads CSV Data**: Imports all product data into the database
4. **Verifies Data**: Confirms the data was loaded correctly by querying the database

## Expected Output

When you run the script, you should see:
- CSV structure analysis (columns, data types, sample rows)
- Database table creation confirmation
- Data loading progress and record count
- Verification results showing total records and sample data

## Next Steps

After completing this milestone, you'll be ready to move on to the next milestones in your project. 