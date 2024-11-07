import pickle
from pathlib import Path
from models import AddressBook

def save_address_book(book: AddressBook, filename="address_book.pkl"):
    """Save the address book to a file using pickle serialization."""
    try:
        with open(filename, "wb") as file:
            pickle.dump(book, file)
    except Exception as e:
        print(f"Error saving address book: {e}")

def load_address_book(filename="address_book.pkl") -> AddressBook:
    """Load the address book from a file using pickle deserialization."""
    if Path(filename).exists():
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error loading address book: {e}")
            return AddressBook()
    return AddressBook()