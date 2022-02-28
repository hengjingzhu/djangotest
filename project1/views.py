from django.http import HttpResponse


def testview(request):
    return HttpResponse('FIRST DJANGO VIEW2')