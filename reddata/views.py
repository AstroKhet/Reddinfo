from django.shortcuts import render, redirect
import praw
from .prawler import POST_DATA, COMMENT_DATA, PROFILE_DATA
import datetime
import time

# Create your views here.


client_id = 'r62MNtXsM0_EMQ'
client_secret = 'R_2e10JpNKVJt8cn5w-pM51-wjM'
username = 'SomeLameScrapingBot'
password = 'EC$zn#*.J8GaVRL'
user_agent = 'RedditScraper'

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, username=username, password=password,
                     user_agent=user_agent)

ACCOUNT = str()


def user_search_view(request, *args, **kwargs):
    context = {'idk': 'https://youtu.be/dQw4w9WgXcQ'}

    account = request.POST.get('USERNAME')
    if account:
        global ACCOUNT
        if account[:2] in ['U/', 'u/']:
            ACCOUNT = account[2:]
        else:
            ACCOUNT = account
        return redirect("Options")

    return render(request, "data/user_search.html", context)


def options_view(request, *args, **kwargs):
    context = {
        'username': ACCOUNT,
        'link': f"https://www.reddit.com/user/{ACCOUNT}"
    }
    return render(request, "data/options.html", context)


def posts_view(request, *args, **kwargs):
    try:
        posts, normal_awards, community_awards, t_u, t_d, t_a, t_na, t_ca, t_nc, t_cc, redditor = POST_DATA(ACCOUNT, reddit)
    except:
        return render(request, "data/invalid_username.html", {'username': ACCOUNT})

    t_nc_a = t_nc + t_cc

    try:
        r = t_u / (t_u + t_d) * 100
    except ZeroDivisionError:
        r = 0

    if r >= 10:
        rounded = str(r)[:7]
    else:
        rounded = str(r)[:6]

    context = {
        'posts': posts,
        'normal_awards': normal_awards,
        'community_awards': community_awards,
        'total_upvotes': t_u,
        'total_downvotes': t_d,
        'username': ACCOUNT,
        'link': f"https://www.reddit.com/user/{ACCOUNT}",
        'award_data': [t_a, t_na, t_ca],  # int
        'coin_data': [t_nc_a, t_nc, t_cc],
        'ratio': f"{rounded}%",
        'redditor': redditor
    }
    return render(request, "data/posts.html", context)


def comments_view(request, *args, **kwargs):
    try:
        comments, normal_awards, community_awards, t_s, t_a, t_na, t_ca, t_nc, t_cc, redditor = COMMENT_DATA(ACCOUNT, reddit)
    except:
        return render(request, "data/invalid_username.html", {'username': ACCOUNT})

    t_nc_a = t_nc + t_cc

    context = {
        'comments': comments,
        'normal_awards': normal_awards,
        'community_awards': community_awards,
        'total_score': t_s,
        'username': ACCOUNT,
        'link': f"https://www.reddit.com/user/{ACCOUNT}",
        'award_data': [t_a, t_na, t_ca],  # int
        'coin_data': [t_nc_a, t_nc, t_cc],
        'redditor': redditor
    }
    return render(request, "data/comments.html", context)


def profile_view(request, *args, **kwargs):
    name, _id, link, comment, karma, created_at, avatar, maindata, premium, mod, employee = PROFILE_DATA(ACCOUNT, reddit)

    age_seconds = int(time.time() - created_at)
    years, remainder = divmod(age_seconds, 31536000)
    months, remainder = divmod(remainder, 2592000)
    weeks, remainder = divmod(remainder, 604800)
    days, remainder = divmod(remainder, 86400)
    age = f"{years} years, {months} months, {weeks} weeks and {days} days"

    created_at = datetime.datetime.utcfromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S')
    context = {
        'username': name,
        'id': _id,
        'link_karma': link,
        'comment_karma': comment,
        'karma': karma,
        'created_at': created_at,
        'age': age,
        'avatar': avatar,
        'maindata': maindata,
        'premium': premium,
        'mod': mod,
        'employee': employee,
        'link': f"https://www.reddit.com/u/{name}"
    }

    return render(request, "data/profile.html", context)

