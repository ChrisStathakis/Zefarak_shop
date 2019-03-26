from django.core.exceptions import ValidationError
import os

def upload_image(instance, filename):
    return f'warehouse_images/{instance.order_related.vendor.title}/{instance.order_related.title}/{filename}'


def validate_file(value):
    if value.file.size > 1024 * 1024 * 0.5:
        raise ValidationError('this file is bigger than 0.5mb')
    return value

def category_site_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'category_site/{0}/{1}'.format(instance.title, filename)


def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'product/{0}/{1}'.format(instance.product.title, filename)


def upload_location(instance, filename):
    return "%s%s" %(instance.id, filename)


def my_awesome_upload_function(instance, filename):
    """ this function has to return the location to upload the file """
    return os.path.join('/media_cdn/%s/' % instance.id, filename)
