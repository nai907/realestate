from django.views.generic import DetailView, ListView

from .models import Property


class HomeView(ListView):
    model = Property
    template_name = 'listings/home.html'
    context_object_name = 'featured_properties'

    def get_queryset(self):
        return Property.objects.filter(is_available=True, is_featured=True)[:6]


class ListingListView(ListView):
    model = Property
    template_name = 'listings/listing_list.html'
    context_object_name = 'properties'
    paginate_by = 9

    def get_queryset(self):
        return Property.objects.filter(is_available=True)


class ListingDetailView(DetailView):
    model = Property
    template_name = 'listings/listing_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images'] = [
            {'url': image.image.url, 'caption': image.caption}
            for image in self.object.images.all()
        ]
        return context
