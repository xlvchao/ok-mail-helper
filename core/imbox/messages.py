from core.imbox.query import build_search_query
from core.imbox.parser import fetch_email_by_uid

class Messages:

    IMAP_ATTRIBUTE_LOOKUP = {
        'unread': '(UNSEEN)',
        'read': '(SEEN)',
        'flagged': '(FLAGGED)',
        'unflagged': '(UNFLAGGED)',
        'sent_from': '(FROM "{}")',
        'sent_to': '(TO "{}")',
        'date__gt': 'SINCE "{}"',
        'date__lt': 'BEFORE "{}"',
        'date__on': '(ON "{}")',
        'subject': '(SUBJECT "{}")',
        'uid__range': '(UID {})',
        'text': '(TEXT "{}")',
    }

    FOLDER_LOOKUP = {}

    current_page = None
    page_size = None
    total_records = None
    total_pages = None
    emails = None
    page = None

    def __init__(self,
                 connection,
                 parser_policy,
                 **kwargs):

        self.connection = connection
        self.parser_policy = parser_policy
        self.kwargs = kwargs
        self._uid_list = self._query_uids(**kwargs)
        self._uid_list_flagged = self._query_uids(flagged=True)
        self._uid_list_unread = self._query_uids(unread=True)

        self.emails = list(self._fetch_email_list())
        self.page = {'current_page':self.current_page, 'page_size':self.page_size,
                                    'total_records':self.total_records, 'total_pages':self.total_pages, 'emails':self.emails}

    def _fetch_email(self, uid):
        email_object = fetch_email_by_uid(uid=uid,
                                  connection=self.connection,
                                  parser_policy=self.parser_policy)
        if uid in self._uid_list_flagged:
            email_object.__dict__['flagged'] = True
        else:
            email_object.__dict__['flagged'] = False

        if uid in self._uid_list_unread:
            email_object.__dict__['unread'] = True
        else:
            email_object.__dict__['unread'] = False
        return email_object.__dict__

    def _query_uids(self, **kwargs):
        query_ = build_search_query(self.IMAP_ATTRIBUTE_LOOKUP, **kwargs)
        _, data = self.connection.uid('search', None, query_)
        if data[0] is None:
            return []
        uids = list(reversed(data[0].split()))

        if 'current_page' in kwargs:
            self.current_page = kwargs['current_page']
        if 'page_size' in kwargs:
            self.page_size = kwargs['page_size']

        if self.current_page==None or self.page_size==None:
            return uids

        self.total_records = len(uids)
        if self.page_size != 0:
            self.total_pages = (len(uids) + self.page_size - 1) // self.page_size

        if (self.current_page-1) * self.page_size > len(uids) - 1:
            return []
        return uids[((self.current_page-1) * self.page_size):((self.current_page-1) * self.page_size + self.page_size)]

    def _fetch_email_list(self):
        for uid in self._uid_list:
            yield self._fetch_email(uid)

    def __repr__(self):
        if len(self.kwargs) > 0:
            return '{' + "'current_page':{},'page_size':{},'total_records':{},'total_pages':{},'emails':{}"\
                    .format(self.current_page,self.page_size,self.total_records,self.total_pages,self.emails) + '}'
        return '{}'

    def __iter__(self):
        return self._fetch_email_list()

    def __next__(self):
        return self

    def __len__(self):
        return len(self._uid_list)

    def __getitem__(self, index):
        uids = self._uid_list[index]

        if not isinstance(uids, list):
            uid = uids
            return uid, self._fetch_email(uid)

        return [(uid, self._fetch_email(uid))
                for uid in uids]
