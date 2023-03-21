import ldap
from superset import db
from superset.models.core import User

LDAP_SERVER = 'ldap://your-ldap-server-url'
LDAP_BIND_USER = 'your-ldap-bind-user'
LDAP_BIND_PASSWORD = 'your-ldap-bind-password'
LDAP_SEARCH_BASE = 'your-ldap-search-base'
LDAP_SEARCH_FILTER = 'your-ldap-search-filter'

# Устанавливаем соединение с сервером Active Directory
ldap_conn = ldap.initialize(LDAP_SERVER)
ldap_conn.simple_bind_s(LDAP_BIND_USER, LDAP_BIND_PASSWORD)

# Извлекаем список пользователей из Active Directory
search_results = ldap_conn.search_s(LDAP_SEARCH_BASE, ldap.SCOPE_SUBTREE, LDAP_SEARCH_FILTER)
usernames = [entry['sAMAccountName'][0].decode() for dn, entry in search_results if isinstance(entry, dict)]

# Обновляем список пользователей в Superset
existing_users = db.session.query(User).all()
existing_usernames = [user.username for user in existing_users]
for username in usernames:
    if username not in existing_usernames:
        user = User(username=username, password='', active=True, email=f'{username}@your-company.com')
        db.session.add(user)

db.session.commit()