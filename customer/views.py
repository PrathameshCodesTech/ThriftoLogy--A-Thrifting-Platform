from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from customer.forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import PasswordChangeView
from customer.models import Customer

# Create your views here.

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'customer/customer_registration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account is successfully created. 🌟 Start exploring our unique, pre-loved pieces and embrace sustainable fashion. Happy thrifting! 🛍️')
            return render(request, 'customer/customer_registration.html', {'form': CustomerRegistrationForm(), 'redirect_after_message': True})
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
        return render(request, 'customer/customer_registration.html', {'form': form})
    
class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Password changed successfully! Redirecting to login page...')
        # Return the template with success message instead of immediate redirect
        return self.render_to_response(self.get_context_data(form=form))


class ProfileView(View):
    def get(self, request):
        obj = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(instance=obj)
        return render(request, 'customer/customer_profile.html', {'form': form})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            phone_number = form.cleaned_data['phone_number']
            region = form.cleaned_data['region']
            
            obj = Customer.objects.filter(user=request.user).first()
            obj.name = name
            obj.locality = locality
            obj.city = city
            obj.zipcode = zipcode
            obj.state = state
            obj.address = address
            obj.country = country
            obj.phone_number = phone_number
            obj.region = region
            # .update(name=name,locality=locality,city=city,zipcode=zipcode,state=state,address=address,country=country,phone_number=phone_number,region=region)
            # reg = obj(user=user, name=name, locality=locality, city=city, zipcode=zipcode, state=state, address=address, country=country, phone_number=phone_number, region=region)
            obj.save()
            messages.success(request, 'Your profile is successfully updated.')
        else:
            messages.error(request, 'There was an error with your profile update. Please try again.')
        return render(request, 'customer/customer_profile.html', {'form': form})