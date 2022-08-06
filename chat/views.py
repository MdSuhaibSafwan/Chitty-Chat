from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        # return redirect("")
        pass

    context = {

    }

    return render(request, "chat/index.html", context)
