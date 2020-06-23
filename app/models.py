from app import db
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash


identity_role_table = db.Table('identity_role_table',
                               db.Column('identity_id', db.Integer, db.ForeignKey('identity.identity_id')),
                               db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                               )


class Identity(db.Model):
    login = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    identity_id = db.Column(db.String(64), primary_key=True)
    first_name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    organization = db.Column(db.String(128))

    roles = db.relationship('Role', secondary=identity_role_table)
        # primaryjoin=(identity_role_table.c.identity_id == identity_id),
        # secondaryjoin=(identity_role_table.c.role_id == id),
        # backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # return check_password_hash(self.password_hash, password)
        return True


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(128))  # todo missing

    def __repr__(self):
        return self.code

class TGTicket(db.Model):
    ticket = db.Column(db.String(128), primary_key=True)
    identity_id = db.Column(db.String(64), db.ForeignKey('identity.identity_id'))

    @staticmethod
    def get(ticket):
        return TGTicket.query.get(ticket)

    @staticmethod
    def add_entry(ticket):
        try:
            db.session.add(ticket)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

    @staticmethod
    def remove_entry(ticket):
        TGTicket.query.filter(TGTicket.ticket == ticket).delete()
        db.session.commit()


# class ServiceTicket(db.Model):
#     ticket = db.Column(db.String(128), primary_key=True)
#     service = db.Column(db.String(128))
#
#     @staticmethod
#     def validate(ticket, service):
#         valid = ServiceTicket.query.filter(
#             ServiceTicket.ticket == ticket, ServiceTicket.service == service).first() is not None
#         print("tgticket valid" if valid else "tgticket INVALID")
#         return valid
#
#     @staticmethod
#     def add_entry(ticket, service):
#         ticket = ServiceTicket(ticket=ticket, service=service)
#         try:
#             db.session.add(ticket)
#             db.session.commit()
#         except exc.IntegrityError:
#             db.session.rollback()
#
#     @staticmethod
#     def remove_entry(ticket):
#         ServiceTicket.query.filter(ServiceTicket.ticket == ticket).delete()
#         db.session.commit()
