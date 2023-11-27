from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import authenticate, login, logout
from .forms import EditProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from cart.views import _cart_id

CustomUser = get_user_model()


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Check if username or email is already taken
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'This email is already associated with an account.')
            else:
                form.save()
                # Redirect to a success page or login page
                return redirect('login')  # Assuming you have a URL pattern named 'login'
        else:
            # If form is not valid, show form-level error messages
            error_message = form.errors.get('__all__')
            if error_message:
                messages.error(request, error_message)
            if 'username' in form.errors:
                messages.error(request, 'This username is already taken.')
            if 'email' in form.errors:
                messages.error(request, 'This email is already associated with an account.')
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # For redirect to previous page after login
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('home')
            else:
                form.add_error('password', 'Invalid email or password')  # Add custom form-level error
                # You can also use messages framework to display the error message
                messages.add_message(request, messages.ERROR, 'Invalid email or password')

    context = {
        'form': form
    }
    return render(request, 'login.html', context)

# Existing login view logic
# def login_view(request):
#     form = LoginForm(request.POST or None)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=email, password=password)
#
#             if user is not None:
#                 login(request, user)
#
#                 # Merge guest cart with user's cart upon successful login
#                 if 'cart_id' in request.session:
#                     guest_cart = Cart.objects.get(cart_id=request.session['cart_id'])
#                     guest_cart_items = CartItem.objects.filter(cart=guest_cart)
#
#                     # Check if the user already has a cart
#                     if user.cart:
#                         user_cart_items = CartItem.objects.filter(cart=user.cart)
#                         for item in guest_cart_items:
#                             # Check if the item is already present in the user's cart
#                             if user_cart_items.filter(product=item.product).exists():
#                                 existing_item = user_cart_items.get(product=item.product)
#                                 existing_item.quantity += item.quantity
#                                 existing_item.save()
#                             else:
#                                 item.cart = user.cart
#                                 item.save()
#                     else:
#                         for item in guest_cart_items:
#                             item.cart = user.cart
#                             item.save()
#
#                     # Clear guest cart or its session
#                     guest_cart.delete()
#                     del request.session['cart_id']
#
#                 return redirect('home')
#             else:
#                 form.add_error('password', 'Invalid email or password')
#                 messages.add_message(request, messages.ERROR, 'Invalid email or password')
#
#     context = {
#         'form': form
#     }
#     return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save(commit=False)
            # Extract the cleaned data from the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            profile_image = form.cleaned_data['profile_image']
            gender = form.cleaned_data['gender']

            # Retrieve the current user instance
            user = request.user

            # Update fields only if they are provided in the form
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if phone_number:
                user.phone_number = phone_number
            if address:
                user.address = address
            if profile_image:
                user.profile_image = profile_image
            if gender:
                user.gender = gender

            # Save the updated user instance
            user.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home')  # Assuming you have a URL pattern named 'profile'
        else:
            messages.error(request, 'Error updating profile. Please check the form data.')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'settings.html', {'form': form})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = '/change-password/done/'  # Redirect to this URL after password change
