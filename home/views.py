from django.shortcuts import render

def home_view(request):
    # if request.user.is_authenticated():
          # context = {
          #     'name': 'Admin',
          # }
    #     context = {
    #         'name': 'Guest',
    #     }
        context = {
            'name': 'Admin',
        }
        return render(request, 'home.html', context)
