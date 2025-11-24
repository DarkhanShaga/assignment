from django.db import models


class AppointmentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    CONFIRMED = 'Confirmed', 'Confirmed'
    DECLINED = 'Declined', 'Declined'


class CaregivingType(models.TextChoices):
    BABYSITTER = 'babysitter', 'Babysitter'
    CAREGIVER_ELDERLY = 'caregiver for elderly', 'Caregiver for Elderly'
    PLAYMATE = 'playmate for children', 'Playmate for Children'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    given_name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_description = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return f"{self.given_name} {self.surname}" if self.given_name or self.surname else self.email


class Caregiver(models.Model):
    caregiver_user = models.OneToOneField('User', models.CASCADE, primary_key=True)
    photo = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    caregiving_type = models.CharField(max_length=50, choices=CaregivingType.choices)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caregiver'

    def __str__(self):
        return str(self.caregiver_user)


class Member(models.Model):
    member_user = models.OneToOneField('User', models.CASCADE, primary_key=True)
    house_rules = models.TextField(blank=True, null=True)
    dependent_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'

    def __str__(self):
        return str(self.member_user)


class Address(models.Model):
    member_user = models.OneToOneField('Member', models.CASCADE, primary_key=True)
    house_number = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'

    def __str__(self):
        return f"{self.house_number} {self.street}, {self.town}" if self.street else str(self.member_user)


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    caregiver_user = models.ForeignKey('Caregiver', models.CASCADE)
    member_user = models.ForeignKey('Member', models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    work_hours = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.CharField(max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING)

    class Meta:
        managed = False
        db_table = 'appointment'

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.appointment_date}"


class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    member_user = models.ForeignKey('Member', models.CASCADE)
    required_caregiving_type = models.CharField(max_length=50, choices=CaregivingType.choices)
    other_requirements = models.TextField(blank=True, null=True)
    date_posted = models.DateField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'job'

    def __str__(self):
        return f"Job {self.job_id} - {self.required_caregiving_type}"


class JobApplication(models.Model):
    caregiver_user = models.ForeignKey('Caregiver', models.CASCADE)
    job = models.ForeignKey('Job', models.CASCADE)
    date_applied = models.DateField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'job_application'
        unique_together = [['caregiver_user', 'job']]

    def __str__(self):
        return f"{self.caregiver_user} applied for {self.job}"


