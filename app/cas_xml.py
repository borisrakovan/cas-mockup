from xml.etree import ElementTree

NS = 'http://www.yale.edu/tp/cas'


def create_xml_response_success(identity):
    ElementTree.register_namespace('cas', NS)

    root = ElementTree.Element(_('serviceResponse'))
    success = ElementTree.SubElement(root, _('authenticationSuccess'))

    user = ElementTree.SubElement(success, _('user'))
    user.text = "username"

    attrs = ElementTree.SubElement(success, _('attributes'))

    for r in identity.roles:
        role = ElementTree.SubElement(attrs, _('SPR.Roles'))
        role.text = r.code

    s_itype = ElementTree.SubElement(attrs, _('Subject.IdentityType'))
    s_itype.text = str(6)  # never accessed, just in case

    s_id = ElementTree.SubElement(attrs, _('Subject.UPVSIdentityID'))
    a_id = ElementTree.SubElement(attrs, _('Actor.UPVSIdentityID'))
    s_id.text = a_id.text = identity.identity_id

    s_name = ElementTree.SubElement(attrs, _('Subject.FormattedName'))
    a_name = ElementTree.SubElement(attrs, _('Actor.FormattedName'))
    s_name.text = a_name.text = identity.organization

    return _dumps(root)


def create_xml_response_failure(ticket):
    ElementTree.register_namespace('cas', NS)
    root = ElementTree.Element(_('serviceResponse'))

    failure = ElementTree.SubElement(root, _('authenticationFailure'), {'code': 'INVALID_TICKET'})
    failure.text = "Ticket %s not recognized" % ticket

    return _dumps(root)


def _dumps(elem):
    return ElementTree.tostring(elem, encoding='unicode')


def _pretty_print(xml_data):
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(xml_data)
    xml_pretty_str = xml.toprettyxml()
    print(xml_pretty_str)


def _(tag):
    return '{%s}%s' % (NS, tag)


if __name__ == "__main__":
    pass
    # data = create_xml_response_success()
    # ElementTree.dump(data)
    # print(ElementTree.tostring(data, encoding='unicode'))
    # pretty_print(ElementTree.tostring(data))


