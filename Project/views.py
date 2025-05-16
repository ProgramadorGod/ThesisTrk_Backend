from django.shortcuts import redirect, render

def redirect_to_react(request):
    # return redirect("http://192.168.0.17:3000")
    # return redirect("http://172.10.8.55:3000")
    return redirect("https://teststrack.thiup.com")


def home(request):
    return redirect("https://teststrack.thiup.com")
