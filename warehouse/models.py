from django.db                      import models
from django.db.models               import Sum
from django.urls                    import reverse
from django.utils.text              import slugify
from django.core.validators         import MaxValueValidator
from django.contrib.auth.models     import AbstractUser
from statistics     import mean
from django_resized import ResizedImageField
from warehouse.validators import *
from warehouse.fields     import *


class Blueprint(models.Model):
    added  = models.DateTimeField(auto_now_add=True,                                                    verbose_name="date d'ajout")
    modif  = models.DateTimeField(auto_now=True,                                                        verbose_name="date d'édition")
    categ  = models.ForeignKey   ('Category', on_delete=models.CASCADE, related_name='blueprints',      verbose_name="catégorie")
    author = models.ForeignKey   ('User',     on_delete=models.CASCADE, related_name="blueprints",      verbose_name="auteur")
    name   = models.CharField    (max_length=64,                                                        verbose_name="nom")
    slug   = models.SlugField    (                                                                      verbose_name="identifiant")
    image  = models.ImageField   (upload_to='covers/', validators=[MaxFileSizeValidator()], blank=True, verbose_name="vignette")
    desc   = models.TextField    (blank=True, default='',                                               verbose_name="description")
    pin    = models.BooleanField (default=False,                                                        verbose_name="épinglé")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('warehouse:blueprint', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('warehouse:blueprint_edit', kwargs={'slug': self.slug})

    def make_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        i = 1
        while Blueprint.objects.filter(slug=unique_slug).exists() or unique_slug == "new":
            unique_slug = f"{slug}-{i}"
            i += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = self.make_unique_slug()
        super().save()

    @property
    def aesthetic_grade(self):
        return mean([review.aesthetic_grade for review in self.reviews.all()] or [0])

    @property
    def technic_grade(self):
        return mean([review.technic_grade for review in self.reviews.all()] or [0])

    @property
    def total_grade(self):
        return mean([review.total_grade for review in self.reviews.all()] or [0])

    @property
    def dwnlds(self):
        return self.file_versions.aggregate(Sum('dwnlds'))['dwnlds__sum'] or 0

    @property
    def last_file_version(self):
        return self.file_versions.order_by('-number')[0]

    class Meta:
        verbose_name = "plan"


class Category(models.Model):
    name   = models.CharField(max_length=64, verbose_name="nom")
    slug   = models.SlugField(               verbose_name="identifiant")
    index  = models.PositiveSmallIntegerField(default=0, verbose_name="index")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('warehouse:main', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['index', 'id']
        verbose_name = "catégorie"


class FileVersion(models.Model):
    added     = models.DateTimeField            (auto_now_add=True,                                                   verbose_name="date d'ajout")
    blueprint = models.ForeignKey               ('Blueprint', on_delete=models.CASCADE, related_name='file_versions', verbose_name="plan")
    file      = models.FileField                (upload_to='blueprints/', validators=[MaxFileSizeValidator()],        verbose_name="fichier")
    number    = models.PositiveSmallIntegerField(default=1,                                                           verbose_name="numéro de version")
    dwnlds    = models.PositiveIntegerField     (default=0,                                                           verbose_name="nombre de téléchargements")

    def __str__(self):
        return f"{self.blueprint} - version {self.number}"

    def get_absolute_url(self):
        return self.blueprint.get_absolute_url()
    
    @property
    def download_url(self):
        return reverse('warehouse:download', kwargs={'slug': self.blueprint.slug, 'ver':self.number})

    class Meta:
        verbose_name        = "version de fichier"
        verbose_name_plural = "versions de fichier"
        unique_together = ('blueprint', 'number')


class Comment(models.Model):
    added     = models.DateTimeField(auto_now_add=True,                                              verbose_name="date d'ajout")
    blueprint = models.ForeignKey   ('Blueprint', on_delete=models.CASCADE, related_name='comments', verbose_name="plan")
    author    = models.ForeignKey   ('User', on_delete=models.CASCADE, related_name='comments',      verbose_name="auteur")
    content   = models.TextField    (                                                                verbose_name="contenu")

    def __str__(self):
        return f"{self.blueprint} - {self.id}"

    def get_absolute_url(self):
        return self.blueprint.get_absolute_url()

    class Meta:
        verbose_name = "commentaire"
        ordering = ['-added']


class Review(models.Model):
    added     = models.DateTimeField(auto_now_add=True,                                             verbose_name="date d'ajout")
    blueprint = models.ForeignKey   ('Blueprint', on_delete=models.CASCADE, related_name='reviews', verbose_name="plan")
    author    = models.ForeignKey   ('User',      on_delete=models.CASCADE, related_name='reviews', verbose_name="auteur")

    # TODO: Custom field type implementing this custom validator
    aesthetic_grade = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], verbose_name="note esthétique")
    technic_grade   = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], verbose_name="note technique")

    def __str__(self):
        return f"{self.blueprint} - {self.id}"

    def get_absolute_url(self):
        return self.blueprint.get_absolute_url()

    @property
    def total_grade(self):
        return (self.aesthetic_grade + self.technic_grade) / 2

    class Meta:
        verbose_name = "appréciation"
        unique_together = ('blueprint', 'author')


# We need this hack to make unique=true on email field without editing AbstractUser
AbstractUser._meta.get_field('email')._unique = True

class User(AbstractUser):
    avatar = ResizedImageField(
        validators=[MaxFileSizeValidator(1024**2)],
        size=(400, 400), crop=('top', 'left'),
        upload_to='avatars/', blank=True, verbose_name="avatar"
    )
    bio    = models.TextField      (default='',  blank=True,          verbose_name="bio"    )
    favs   = models.ManyToManyField('Blueprint', related_name='fans', verbose_name="favoris")

    # Disable default AbstractUser fields
    first_name = None
    last_name  = None

    def get_absolute_url(self):
        return reverse('warehouse:user', kwargs={'username':self.username})

    @property
    def dwnlds(self):
        return sum([bp.dwnlds or 0 for bp in self.blueprints.all()])

    @property
    def fans_nb(self):
        return sum([bp.fans.count() or 0 for bp in self.blueprints.all()])

    class Meta:
        verbose_name = "utilisateur"