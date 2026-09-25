from django.db import models
from accounts.models import CustomUser, TimeStampedModel



#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------Project-----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

class Project(TimeStampedModel):
    class Visibility(models.TextChoices):
        PRIVATE = 'private', 'Private'
        PUBLIC = 'public', 'Public'

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='owned_projects',
    )
    visibility = models.CharField(
        max_length=7,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )
    members = models.ManyToManyField(
        CustomUser,
        through='ProjectMember',
        related_name='projects',
        blank=True,                      # null=True olib tashlandi (W340)
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name




#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------ProjectMember--------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

class ProjectMember(TimeStampedModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_members',
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='project_memberships',
    )
    role = models.CharField(             # yangi: Role bor edi, maydon yo'q edi
        max_length=6,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    join_date = models.DateField(blank=True, null=True)
    left_date = models.DateField(blank=True, null=True)   # hard delete'da ishlatilmaydi

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_project_member',
            ),
        ]

    def __str__(self):
        return f'{self.user} - {self.project}'





#-----------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------Task------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

class Task(TimeStampedModel):
    class Status(models.TextChoices):
        TODO = 'todo', 'ToDo'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=11,
        choices=Status.choices,
        default=Status.TODO
    )
    priority = models.CharField(
        max_length=6,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        blank=True, null=True
    )
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['status', '-created_at']

    def __str__(self):
        return self.title