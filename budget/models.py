from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()

    def __str__(self):
        return self.name

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    @property
    def budget_left(self):
        expense_list = Expense.objects.filter(project=self)
        total_expense_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.amount

        # temporary solution, because the form currently only allows integer amounts
        total_expense_amount = int(total_expense_amount)

        return self.budget - total_expense_amount

    @property
    def total_transactions(self):
        expense_list = Expense.objects.filter(project=self)
        # return len(expense_list)
        return expense_list.count()

    def get_absolute_url(self):
        return '/' + self.slug


class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    objects = models.Manager()


class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-amount',)

    def __str__(self):
        return self.title

    objects = models.Manager()
