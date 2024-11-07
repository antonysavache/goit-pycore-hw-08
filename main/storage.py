from models import AddressBook

contacts = AddressBook()
leave_commands = ['close', 'exit', 'vihod']

exceptions = {
    'LACK_OF_ARGUMENTS': 'This error might happen when you wrote wrong arguments',
    'LACK_OF_RECORDS': 'This error might happen when contacts dict is empty',
    'LACK_OF_DATA': 'This error might happen when contacts dict is fulfill, but there is no matches with the name',
    'INVALID_NUMBER': 'This error might happen when the provided number is invalid',
    'Any other exception': '500'
}