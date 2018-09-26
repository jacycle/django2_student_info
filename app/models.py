from django.db import models

class Teachers(models.Model):
    SEX = (
        ('male', '男'),
        ('female', '女')
    )
    name = models.CharField(verbose_name='教师姓名', max_length=50)
    sex = models.CharField(choices=SEX, verbose_name='性别', max_length=50)
    age = models.IntegerField(verbose_name='年龄')
    address = models.CharField(verbose_name='家庭住址', max_length=250, blank=True)
    phone = models.CharField(verbose_name='手机', max_length=32, blank=True)
    class Meta:
        verbose_name = '教师信息'
        verbose_name_plural = '教师信息'

    def __str__(self):
        return self.name

class Subjects(models.Model):
    name = models.CharField(verbose_name='课程名称', max_length=50, blank=True)
    score = models.IntegerField(verbose_name='学分', blank=True)
    teacher = models.OneToOneField(Teachers, verbose_name='老师', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = '课程信息'

    def __str__(self):
        return self.name
    
class Class(models.Model):
    class_name = models.CharField(verbose_name='班级', max_length=100)
    headmaster = models.OneToOneField(Teachers, verbose_name='班主任', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'

    def __str__(self):
        return self.class_name

# Create your models here.
class Students(models.Model):
    SEX = (
        ('male', '男'),
        ('female', '女')
    )
    name = models.CharField(verbose_name='学生姓名', max_length=50)
    sex = models.CharField(choices=SEX, verbose_name='性别', max_length=50)
    age = models.IntegerField(verbose_name='年龄')
    address = models.CharField(verbose_name='家庭住址', max_length=250, blank=True)
    enter_date = models.DateField(verbose_name='入学时间')
    subjects = models.ManyToManyField(Subjects, verbose_name='选修课程', blank=True)
    remarks = models.TextField(verbose_name='备注', blank=True)

    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'

    def __str__(self):
        return self.name

class StuCourse(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    course = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'scores'
        managed = True
        verbose_name = '成绩'
        verbose_name_plural = '成绩集'
    def __str__(self):
        return "%s的%s的成绩" % (self.student.name, self.course.name)
        

