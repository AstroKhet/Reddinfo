import praw


def POST_DATA(user_account, instance):
    posts = {}
    community_awards = {}
    normal_awards = {'Silver': 0, 'Gold': 0, 'Platinum': 0, 'Argentium': 0}
    total_upvotes = 0
    total_downvotes = 0

    TOTAL_NORMAL_AWARDS = 0
    TOTAL_COMMUNITY_AWARDS = 0
    TOTAL_NORMAL_COINS = 0
    TOTAL_COMMUNITY_COINS = 0
    nc = {'Silver': 100, 'Gold': 500, 'Platinum': 1800, 'Argentium': 20000}

    redditor = instance.redditor(user_account)

    for submission in redditor.submissions.top(limit=None):
        title = submission.title
        url = f"https://www.reddit.com{submission.permalink}"

        ratio = float(submission.upvote_ratio)
        score = submission.score

        upvotes = score * ratio
        downvotes = score * (1 - ratio)

        total_upvotes += upvotes
        total_downvotes += downvotes

        awards = submission.all_awardings
        subreddit = str(submission.subreddit)

        if subreddit not in posts.keys():
            posts[subreddit] = dict()
        posts[subreddit][url] = (title, round(upvotes), round(downvotes))

        for award in awards:
            name = str(award['name'])
            count = int(award['count'])
            img = str(award['icon_url'])
            coins = int(award['coin_price'])

            if name in ('Silver', 'Gold', 'Platinum', 'Argentium'):
                normal_awards[name] += count
                TOTAL_NORMAL_AWARDS += count
                TOTAL_NORMAL_COINS += nc[name]

            else:
                if subreddit not in community_awards.keys():
                    # New community encountered
                    community_awards[subreddit] = dict()
                    community_awards[subreddit][name] = [count, img, coins]
                    TOTAL_COMMUNITY_AWARDS += count
                    TOTAL_COMMUNITY_COINS += coins

                else:
                    # Community exists in dict
                    # There should be an award dict pre-existing in community_awards[subreddit]
                    if name in community_awards[subreddit].keys():
                        community_awards[subreddit][name][0] += count
                        TOTAL_COMMUNITY_AWARDS += count
                        TOTAL_COMMUNITY_COINS += coins
                    else:
                        community_awards[subreddit][name] = [count, img, coins]
                        TOTAL_COMMUNITY_AWARDS += count
                        TOTAL_COMMUNITY_COINS += coins

    TOTAL_AWARDS = TOTAL_NORMAL_AWARDS + TOTAL_COMMUNITY_AWARDS
    return posts, normal_awards, community_awards, round(total_upvotes), round(total_downvotes), TOTAL_AWARDS, \
           TOTAL_NORMAL_AWARDS, TOTAL_COMMUNITY_AWARDS, TOTAL_NORMAL_COINS, TOTAL_COMMUNITY_COINS, redditor


def COMMENT_DATA(user_account, instance):
    comments = {}
    community_awards = {}
    normal_awards = {'Silver': 0, 'Gold': 0, 'Platinum': 0, 'Argentium': 0}
    # PRAW doesn't support getting upvote_ratio anymore for comments
    total_score = 0

    TOTAL_NORMAL_AWARDS = 0
    TOTAL_COMMUNITY_AWARDS = 0
    TOTAL_NORMAL_COINS = 0
    TOTAL_COMMUNITY_COINS = 0
    nc = {'Silver': 100, 'Gold': 500, 'Platinum': 1800, 'Argentium': 20000}

    redditor = instance.redditor(user_account)

    for comment in redditor.comments.top(limit=None):
        url = f"https://www.reddit.com{comment.permalink}"
        body = comment.body

        score = comment.score
        total_score += score

        awards = comment.all_awardings
        subreddit = str(comment.subreddit)

        if subreddit not in comments.keys():
            comments[subreddit] = dict()

        comments[subreddit][url] = (body, score)

        for award in awards:
            name = str(award['name'])
            count = int(award['count'])
            img = str(award['icon_url'])
            coins = int(award['coin_price'])

            if name in ('Silver', 'Gold', 'Platinum', 'Argentium'):
                normal_awards[name] += count
                normal_awards[name] += count
                TOTAL_NORMAL_AWARDS += count
                TOTAL_NORMAL_COINS += nc[name]

            else:
                if subreddit not in community_awards.keys():
                    # New community encountered
                    community_awards[subreddit] = dict()
                    community_awards[subreddit][name] = [count, img, coins]
                    TOTAL_COMMUNITY_AWARDS += count
                    TOTAL_COMMUNITY_COINS += coins

                else:
                    # Community exists in dict
                    # There should be an award dict pre-existing in community_awards[subreddit]
                    if name in community_awards[subreddit].keys():
                        community_awards[subreddit][name][0] += count
                        TOTAL_COMMUNITY_AWARDS += count
                        TOTAL_COMMUNITY_COINS += coins
                    else:
                        community_awards[subreddit][name] = [count, img, coins]
                        TOTAL_COMMUNITY_AWARDS += count
                        TOTAL_COMMUNITY_COINS += coins

    TOTAL_AWARDS = TOTAL_NORMAL_AWARDS + TOTAL_COMMUNITY_AWARDS
    return comments, normal_awards, community_awards, round(total_score), TOTAL_AWARDS, \
           TOTAL_NORMAL_AWARDS, TOTAL_COMMUNITY_AWARDS, TOTAL_NORMAL_COINS, TOTAL_COMMUNITY_COINS, redditor


def PROFILE_DATA(user_account, instance):
    redditor = instance.redditor(user_account)

    name = redditor.name
    _id = redditor.id

    link = redditor.link_karma
    comment = redditor.comment_karma
    karma = link + comment

    created_at = redditor.created_utc
    avatar = redditor.icon_img
    maindata = redditor.subreddit

    premium = redditor.is_gold
    mod = redditor.is_mod
    employee = redditor.is_employee

    return name, _id, link, comment, karma, created_at, avatar, maindata, premium, mod, employee


