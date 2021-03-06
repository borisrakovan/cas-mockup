# -*- coding: utf-8 -*-

import json
import random
import string
from flask import request, render_template, url_for, redirect, make_response, flash, Response
from app import app, db
from app.forms import LoginForm, CreateForm
from app.models import Identity, Role, TGTicket
from app.cas_xml import create_xml_response_success, create_xml_response_failure


TG_COOKIE = 'CASTGC'
TICKET_DICT = dict()  # todo periodically invalidate


# TODO
#  bootstrap styling
#  URL validator?
#  periodically remove old tickets
#  create new identity functionality

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    # try to read tgt
    tgc = request.cookies.get(TG_COOKIE)
    service = request.args.get('service', '')

    # is ticket granting cookie set and does it key to a valid ticket-granting ticket?

    if tgc:
        tg_ticket = TGTicket.get(tgc)
        if tg_ticket:
            if service:
                identity = Identity.query.get(tg_ticket.identity_id)
                service_url = _create_ticket_and_generate_url(service, identity)
                return redirect(service_url)
            else:
                return redirect(url_for('login_successful'))

    form = LoginForm()

    # credential acceptor
    if form.validate_on_submit():
        identity = Identity.query.filter_by(login=form.login.data).first()

        # authentication failed
        if not identity:
            app.logger.info("identity %s doesn't exist" % form.login.data)
            flash(u"Subjekt %s neexistuje." % form.login.data)
            params = {}
            if service:
                params['service'] = service
            return redirect(url_for('login', **params))

        # if not identity.check_password(form.password.data):
        #     flash(u"Zadali ste nesprávne heslo.")
        #     params = {}
        #     if service:
        #         params['service'] = service
        #     return redirect(url_for('login', **params))

        # authentication successful
        service = form.service.data

        if service:
            # add service ticket (that is only valid to the service it was issued for)
            service_url = _create_ticket_and_generate_url(service, identity)
            response = make_response(redirect(service_url))
            app.logger.info("redirecting to service url: " + service_url)
        else:
            response = make_response(redirect(url_for('login_successful')))
            app.logger.info("authentication successful but no service requested")

        # set a ticket granting cookie (tgc)
        tgt = _generate_tg_ticket()
        response.set_cookie(TG_COOKIE, tgt)
        app.logger.info("setting cookie to " + tgt)

        tg_ticket = TGTicket(ticket=tgt, identity_id=identity.identity_id)
        TGTicket.add_entry(tg_ticket)

        return response


    # credential requestor
    form.service.data = service
    return render_template('login.html', title='Login', form=form, identities=Identity.query.all())


@app.route('/login_successful')
def login_successful():
    return render_template('login_successful.html', title='Login successful')


@app.route('/logout')
def logout():
    service = request.args.get('service')

    if service:
        if 'edem.microcomp.sk' in service:
            service += ':5000'
        response = make_response(redirect(service))
    else:
        response = make_response(render_template('logout.html', title='Logout'))

    tgt = request.cookies.get(TG_COOKIE)
    if tgt:
        TGTicket.remove_entry(tgt)

    response.set_cookie(TG_COOKIE, '', expires=0)

    return response


@app.route('/serviceValidate')
def service_validate():
    service = request.args.get('service')
    ticket = request.args.get('ticket', '')

    service_ticket = (service, ticket)

    xml = TICKET_DICT.pop(service_ticket, None)

    if not xml:
        app.logger.info("validation failed")
        xml = create_xml_response_failure(ticket)
    else:
        app.logger.info("validation successful")

    return Response(xml, mimetype='text/xml')


@app.route('/createSubject', methods=['GET', 'POST'])
def create_subject():
    form = CreateForm()

    if form.validate_on_submit():
        login = form.login.data
        identity_id = form.identity_id.data
        from sqlalchemy import or_
        exists = Identity.query.filter(or_(Identity.identity_id == identity_id, Identity.login == login)).first()
        if exists:
            flash(u'Subjekt s danými údajmi už existuje.')
            return redirect(url_for('create_subject'))

        identity = Identity(login=login, identity_id=identity_id, organization=form.organization.data)
        # identity.set_password('PopradTa3')
        for r_id in form.roles.data:
            identity.roles.append(Role.query.get(r_id))

        db.session.add(identity)
        db.session.commit()

        flash(u'Nový subjekt bol úspešne vytvorený.')
        return redirect(url_for('login'))

    return render_template('create_subject.html', form=form)


@app.route('/testService')
def test_service():
    # http://127.0.0.1:5000/serviceValidate?ticket=ST-32-H66FZ5MICZCW41CLKMX91M8FKA5CBNTY-node0&service=http://127.0.0.1:5000/testService
    service_ticket = request.args.get('ticket')

    return "received service ticket: " + service_ticket


def _create_ticket_and_generate_url(service, identity):
    ticket = _generate_service_ticket()
    TICKET_DICT[(service, ticket)] = create_xml_response_success(identity)
    return '{service}?ticket={ticket}'.format(service=service, ticket=ticket)


def _generate_service_ticket():
    k = 32
    ticket = []
    choices = string.ascii_uppercase + string.digits
    for i in range(k):
        ticket.append(random.choice(choices))

    ticket = ''.join(ticket)
    return "ST-32-{}-node0".format(ticket)


def _generate_tg_ticket():
    k = 32
    ticket = []
    choices = string.ascii_uppercase + string.digits
    for i in range(k):
        ticket.append(random.choice(choices))

    ticket = ''.join(ticket)
    return "TGC-32-{}-node0".format(ticket)
