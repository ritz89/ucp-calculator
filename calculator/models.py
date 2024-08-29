from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    ACTOR_TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('average', 'Average'),
        ('complex', 'Complex'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='actors')
    name = models.CharField(max_length=255)
    actor_type = models.CharField(max_length=10, choices=ACTOR_TYPE_CHOICES)

    def get_weight(self):
        if self.actor_type == 'simple':
            return 1
        elif self.actor_type == 'average':
            return 2
        elif self.actor_type == 'complex':
            return 3

    def __str__(self):
        return self.name


class UseCase(models.Model):
    COMPLEXITY_CHOICES = [
        ('simple', 'Simple'),
        ('average', 'Average'),
        ('complex', 'Complex'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='use_cases')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    complexity = models.CharField(max_length=10, choices=COMPLEXITY_CHOICES)

    def get_weight(self):
        if self.complexity == 'simple':
            return 5
        elif self.complexity == 'average':
            return 10
        elif self.complexity == 'complex':
            return 15

    def __str__(self):
        return self.name


class Transaction(models.Model):
    COMPLEXITY_CHOICES = [
        ('simple', 'Simple'),
        ('average', 'Average'),
        ('complex', 'Complex'),
    ]

    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE, related_name='transactions')
    name = models.CharField(max_length=255)
    complexity = models.CharField(max_length=10, choices=COMPLEXITY_CHOICES)

    def get_weight(self):
        if self.complexity == 'simple':
            return 1
        elif self.complexity == 'average':
            return 2
        elif self.complexity == 'complex':
            return 3

    def __str__(self):
        return self.name

class EnvironmentalFactor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='environmental_factors')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    value = models.IntegerField(default=0)

    def get_impact_factor(self):
        return self.weight * self.value

    def __str__(self):
        return f"{self.name} (Weight: {self.weight}, Value: {self.value})"


class TechnicalFactor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technical_factors')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    value = models.IntegerField(default=0)

    def get_impact_factor(self):
        return self.weight * self.value

    def __str__(self):
        return f"{self.name} (Weight: {self.weight}, Value: {self.value})"


class UseCasePoint(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='ucp')

    def calculate_ucp(self):
        total_actor_points = sum([actor.get_weight() for actor in self.project.actors.all()])
        total_use_case_points = sum([use_case.get_weight() for use_case in self.project.use_cases.all()])
        total_transaction_points = sum([transaction.get_weight() for use_case in self.project.use_cases.all() for transaction in use_case.transactions.all()])

        # Assuming Environmental and Technical Factor weights are summed up separately
        total_technical_factor = sum([factor.get_impact_factor() for factor in self.project.technical_factors.all()])
        total_environmental_factor = sum(
            [factor.get_impact_factor() for factor in self.project.environmental_factors.all()])

        ucp = (total_actor_points + total_use_case_points + total_transaction_points) * (0.6 + (0.01 * total_environmental_factor)) * (0.6 + (0.01 * total_technical_factor))
        return ucp

    def __str__(self):
        return f"UCP for {self.project.name}"


@receiver(post_save, sender=Project)
def create_default_factors(sender, instance, created, **kwargs):
    if created:
        # Default Technical Factors
        technical_defaults = [
            {'name': 'Distributed System', 'weight': 2, 'value': 0},
            {'name': 'Response time or throughput performance objectives', 'weight': 1, 'value': 0},
            {'name': 'End user efficiency', 'weight': 1, 'value': 4},
            {'name': 'Complex internal processing', 'weight': 1, 'value': 5},
            {'name': 'Code must be reusable', 'weight': 1, 'value': 0},
            {'name': 'Easy to install', 'weight': 0.5, 'value': 0},
            {'name': 'Easy to use', 'weight': 0.5, 'value': 2},
            {'name': 'Portable', 'weight': 2, 'value': 0},
            {'name': 'Easy to change', 'weight': 1, 'value': 3},
            {'name': 'Concurrent', 'weight': 1, 'value': 0},
            {'name': 'Includes special security objectives', 'weight': 1, 'value': 0},
            {'name': 'Provides direct access for third parties', 'weight': 1, 'value': 0},
            {'name': 'Special user training facilities are required', 'weight': 1, 'value': 0},
        ]
        for tech in technical_defaults:
            TechnicalFactor.objects.create(project=instance, **tech)

        # Default Environmental Factors
        environmental_defaults = [
            {'name': 'Familiar with the project model that is used', 'weight': 1.5, 'value': 3},
            {'name': 'Application experience', 'weight': 0.5, 'value': 2},
            {'name': 'Object-oriented experience', 'weight': 1, 'value': 4},
            {'name': 'Lead analyst capability', 'weight': 0.5, 'value': 4},
            {'name': 'Motivation', 'weight': 1, 'value': 4},
            {'name': 'Stable requirements', 'weight': 2, 'value': 5},
            {'name': 'Part-time staff/not main job', 'weight': -1, 'value': 4},
            {'name': 'Difficult programming language', 'weight': -1, 'value': 0},
        ]
        for env in environmental_defaults:
            EnvironmentalFactor.objects.create(project=instance, **env)