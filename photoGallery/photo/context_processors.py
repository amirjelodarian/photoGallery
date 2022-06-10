from user.context_processors import loggedIn


def userOwner(request):
    if 'user_id' in request.session:
        if request.session['user_id'] != None: 
            return {'userOwner': request.session['user_id']}
        else:
            return {'userOwner': False}
    else:
        return {'userOwner': False}