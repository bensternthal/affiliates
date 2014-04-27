from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found, server_error

from commonware.response.decorators import xframe_allow

from affiliates.base.milestones import MilestoneDisplay
from affiliates.base.models import NewsItem
from affiliates.facebook.utils import in_facebook_app
from affiliates.links.models import DataPoint, Link


def home(request):
    if request.user.is_authenticated():
        return redirect('base.dashboard')
    else:
        aggregate_clicks = Link.objects.aggregate(a=Sum('aggregate_link_clicks'))['a'] or 0
        datapoint_clicks = DataPoint.objects.aggregate(d=Sum('link_clicks'))['d'] or 0
        return render(request, 'base/home.html', {
            'affiliate_count': User.objects.count(),
            'link_count': Link.objects.count(),
            'click_count': aggregate_clicks + datapoint_clicks
        })

def about(request):
    return render(request, 'base/about.html')

def terms(request):
    return render(request, 'base/terms.html')

@login_required
def dashboard(request):
    try:
        newsitem = NewsItem.objects.filter(visible=True).latest('created')
    except NewsItem.DoesNotExist:
        newsitem = None

    return render(request, 'base/dashboard.html', {
        'newsitem': newsitem,
        'milestones': MilestoneDisplay(request.user),
        'links': request.user.link_set.order_by('-created'),
    })


@xframe_allow
def handler404(request):
    if in_facebook_app(request):
        return render(request, 'facebook/error.html', status=404)
    else:
        return page_not_found(request)


@xframe_allow
def handler500(request):
    if in_facebook_app(request):
        return render(request, 'facebook/error.html', status=500)
    else:
        return server_error(request)


def strings(request):
    return render(request, 'base/strings.html')
