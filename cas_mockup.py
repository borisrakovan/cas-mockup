from app import app, db
from app.models import Identity, Role, TGTicket


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Identity': Identity, 'Role': Role, 'TGTicket': TGTicket}



