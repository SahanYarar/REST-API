from flask import Flask, request
from db import db_session, init_test_db
from crud import *
from serialization import UserSchema, AccountSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)


@app.before_request
def create_session():
    if app.config.get("TESTING"):
        test_session = init_test_db()
        g.db_session = test_session()
    else:
        g.db_session = db_session()


@app.route("/users/create_user", methods=["POST"])
def create_user_view():
    try:
        payload = request.json
        user_schema = UserSchema()
        user_schema.load(payload)
        user = create_user(payload)
    except ValidationError as err:
        return {'message': f"Given value or values are wrong{err}"}, 400
    except KeyError as ky:
        return {'message': f"Given value or values are wrong or missing:{ky}"}, 400
    return user.json(), 201


@app.route("/users/<user_id>", methods=["GET"])
def get_user_view(user_id):
    user_schema = UserSchema()
    user = get_user(user_id)
    if not user:
        return {'message': "User Not Found"}, 404
    return user_schema.dump(user), 200


@app.route("/users/update/<user_id>", methods=["PUT"])
def update_user_view(user_id):
    try:
        payload = request.json
        user_schema = UserSchema()
        user_schema.load(payload)
        user = update_user(user_id, payload,)
    except ValidationError as err:
        return {'message': f"Given value or values are wrong{err}"}, 400
    if not user:
        return {'message': "User Not Found"}, 404
    return user_schema.dump(user), 200


@app.route("/users", methods=["GET"])
def all():
    user = get_all()
    return user


@app.route("/users/delete/<user_id>", methods=["DELETE"])
def delete_user_view(user_id):
    check = check_user(user_id)
    if check:
        user = delete_user(user_id)
        if user:
            return {'message': "User isn't  Deleted "},
        return {'message': "User is Deleted"}, 204
    return {'message': "User Not Found"}, 404


@app.route("/accounts/create_account", methods=["POST"])
def create_account_view():
    try:
        payload = request.json
        account_schema = AccountSchema()
        account_schema.load(payload)
        account = create_account(payload["user_id"], payload["name"])
        user = check_user(payload["user_id"])
    except ValidationError as err:
        return {'message': f"Given value or values are wrong{err}"}, 400
    except KeyError as ky:
        return {'message': f"Given value or values are wrong or missing:{ky}"}, 400
    if not user:
        return {'message': "User Not Found"}, 404
    return account.json(), 201


@app.route("/accounts/delete/<account_id>", methods=["DELETE"])
def delete_account_view(account_id):
    check = check_account(account_id)
    if check:
        account = delete_account(account_id)
        if account:
            return {'message': "Account isn't  Deleted "},
        return {'message': "Account is Deleted"}, 204
    return {'message': "Account Not Found"}, 404


@app.route("/accounts/<account_id>", methods=["GET"])
def get_account_view(account_id):
    account_schema = AccountSchema()
    account = get_account(account_id)
    if not account:
        return {'message': "Account Not Found"}, 404
    return account_schema.dump(account), 200


@app.route("/accounts/update/<account_id>", methods=["PUT"])
def update_account_view(account_id):
    try:
        payload = request.json
        account_schema = AccountSchema()
        account_schema.load(payload)
        account = update_account(account_id, payload)
        account1 = get_account(account_id)
        user = check_user(payload["user_id"])
    except ValidationError as err:
        return {'message': f"Given value or values are wrong{err}"}, 400
    except IntegrityError as err1:
        return {'message': f"Given user_id don't match with user.id"}, 400
    except KeyError as ky:
        return {'message': f"Given value or values are wrong or missing:{ky}"}, 400
    if (not account1) or (not user):
        return {'message': "Account or User Not Found"}, 404
    return account_schema.dump(account), 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    if hasattr(g, 'db_session'):
        g.pop('db_session')
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
