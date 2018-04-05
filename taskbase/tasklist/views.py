from django.http import HttpResponse
from django.shortcuts import render


def sample_view_1(request):
    html = \
        """
        <html>
            <head>
                <title>Test page - hardcoded HTML</title>
                <style>p {color: red; padding: 10px 10px;}</style>
            </head>
            <body>
                <p>This is just a test</p>
            </body>
        </html>
        """
    return HttpResponse(html)


def sample_view_2(request):
    ctx = {'page_title': 'Test page - template',
           'msg': 'This is just a test',
           }
    return render(request, 'test_page.html', ctx)
