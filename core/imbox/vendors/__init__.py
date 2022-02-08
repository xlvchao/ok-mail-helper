from core.imbox.vendors.gmail import GmailMessages
from core.imbox.vendors.qqmail import QQmailMessages

vendors = [GmailMessages, QQmailMessages]

hostname_vendorname_dict = {vendor.hostname: vendor.name for vendor in vendors}
name_authentication_string_dict = {vendor.name: vendor.authentication_error_message for vendor in vendors}

__all__ = [v.__name__ for v in vendors]

__all__ += ['hostname_vendorname_dict',
            'name_authentication_string_dict']
