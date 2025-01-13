from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from customer.forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import PasswordChangeView
from customer.models import Customer
from product.models import Cart
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        # Fetch the existing Customer object or initialize a form with default values
        customer = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(instance=customer)
        return render(request, 'customer/customer_profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})
    
    def post(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        
        # Fetch the existing Customer object
        customer = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(request.POST, instance=customer)  # Bind to the existing instance
        
        if form.is_valid():
            # Save the updated or new Customer object
            profile = form.save(commit=False)
            profile.user = request.user  # Ensure user is associated
            profile.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully.')
        
        return render(request, 'customer/customer_profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})
