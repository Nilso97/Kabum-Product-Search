from src.services.UserService import UserService
from src.services.KabumConsultService import KabumConsultService


def main():
    user_service = UserService()
    insert_values = user_service.get_user_insert_search_values()
    kabum_service = KabumConsultService(min_value=insert_values.get('min'),
                                        max_value=insert_values.get('max'))
    kabum_service.consult_service_init()


if __name__ == '__main__':
    main()
