from model import Place, Address, Exit, Direction


def mock_exit():
    return Exit(eid=42,
                dxn=Direction.NORTH,
                port='some portal',
                nbr=mock_place())


def mock_place():
    return Place(pid=1,
                 name='some_place',
                 desc='some_place_description',
                 address=mock_address())


def mock_address():
    return Address(idn=1,
                   name='some_game_address',
                   street_number=42,
                   street_name='some_street',
                   city='some_city',
                   country='some_country')
