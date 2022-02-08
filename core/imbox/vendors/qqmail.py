from core.imbox.messages import Messages
from core.imbox.utils import merge_two_dicts

class QQmailMessages(Messages):
    authentication_error_message = ('If you\'re not using an authorization-code password, grab one here: https://mail.qq.com/')
    hostname = 'imap.qq.com'
    name = 'qq'

    FOLDER_LOOKUP = {
        'inbox': '"INBOX"',
        'sent': '"Sent Messages"',
        'drafts': '"Drafts"',
        'deleted': '"Deleted Messages"',
        'junk': '"Junk"',
    }

    QQMAIL_IMAP_ATTRIBUTE_LOOKUP_DIFF = {
        # 'subject': '(X-GM-RAW "subject:\'{}\'")',
        # 'label': '(X-GM-LABELS "{}")',
        # 'raw': '(X-GM-RAW "{}")'
    }

    def __init__(self,
                 connection,
                 parser_policy,
                 **kwargs):

        self.IMAP_ATTRIBUTE_LOOKUP = merge_two_dicts(self.IMAP_ATTRIBUTE_LOOKUP,
                                                     self.QQMAIL_IMAP_ATTRIBUTE_LOOKUP_DIFF)

        super().__init__(connection, parser_policy, **kwargs)