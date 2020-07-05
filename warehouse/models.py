from django.db                      import models
from django.db.models               import Sum
from django.db.models.signals       import post_init
from django.urls                    import reverse
from django.utils.text              import slugify
from django.core.validators         import MaxValueValidator, FileExtensionValidator
from django.contrib.auth.models     import AbstractUser
from statistics     import mean
from django_resized import ResizedImageField
from sorl.thumbnail import ImageField as ThumbnailImageField
from warehouse.validators import *
from warehouse.fields     import *


class Blueprint(models.Model):
    added = models.DateTimeField(auto_now_add=True, verbose_name="date added")
    modif = models.DateTimeField(auto_now=True,     verbose_name="date edited")
    categ  = models.ForeignKey('Category',
        on_delete=models.CASCADE,
        related_name='blueprints',
        verbose_name="category"
    )
    author = models.ForeignKey('User',
        on_delete=models.CASCADE,
        related_name='blueprints',
    )
    name   = models.CharField(max_length=64)
    slug   = models.SlugField(verbose_name="identifier")
    image  = ThumbnailImageField(
        upload_to='covers/',
        validators=[MaxFileSizeValidator()],
        blank=True,
        verbose_name="cover picture"
    )
    desc   = models.TextField(blank=True, default='', verbose_name="description")
    pin    = models.BooleanField(default=False, verbose_name="pinned")

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
        try:
            return self.file_versions.order_by('-number')[0]
        except IndexError:
            return None

# Needed to fix a hudge performance issue related to media storage.
# Blueprint model will need its own logic to access cover dimensions.
post_init.disconnect(ThumbnailImageField.update_dimension_fields)


class Category(models.Model):
    name   = models.CharField(max_length=64)
    slug   = models.SlugField(verbose_name="identifier")
    index  = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('warehouse:main', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['index', 'id']
        verbose_name_plural = "categories"


class FileVersion(models.Model):
    added     = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "date added"
    )
    blueprint = models.ForeignKey('Blueprint',
        on_delete = models.CASCADE,
        related_name = 'file_versions'
    )
    file = models.FileField(
        upload_to='blueprints/',
        validators=[MaxFileSizeValidator(), FileExtensionValidator(('swbp', 'mps'))]
    )
    number = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="version number"
    )
    dwnlds = models.PositiveIntegerField(
        default=0,
        verbose_name="downloads number"
    )

    def __str__(self):
        return f"{self.blueprint} - version {self.number}"

    def get_absolute_url(self):
        return self.blueprint.get_absolute_url()
    
    @property
    def save_format(self):
        if self.file.name.lower().endswith('.swbp'):
            return 1
        if self.file.name.lower().endswith('.mps'):
            return 2
        return None
    
    @property
    def download_url(self):
        return reverse('warehouse:download',
            kwargs={'slug': self.blueprint.slug, 'ver':self.number}
        )

    class Meta:
        verbose_name        = "file version"
        unique_together = ('blueprint', 'number')


class Comment(models.Model):
    added     = models.DateTimeField(auto_now_add=True, verbose_name="date added")
    blueprint = models.ForeignKey('Blueprint',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey('User',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField()

    def __str__(self):
        return f"{self.blueprint} - {self.id}"

    def get_absolute_url(self):
        return self.blueprint.get_absolute_url()

    class Meta:
        ordering = ['-added']


class Review(models.Model):
    added = models.DateTimeField(auto_now_add=True, verbose_name="date added")
    blueprint = models.ForeignKey('Blueprint',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey('User',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    # TODO: Custom field type implementing this custom validator
    aesthetic_grade = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="aesthetic grade"
    )
    technic_grade = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="technic grade"
    )

    def __str__(self):
        return f"{self.blueprint} - {self.id}"

    def get_absolute_url(self):
        return self.blueprint.get_absolute_url()

    @property
    def total_grade(self):
        return (self.aesthetic_grade + self.technic_grade) / 2

    class Meta:
        unique_together = ('blueprint', 'author')


# We need this hack to make unique=true on email field without editing AbstractUser
AbstractUser._meta.get_field('email')._unique = True

class User(AbstractUser):
    avatar = ResizedImageField(
        validators=[MaxFileSizeValidator(1024**2)],
        size=(400, 400), crop=('top', 'left'),
        upload_to='avatars/', blank=True
    )
    bio = models.TextField(default='', blank=True)
    favs = models.ManyToManyField('Blueprint', related_name='fans', verbose_name="favorites")

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
