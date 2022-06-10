import user
def loggedIn(request):
    if 'user_id' in request.session:
        if request.session['user_id'] != None: 
            return {'loggedIn': True}
        else:
            return {'loggedIn': False}
    else:
        return {'loggedIn': False}
