from django.db                  import models
from django.db.models           import Sum
from django.urls                import reverse
from django.utils.text          import slugify
from django.core.validators     import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from statistics                 import mean
from warehouse.validators       import *
from warehouse.fields           import *


class Blueprint(models.Model):
    added  = models.DateTimeField       (auto_now_add=True,                                                    verbose_name="date d'ajout")
    modif  = models.DateTimeField       (auto_now=True,                                                        verbose_name="date d'édition")
    categ  = models.ForeignKey          ('Category', on_delete=models.CASCADE, related_name='blueprints',      verbose_name="catégorie")
    author = models.ForeignKey          ('User',     on_delete=models.CASCADE, related_name="blueprints",      verbose_name="auteur")
    name   = models.CharField           (max_length=64,                                                        verbose_name="nom")
    mass   = models.PositiveIntegerField(default=0,                                                            verbose_name="masse")
    blocks = models.PositiveIntegerField(default=0,                                                            verbose_name="nombre de blocs")
    slug   = models.SlugField           (                                                                      verbose_name="identifiant")
    image  = models.ImageField          (upload_to='covers/', validators=[MaxFileSizeValidator()], blank=True, verbose_name="vignette")
    desc   = models.TextField           (blank=True, default='',                                               verbose_name="description")
    pin    = models.BooleanField        (default=False,                                                        verbose_name="épinglé")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('warehouse:blueprint', kwargs={'slug': self.slug})

    def make_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        i = 1
        while Blueprint.objects.filter(slug=unique_slug).exists():
            unique_slug = '%s-%s' % (slug, i)
            i += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = self.make_unique_slug()
        super().save()

    @property
    def aesthetic_grade(self):
        return mean([review.get_aesthetic_grade() for review in self.reviews.all()] or [0])

    @property
    def technic_grade(self):
        return mean([review.get_technic_grade() for review in self.reviews.all()] or [0])

    @property
    def total_grade(self):
        return mean([review.get_total_grade() for review in self.reviews.all()] or [0])

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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('warehouse:main', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "catégorie"


class FileVersion(models.Model):
    added     = models.DateTimeField            (auto_now_add=True,                                                   verbose_name="date d'ajout")
    blueprint = models.ForeignKey               ('Blueprint', on_delete=models.CASCADE, related_name='file_versions', verbose_name="plan")
    file      = models.FileField                (upload_to='blueprints/', validators=[MaxFileSizeValidator()],        verbose_name="fichier")
    number    = models.PositiveSmallIntegerField(default=1,                                                           verbose_name="numéro de version")
    dwnlds    = models.PositiveIntegerField     (default=0,                                                           verbose_name="nombre de téléchargements")

    def __str__(self):
        return "%s - version %s" % (self.blueprint, self.number)

    def get_absolute_url(self):
        return reverse('warehouse:blueprint', kwargs={'id': self.id})

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
        return "%s - %s" % (self.blueprint, self.id)

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
    grade_interior  = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], verbose_name="note design intérieur")
    grade_exterior  = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], verbose_name="note design extérieur")
    grade_space     = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], verbose_name="note espace")
    grade_mechanics = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], verbose_name="note mécanismes")
    grade_weapons   = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], verbose_name="note armes")
    grade_maneuv    = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], verbose_name="note manoeuvrabilité")

    def __str__(self):
        return "%s - %s" % (self.blueprint, self.id)

    def get_absolute_url(self):
        return self.blueprint.get_absolute_url()

    def get_aesthetic_grade(self):
        return (self.grade_interior + self.grade_exterior + self.grade_space) / 3.0

    def get_technic_grade(self):
        return (self.grade_mechanics + self.grade_weapons + self.grade_maneuv) / 3.0

    def get_total_grade(self):
        return (self.get_aesthetic_grade() + self.get_technic_grade()) / 2.0

    class Meta:
        verbose_name = "appréciation"
        unique_together = ('blueprint', 'author')


class User(AbstractUser):
    avatar = models.ImageField     (upload_to='avatars/', validators=[MaxFileSizeValidator()], blank=True, verbose_name="avatar" )
    bio    = models.TextField      (default='',                                                blank=True, verbose_name="bio"    )
    favs   = models.ManyToManyField('Blueprint', related_name='fans',                                      verbose_name="favoris")

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

    @property
    def blocks(self):
        return sum([bp.blocks or 0 for bp in self.blueprints.all()])

    class Meta:
        verbose_name = "utilisateur"
