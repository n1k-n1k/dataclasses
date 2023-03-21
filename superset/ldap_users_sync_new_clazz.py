from superset.security import SupersetSecurityManager
from flask_appbuilder.security.sqla.models import User
from ldap3 import Server, Connection, SUBTREE

# Конфигурация подключения к Active Directory
AD_SERVER = 'ldap://your.ad.server'
AD_BASE_DN = 'dc=your,dc=domain'
AD_SEARCH_FILTER = '(objectClass=user)'
AD_USERNAME = 'your_username'
AD_PASSWORD = 'your_password'

class CustomSecurityManager(SupersetSecurityManager):
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)

        # Синхронизация пользователей
        self.sync_ldap_users()

    def sync_ldap_users(self):
        # Подключение к Active Directory
        server = Server(AD_SERVER)
        conn = Connection(server, user=AD_USERNAME, password=AD_PASSWORD, auto_bind=True)

        # Поиск пользователей в Active Directory
        conn.search(AD_BASE_DN, AD_SEARCH_FILTER, SUBTREE)

        # Сохранение пользователей в базу данных Superset
        for entry in conn.entries:
            username = entry['sAMAccountName'].value
            email = entry['mail'].value
            first_name = entry['givenName'].value
            last_name = entry['sn'].value

            user = self.find_user(username)
            if not user:
                user = User(username=username, email=email, first_name=first_name, last_name=last_name)
                user.active = True
                self.add_user(user)
                self.get_session.commit()
