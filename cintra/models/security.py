from pyramid_zodbconn import get_connection


def groupfinder(userid, request):
    conn = get_connection(request)
    app_root = conn.root()['cintra_root']
    users = app_root['users']

    if userid in users:
        user = users[userid]
        return user.group
