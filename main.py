from core.user.UserService import UserService
from src.KabumScrapService import KabumScrapService


def main():
    user_service = UserService()
    insert_values = user_service.insert_values()  
    scrap = KabumScrapService(min_value=insert_values.get('min'), max_value=insert_values.get('max'))
    scrap.scrap_init()

if __name__ == '__main__':
    main()
