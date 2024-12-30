from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncHour
from .models import *
from .forms import ImageForm,CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q



#Admins Page
@login_required
def admin(request):
    # Get the current date and time
    now = timezone.now()

    # Get the first day of the current month
    start_of_month = now.replace(day=1)

    # Get the last day of the current month
    next_month = (now.replace(day=28) + timedelta(days=4)).replace(day=1)
    end_of_month = next_month - timedelta(days=1)
    
    # Get the total images
    total_images = Image.objects.all().order_by("-created_at")

    # Get the images uploaded this month
    images_this_month = total_images.filter(created_at__gte=start_of_month, created_at__lte=end_of_month)
    
    # For counting
    total_images_count = total_images.count()
    images_this_month_count = images_this_month.count()

    # Get category data
    categories = Category.objects.all()
    category_counts = total_images.values('category').annotate(count=Count('id')).order_by('category')
    category_dict = {category.id: category.name for category in categories if category.id in [cat['category'] for cat in category_counts]}
    category_names = [category_dict[category['category']] for category in category_counts]
    image_counts = [category['count'] for category in category_counts]

    # Pagination for images
    images_list = Image.objects.all().order_by("-created_at")
    paginator = Paginator(images_list, 5)
    page_number = request.GET.get('page')
    paginated_images = paginator.get_page(page_number)

    # Hourly upload trends
    start_of_day = now - timedelta(days=1)
    uploads_per_hour = total_images.filter(created_at__gte=start_of_day).annotate(hour=TruncHour('created_at')).values('hour').annotate(count=Count('id')).order_by('hour')
    hours = [upload['hour'].strftime('%H:%M') for upload in uploads_per_hour]
    upload_counts = [upload['count'] for upload in uploads_per_hour]

    # Get the user's first and last name
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name
    full_name = f"{user_first_name} {user_last_name}"

    # Get total downloads
    downloads=ImageDownload.objects.all()
    total_downloads=downloads.count()

    # Pass data to the template
    context = {
        'total_images': total_images,
        'images': paginated_images,
        'categories': categories,
        'images_this_month_count': images_this_month_count,
        'hours': hours,
        'upload_counts': upload_counts,
        'category_names': category_names,
        'image_counts': image_counts,
        'full_name': full_name,  # Pass the user's full name to the template
        'total_downloads':total_downloads,
    }

    return render(request, 'admin_dashboard/index.html', context)



#IMAGE MANAGEMENT

#Adding Image
def add_image(request):
    categories = Category.objects.all()

    # Handle form submission
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_image')  # Redirect after successful upload
    else:
        form = ImageForm()

    # Pagination for images
    images_list = Image.objects.all().order_by("-created_at")
    paginator = Paginator(images_list, 5)
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)

    # Get the user's first and last name
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name
    full_name = f"{user_first_name} {user_last_name}"

    return render(request, 'admin_dashboard/manage_images.html', {
        'form': form, 
        'categories': categories, 
        'images': images,
        'paginator': paginator,
        'full_name':full_name,
    })

# View image detail
def view_image(request, id):
    image = get_object_or_404(Image, id=id)
    return render(request, 'admin_dashboard/view_image.html', {'image': image})

# Edit image details
def edit_image(request, id):
    image = get_object_or_404(Image, id=id)
    categories = Category.objects.all()

    if request.method == 'POST':
        # Process form data
        title = request.POST['title']
        description = request.POST['description']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        
        # Optionally handle image update (ensure to use form validation in real cases)
        image.title = title
        image.description = description
        image.category = category
        
        if 'image' in request.FILES:
            image.image = request.FILES['image']

        image.save()
        return redirect('add_image')
    
    return render(request, 'admin_dashboard/edit_image.html', {'image': image, 'categories': categories})

# Delete image (with confirmation)
def delete_image(request, id):
    image = get_object_or_404(Image, id=id)

    if request.method == 'POST':
        image.delete()
        return redirect('admin')  # Or another page after delete

    return render(request, 'admin_dashboard/delete_image.html', {'image': image})


#USER MANAGEMENT
# Add New user
def users(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! You are now logged in.')
            return redirect('users')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()

    # Pagination for users list
    users_list = get_user_model().objects.all().order_by('-date_joined')  # Get all users, ordered by join date
    paginator = Paginator(users_list, 5)  # Show 5 users per page
    page_number = request.GET.get('page')  # Get the current page number from the URL query string
    users = paginator.get_page(page_number)  # Get the users for the current page

    
    # Render the template with the form and paginated users
    return render(request, 'admin_dashboard/manage_users.html', {
        'users': users,
    }) 

# View User - Display user details
def view_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'admin_dashboard/view_user.html', {'user': user})

