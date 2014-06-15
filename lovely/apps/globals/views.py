# from django.http import HttpResponseRedirect, HttpResponse
# from django.template.context import RequestContext
# from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import redirect, render, render_to_response

# from globals.utils import slugreverse

# def home(request):
#     """ Global homepage.  Redirects to user's profile page if authenticated, registration-signup
#     otherwise. """
#     context = {}

#     if request.user.is_authenticated():
#         # return HttpResponseRedirect(slugreverse(request.user, "user-profile", args=[request.user.id]))
#         return render_to_response("landing.html", context, context_instance=RequestContext(request))
#     else:
#         return render_to_response("landing.html", context, context_instance=RequestContext(request))


# def globals_logout(request):
#     logout(request)
#     return redirect("/")

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from news.models import News

def index(request):
    latest_news = News.objects.filter()
    resp_data = {
                'latest_news': latest_news
            }
    return render_to_response('home.html', resp_data, context_instance=RequestContext(request))

