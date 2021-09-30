from flask import g
from models import User, Account


def create_user(payload):
    session = g.db_session
    if len(payload) == 1:
        user = User(email=payload["email"])
        session.add(user)
        session.commit()
        return user
    else:
        user = User(username=payload["username"], email=payload["email"])
        session.add(user)
        session.commit()
        return user


def get_user(user_id):
    session = g.db_session
    user = session.query(User).get(user_id)
    if user:
        return user
    return None


def update_user(user_id, payload):
    session = g.db_session
    session.query(User).filter(User.id == user_id).update(payload)
    session.commit()
    return get_user(user_id)


def check_user(user_id):
    session = g.db_session
    user = session.query(User).get(user_id)
    if user:
        return user
    return None


def get_all():
    return {'users': [user.json() for user in User.query.all()]}


def delete_user(user_id):
    session = g.db_session
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        return session.commit()
    return None


def change_this(bool):
    if bool == True:
        return False
    else:
        return True


def check_account(account_id):
    session = g.db_session
    account = session.query(Account).get(account_id)
    if account:
        return True
    return False


def create_account(user_id, name):
    session = g.db_session
    check = check_user(user_id)
    if check:
        account = Account(name, user_id)
        session.add(account)
        session.commit()
        return account
    return None


def get_account(account_id):
    session = g.db_session
    account = session.query(Account).get(account_id)
    if account:
        return account
    return None


def update_account(account_id, payload):
    session = g.db_session
    account = session.query(Account).filter(Account.id == account_id).update(payload)
    user = check_user(payload["user_id"])
    if account and user:
        session.commit()
        return get_account(account_id)
    return {'message', "Account or User_id Not Found"}, 404


def delete_account(account_id):
    session = g.db_session
    account = session.query(Account).get(account_id)
    if account:
        session.delete(account)
        return session.commit()
    return None


def count_all(lis):
    count = 0
    for element in lis:
        count += 1
    return count