# Edit User - Edit user details
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')  # Redirect to the users list page after saving
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'admin_dashboard/edit_user.html', {'form': form, 'user': user})

# Delete User - Delete user and redirect back
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('users')  # Redirect back to the users list page after deleting


def categories(request):
    return render(request,'admin_dashboard/categories.html')



def gallery(request):
    images=Image.objects.all().order_by('-created_at')
    categories=Category.objects.all()
    return render(request, 'index.html',{
        "images":images,
        "categories":categories
        })



def load_images(request):
    # Get all images, ordered by creation date (most recent first)
    images = Image.objects.all().order_by('-created_at')

    # Paginate the images (20 images per page)
    paginator = Paginator(images, 20)
    page_number = request.GET.get('page', 1)  # Get the page number from the request

    try:
        page_images = paginator.get_page(page_number)  # Get the images for the requested page
    except:
        return JsonResponse({"images": []})  # Return an empty list if the page doesn't exist

    # Prepare JSON data
    images_data = [
        {
            "id": image.id,
            "url": image.image_file.url,  # Adjust field name if necessary
            "title": image.name,  # Include any other fields if needed
        }
        for image in page_images
    ]

    # Return JSON response
    return JsonResponse({
        "images": images_data,
        "has_next": page_images.has_next(),  # To know if there are more pages
    })


@csrf_exempt 
def download_image(request): 
    if request.method == 'POST': 
        data = json.loads(request.body) 
        image_id = data.get('image_id') 
        try: 
            image = Image.objects.get(id=image_id) 
            ImageDownload.objects.create(image=image) 
            return JsonResponse({'message': 'Download count updated successfully.'}, status=200) 
        except Image.DoesNotExist: 
            return JsonResponse({'error': 'Image not found.'}, status=404) 
        
    return JsonResponse({'error': 'Invalid request.'}, status=400)

@csrf_exempt 
def like_image(request): 
    if request.method == 'POST': 
        data = json.loads(request.body) 
        image_id = data.get('image_id') 
        image = get_object_or_404(Image, id=image_id) 
        image_like, created = ImageLike.objects.get_or_create(image=image) 
        image_like.likes += 1 
        image_like.save() 
        return JsonResponse({'message': 'Like count updated successfully.'}, status=200) 
    return JsonResponse({'error': 'Invalid request.'}, status=400)



@csrf_exempt
def search_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        search_term = data.get('search_term', '').strip()
        if search_term:
            images = Image.objects.filter(name__icontains=search_term) | Image.objects.filter(description__icontains=search_term)
            if images.exists():
                # Serialize image data to send as JSON response
                image_data = [
                    {
                        'id': image.id,
                        'name': image.name,
                        'image_file': image.image_file.url
                    }
                    for image in images
                ]
    
                return JsonResponse({'success': True, 'images': image_data}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'No images found.'}, status=404)
        return JsonResponse({'success': False, 'message': 'Invalid search term.'}, status=400)
    return JsonResponse({'error': 'Invalid request.'}, status=400)


@csrf_exempt
def filter_by_category(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            category_name = data.get('category', '').strip()

            # Check if a valid category is provided
            if category_name.lower() == 'all' or not category_name:
                # If "All" category is selected or no category is given, return all images
                images = Image.objects.all().order_by('-created_at')
            else:
                # Filter images by category name
                images = Image.objects.filter(category__name__icontains=category_name)

            if images.exists():
                # Serialize image data to send as JSON response
                image_data = [
                    {
                        'id': image.id,
                        'name': image.name,
                        'image_file': image.image_file.url
                    }
                    for image in images
                ]
                return JsonResponse({'success': True, 'images': image_data}, status=200)

            else:
                return JsonResponse({'success': False, 'message': 'No images found in this category.'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data provided.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method. Only POST is allowed.'}, status=400)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin' if user.username == 'david' else 'gallery')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'admin_dashboard/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! You are now logged in.')
            return redirect('gallery')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'admin_dashboard/register.html', {'form': form})

def password_view(request):
    return render(request, 'admin_dashboard/password.html')
