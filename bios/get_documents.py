import os
from django.conf import settings
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions

class GetDocumentsCommand(object):
    error = None
    global_last = ''

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def _get_bios_list(self, authentication_context, url, first_last=None):
        request = ClientRequest(authentication_context)
        options = RequestOptions(url)
        options.set_header('Accept', 'application/json')
        options.set_header('Content-Type', 'application/json')
        data = request.execute_query_direct(options)
        resumes = set()
        last = ''
        lasts = []

        for count, part in enumerate(list(str(data.content).split('.docx'))[:-1]):
            if 'bio' in part.lower():
                try:
                    last = part.rsplit('file=')[1] + '.docx'
                    lasts.append(last)
                    last = (
                        last
                    ).replace(
                        '%20', ' '
                    ).replace(
                        '%C3%B1', 'ñ'
                    )
                    resumes.add(last)
                except:
                    pass

        if self.global_last:
            try:
                while self.global_last == lasts.pop():
                    pass
            except:
                return set()
            last = self.global_last = lasts.pop()
        else:
            self.global_last = lasts.pop()

        url = '{0}{1}{2}{3}'.format(
            settings.SHAREPOINT_URL,
            settings.SHAREPOINT_PREFIX,
            self.global_last,
            settings.SHAREPOINT_SUFFIX
        )

        return resumes.union(
            self._get_bios_list(authentication_context, url, last)
        )

    def handle(self):
        email, password = self.email, self.password
        authentication_context = AuthenticationContext(settings.SHAREPOINT_URL)
        authentication_context.acquire_token_for_user(email, password)

        if not authentication_context.get_last_error():
            request = ClientRequest(authentication_context)
            os.makedirs(settings.BIOS_ROOT, exist_ok=True)
            for bio in self._get_bios_list(
                authentication_context, settings.BIOS_URL
            ):
                if not 'template' in bio.lower():
                    options = RequestOptions(
                        '{0}mexico/Shared Documents/Resumes/{1}'.format(
                            settings.SHAREPOINT_URL, bio
                        )
                    )
                    options.set_header('Accept', 'application/json')
                    options.set_header('Content-Type', 'application/json')
                    data = request.execute_query_direct(options)
                    docx = open('{0}/{1}'.format(
                        settings.BIOS_ROOT,
                        bio.replace(
                            "a%C3%A1", "á"
                        ).replace(
                            "e%CC%81", "é"
                        ).replace(
                            "i%C3%AD", "í"
                        ).replace(
                            "o%C3%B3", "ó"
                        ).replace(
                            "u%C3%BA", "ú"
                        ).replace(
                            "%C3%91", "Ñ"
                        ).replace(
                            "A%C3%81", "Á"
                        ).replace(
                            "E%C3%89", "É"
                        ).replace(
                            "I%C3%8D", "Í"
                        ).replace(
                            "O%C3%93", "Ó"
                        ).replace(
                            "U%C3%9A", "Ú"
                        )
                    ), "wb")
                    docx.write(data.content)
                    docx.close()
        else:
            self.error = authentication_context.get_last_error()
