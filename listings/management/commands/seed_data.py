import io
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw

from listings.models import Property, PropertyImage

PALETTE = [
    (26, 77, 62), (47, 122, 95), (201, 162, 75), (91, 74, 124),
    (43, 100, 130), (150, 87, 60), (74, 105, 60), (120, 80, 110),
]

SAMPLE_PROPERTIES = [
    dict(title='Modern Pool Villa in Rawai', property_type='house', listing_type='sale',
         price=17500000, bedrooms=3, bathrooms=3, area_sqm=280,
         address='12/3 Soi Rawai 5', city='Rawai', state='Phuket', zip_code='83130',
         owner_phone='081-234-5678',
         is_featured=True,
         description='A modern pool villa minutes from Rawai Beach, with an open-plan living '
                      'area, private infinity pool, and a lush tropical garden.'),
    dict(title='Sukhumvit Sky Condo', property_type='condo', listing_type='sale',
         price=23900000, bedrooms=2, bathrooms=2, area_sqm=100,
         address='199 Sukhumvit Soi 24, Khlong Tan', city='Bangkok', state='Bangkok', zip_code='10110',
         owner_phone='089-876-5432',
         is_featured=True,
         description='High-floor condo in the heart of Sukhumvit with skyline views, steps '
                      'from the BTS, top restaurants, and shopping.'),
    dict(title='Riverside Serviced Apartment', property_type='apartment', listing_type='rent',
         price=25000, bedrooms=1, bathrooms=1, area_sqm=60,
         address='45 Charoen Prathet Road, Chang Klan', city='Chiang Mai', state='Chiang Mai', zip_code='50200',
         owner_phone='082-345-6789',
         is_featured=True,
         description='A quiet one-bedroom serviced apartment along the Ping River, with '
                      'in-unit laundry, a shared pool, and a private balcony.'),
    dict(title='Hillside Family House with Pool', property_type='house', listing_type='sale',
         price=29500000, bedrooms=4, bathrooms=3, area_sqm=320,
         address='88 Soi Hua Hin 112, Nong Kae', city='Hua Hin', state='Prachuap Khiri Khan', zip_code='77110',
         owner_phone='086-123-4567',
         is_featured=True,
         description='Spacious hillside home with open-concept living, a chef\'s kitchen, '
                      'and a resort-style backyard pool with sea views.'),
    dict(title='Garden Condo near Jomtien Beach', property_type='condo', listing_type='rent',
         price=32000, bedrooms=2, bathrooms=1, area_sqm=85,
         address='168 Thappraya Road, Jomtien', city='Pattaya', state='Chonburi', zip_code='20150',
         owner_phone='090-234-5678',
         is_featured=False,
         description='Ground-floor condo a short walk from Jomtien Beach, with a private '
                      'garden patio, updated bathroom, and secure parking.'),
    dict(title='Beachfront Land Plot, Bophut', property_type='land', listing_type='sale',
         price=5200000, bedrooms=0, bathrooms=0, area_sqm=500,
         address='Plot 7, Bophut Hills Road', city='Koh Samui', state='Surat Thani', zip_code='84320',
         owner_phone='081-987-6543',
         is_featured=False,
         description='Elevated plot with sea views over Bophut, with road access and '
                      'utilities already run to the property line.'),
    dict(title='Retail Shophouse in Hat Yai', property_type='commercial', listing_type='rent',
         price=60000, bedrooms=0, bathrooms=1, area_sqm=140,
         address='22 Niphat Uthit 3 Road', city='Hat Yai', state='Songkhla', zip_code='90110',
         owner_phone='087-654-3210',
         is_featured=False,
         description='High-visibility corner shophouse in a busy downtown district, '
                      'previously operated as a boutique retail shop.'),
    dict(title='Restored Thai Teak House', property_type='house', listing_type='sale',
         price=25500000, bedrooms=3, bathrooms=3, area_sqm=240,
         address='5 Moo 3, U Thong Road', city='Ayutthaya', state='Phra Nakhon Si Ayutthaya', zip_code='13000',
         owner_phone='083-456-7890',
         is_featured=True,
         description='A carefully restored traditional teak house blending period details '
                      'with modern systems, near the historic riverside temples.'),
    dict(title='Old Town Studio Apartment', property_type='apartment', listing_type='rent',
         price=15000, bedrooms=1, bathrooms=1, area_sqm=45,
         address='31 Thalang Road, Talat Yai', city='Phuket Town', state='Phuket', zip_code='83000',
         owner_phone='089-123-4567',
         is_featured=False,
         description='A compact studio in the heart of Phuket\'s Old Town, surrounded by '
                      'Sino-Portuguese architecture, cafes, and galleries.'),
]


def make_placeholder_image(title, subtitle, color, filename):
    img = Image.new('RGB', (900, 600), color=color)
    draw = ImageDraw.Draw(img)
    for i in range(0, 900, 40):
        draw.line([(i, 0), (i, 600)], fill=tuple(min(c + 12, 255) for c in color), width=1)
    draw.rectangle([40, 480, 860, 560], fill=(0, 0, 0))
    draw.text((60, 495), title, fill=(255, 255, 255))
    draw.text((60, 525), subtitle, fill=(220, 220, 220))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    return ContentFile(buffer.getvalue(), name=filename)


class Command(BaseCommand):
    help = 'Seed the database with sample properties and generated placeholder images.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Delete existing properties before seeding.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['flush']:
            Property.objects.all().delete()
            self.stdout.write('Cleared existing properties.')

        created_count = 0
        updated_count = 0
        for data in SAMPLE_PROPERTIES:
            existing = Property.objects.filter(title=data['title']).first()
            if existing:
                if not existing.owner_phone and data.get('owner_phone'):
                    existing.owner_phone = data['owner_phone']
                    existing.save(update_fields=['owner_phone'])
                    updated_count += 1
                continue

            property_obj = Property.objects.create(**data)
            color = random.choice(PALETTE)
            image_count = random.randint(2, 3)
            for i in range(image_count):
                filename = f'{property_obj.slug}-{i + 1}.jpg'
                image_file = make_placeholder_image(
                    property_obj.title, f'{property_obj.city}, {property_obj.state}', color, filename,
                )
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image_file,
                    caption=f'{property_obj.title} - view {i + 1}',
                    is_primary=(i == 0),
                )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {created_count} new properties, backfilled {updated_count} existing '
            f'(of {len(SAMPLE_PROPERTIES)} total sample records).'
        ))
