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
    map_embed = models.TextField(blank=True, null=True, help_text="ฝังโค้ด iframe จาก Google Maps")
    has_parking = models.BooleanField(default=False, null=True)
    has_restaurant = models.BooleanField(default=False, null=True)
    has_wifi = models.BooleanField(default=False, null=True)
    has_restroom = models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "สถานที่ท่องเที่ยว"
        verbose_name_plural = "สถานที่ท่องเที่ยว"

    def get_main_image(self):
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image.image
        # ถ้าไม่มีรูปหลัก ให้ใช้รูปแรก
        first_image = self.images.first()
        if first_image:
            return first_image.image
        # ถ้าไม่มีรูปเลย ให้ใช้รูป placeholder
        return None
    

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

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='review_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for review {self.review.id}"


class TeamMember(models.Model):
    student_id = models.CharField(max_length=15, verbose_name="รหัสนักศึกษา")
    first_name = models.CharField(max_length=100, verbose_name="ชื่อ")
    last_name = models.CharField(max_length=100, verbose_name="นามสกุล")
    photo = models.ImageField(upload_to='team/', verbose_name="รูปภาพ", blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name="ลำดับการแสดงผล")

    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook")
    twitter = models.URLField(blank=True, null=True, verbose_name="Twitter")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram")
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")
  
    class Meta:
        verbose_name = "สมาชิกในทีม"
        verbose_name_plural = "สมาชิกในทีม"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class PlaceImage(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='images',
                              verbose_name="สถานที่ท่องเที่ยว")
    image = models.ImageField(upload_to='places/', verbose_name="รูปภาพ")
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="คำอธิบายรูปภาพ")
    order = models.IntegerField(default=0, verbose_name="ลำดับการแสดงผล")
    is_main = models.BooleanField(default=False, verbose_name="เป็นรูปหลัก")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")

    class Meta:
        verbose_name = "รูปภาพสถานที่ท่องเที่ยว"
        verbose_name_plural = "รูปภาพสถานที่ท่องเที่ยว"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.place.name} - รูปที่ {self.order}"

    def save(self, *args, **kwargs):
        # ถ้าตั้งเป็นรูปหลัก ให้ยกเลิกรูปหลักอื่นๆ ของสถานที่เดียวกัน
        if self.is_main:
            PlaceImage.objects.filter(place=self.place, is_main=True).exclude(id=self.id).update(is_main=False)
        super().save(*args, **kwargs)