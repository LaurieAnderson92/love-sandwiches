import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales figures input from the user
    """
    while True:
        print("Please enter sales data")
        print("Dads should be 6 numbers separated by a commas")
        print("Example: 10,20,10,25,7,100\n")

        data_str = input("Enter the data here:")
        
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data



def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int
    or if there arent exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"There needs to be exactly 6 values, you povided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_worksheet(data, worksheet):
    """
    Update surplus worksheet, add new row with the list data provided
    """
    print(f"Updating {worksheet} worksheet...")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} woksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the suplus for each item type.

    The suplus is defined as the sales figure subtracted from the stock:
    - Positive surplus means waste
    - Negative suplus means sandwiches made when stock ran out
    """
    print("Calculating Surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock.pop()

    surplus_data = []
    for stock,sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_entries_sales():
    """
    Adds the last 5 sales data, divides the result by 5.
    Adds an additional 10% to the result then rounds the number
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def main():
    """
    Run all program funtions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to Love Sandwiches")
# main()
sales_columns = get_last_5_entries_sales()