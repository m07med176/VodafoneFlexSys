from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Area(models.Model):
    area_name = models.CharField(max_length=50,unique=True,null=False,verbose_name="إسم المنطقة")
    selected = models.BooleanField(default=False)
    def __str__(self):
        return str(self.area_name)

    class Meta:
        db_table = "Area"
        verbose_name = "المنطقة"
        verbose_name_plural = "المناطق"
        ordering = ['area_name']

class Branch(models.Model):
    branch_name = models.CharField(max_length=50,null=False,verbose_name="إسم الفرع")
    selected = models.BooleanField(default=False)
    area = models.ForeignKey(Area,on_delete = models.CASCADE,verbose_name="المنطقة",null=False)
    def __str__(self):
        return str(self.branch_name)

    class Meta:
        db_table = "Branch"
        verbose_name = "الفرع"
        verbose_name_plural = "الفرع"
        ordering = ['branch_name']

class ROR(models.Model):
    date_record = models.DateField(null=False,auto_now = True,verbose_name = "تاريخ التسجيل")
    
    def __str__(self):
        return str(self.date_record)
    
    class Meta:
        db_table = "ROR"
        verbose_name = "تسجيل السحب"
        verbose_name_plural = "تسجيلات السحب"
        ordering = ['-date_record']

class ScrappingLogs(models.Model):
    name        = models.CharField(max_length=50,null=True,verbose_name="الإسم")
    content     = models.TextField(null=True,blank=True,verbose_name="المحتوى")
    # time stamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # log type
    type = models.IntegerField(verbose_name="نوع السجل",default=0) # zero default value of scrapping and check number is 1

    def __str__(self):
        return str(self.name)
    class Meta:
        db_table = "ScrappingLogs"
        verbose_name = "تسجيل"
        verbose_name_plural = "سجلات"
        ordering = ['-updated_at']

@receiver(post_save, sender=ScrappingLogs)
def checkSize(sender, instance=None, created=False, **kwargs):
    if created: 
        try:
            count = ScrappingLogs.objects.all().count()
            if count > 1000:ScrappingLogs.objects.filter(id__range=(0,int(instance.id-100))).delete()
        except Exception as e:
            print(e)


class Config(models.Model):
    name        = models.CharField(unique=True,max_length=50,null=False,verbose_name="Variable Name")
    content     = models.TextField(null=True,blank=True,verbose_name="Variable Content")
    def __str__(self): return str(self.name)
    class Meta:
        db_table = "Config"
        verbose_name_plural = "Vars"
        ordering = ['name']