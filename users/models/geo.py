from django.db import models
from django.db.models import Q


class Geo(models.Model):
    id = models.AutoField(primary_key=True)
    country_en = models.CharField(max_length=256)
    region_en = models.CharField(max_length=256)
    city_en = models.CharField(max_length=256, db_index=True)
    country = models.CharField(max_length=256)
    region = models.CharField(max_length=256)
    city = models.CharField(max_length=256, db_index=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    population = models.IntegerField(default=0)

    class Meta:
        db_table = "geo"
        ordering = ["id"]

    @classmethod
    def update_for_user(cls, user, fuzzy=False):
        if not user.country or not user.city:
            return

        geo = Geo.objects.filter(
            Q(country=user.country) &
            (Q(city__iexact=user.city) | Q(city_en__iexact=user.city))
        ).order_by("id").first()

        if not geo and fuzzy:
            # try fuzzy matches
            geo = Geo.objects.filter(
                Q(country=user.country) &
                (Q(city__icontains=user.city) | Q(city_en__icontains=user.city))
            ).order_by("id").first()

        if geo:
            user.geo = {
                "latitude": geo.latitude,
                "longitude": geo.longitude,
            }
            user.save()
