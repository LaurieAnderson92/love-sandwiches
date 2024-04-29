import gspread
from google.oauth2.service_account import Credentials

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
    print("Please enter sales data")
    print("Dads should be 6 numbers separated by a commas")
    print("Example: 10,20,10,25,7,100\n")

    data_str = input("Enter the data here:")
    
    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int
    or if there arent exactly 6 values
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"There needs to be exactly 6 values, you povided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")



get_sales_data()