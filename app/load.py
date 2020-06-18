import xlrd
from app import db
from app.models import Identity, Role


def load_identities(path):
    #  load_identities("/mnt/c/Users/brako/Desktop/Work/microcomp_2020/other/FIX_Identity_MOD_AZA.xlsx")
    wb = xlrd.open_workbook(path)

    sheet = wb.sheet_by_index(0)  # must be 0

    role_sheet = wb.sheet_by_index(2)

    for i in range(1, sheet.nrows):
        login = sheet.cell_value(i, 0).strip()
        identity_id = sheet.cell_value(i, 2).strip()
        first_name = sheet.cell_value(i, 4).strip()
        surname = sheet.cell_value(i, 5).strip()
        password = sheet.cell_value(i, 8).strip()
        organization = sheet.cell_value(i, 12).strip()

        roles = []
        for i in range(1, role_sheet.nrows):
            if role_sheet.cell_value(i, 0).strip() == login:
                role = Role.query.filter_by(code=role_sheet.cell_value(i, 8).strip()).first()
                if role:
                    roles.append(role)

        identity = Identity(
            login=login,
            identity_id=identity_id,
            first_name=first_name,
            surname=surname,
            organization=organization
        )

        for r in roles:
            identity.roles.append(r)

        identity.set_password(password)

        db.session.add(identity)

    db.session.commit()


def load_roles():
    roles = ['MOD-R-PO', 'MOD-R-PO-API', 'MOD-R-DATA', 'MOD-R-ONTO', 'MOD-R-TRANSA', 'MOD-R-MODER', 'MOD-R-APP', 'MOD-R-SLA-ADM']
    # todo textual descriptions

    for r in roles:
        role = Role(code=r, description='')
        db.session.add(role)

    db.session.commit()