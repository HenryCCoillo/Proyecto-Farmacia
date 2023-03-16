from django.shortcuts import render,redirect
from django.views.generic import View

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from django.contrib.auth.views import LoginView


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

class RegisterView(View):
    form_class = UserCreationForm
    template_name = 'signup.html'

    def get(self,request, *args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            signup = form.save()
            login(request,signup)
            return redirect('home')
        
        for msg in form.error_messages:
            messages.error(request,form.error_messages[msg])

        return render(request,self.template_name,{'form':form})



class CustomLoginView(LoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

class Login(View):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request,data=request.POST)
        
        if form.is_valid():
            username1 = form.cleaned_data.get("username")
            password1 = form.cleaned_data.get("password")

            authen = authenticate(username=username1,password=password1)

            if authen is not None:
                login(request,authen)
                print(authen)
                return redirect('home')
            
            # messages.error(request,"Please enter a correct username and password")
            return render(request,self.template_name,{'form':form})

        # messages.error(request,"Please enter a correct username and password")
        return render(request,self.template_name,{'form':form})
        
    


class VRegistro(View):
    def get(self,request):
        form = UserCreationForm()

        return render(request,'signup.html',{'form':form})

    def post(self,request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            usuario = form.save()

            # login(request, usuario)

            # return render(request,'home.html')
            return redirect('home')

        else:
            for msg in form.error_messages:
                messages.error(request,form.error_messages[msg])

            return render(request,'signup.html',{'form':form})


def cerrar_sesion(request):
    logout(request)
    return redirect('home')

@method_decorator(login_required, name='dispatch')
class Editar(View):
    def get(self,request):
        
        return render(request, 'home.html')
        
# def home(request):
    # return render(request, 'home.html')
