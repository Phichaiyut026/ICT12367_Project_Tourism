from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "หมวดหมู่"
        verbose_name_plural = "หมวดหมู่"

class Province(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อจังหวัด")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "จังหวัด"
        verbose_name_plural = "จังหวัด"

class Place(models.Model):
    name = models.CharField(max_length=200, verbose_name="ชื่อสถานที่")
    description = models.TextField(verbose_name="รายละเอียด")
    address = models.TextField(verbose_name="ที่อยู่")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="จังหวัด")
    categories = models.ManyToManyField(Category, verbose_name="หมวดหมู่")
    image = models.ImageField(upload_to='places/', verbose_name="รูปภาพ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่อัปเดต")
    is_featured = models.BooleanField(default=False, verbose_name="แนะนำ")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "สถานที่ท่องเที่ยว"
        verbose_name_plural = "สถานที่ท่องเที่ยว"

class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews', verbose_name="สถานที่")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ผู้ใช้")
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name="คะแนน")
    comment = models.TextField(verbose_name="ความคิดเห็น")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    
    def __str__(self):
        return f"รีวิวโดย {self.user.username} สำหรับ {self.place.name}"
    
    class Meta:
        verbose_name = "รีวิว"
        verbose_name_plural = "รีวิว"