# from django.forms import ModelForm, forms
# from django.utils.safestring import mark_safe
#
# from file_storage.models import Image_Storage
#
#
#
#
# class Image_StorageAdminForm(ModelForm):
#
#     class Meta:
#         model = Image_Storage
#         fields = ('image', 'image_order', 'resize',)
#
#     def clean(self):
#         print('clean')
#         cleaned_data = self.cleaned_data
#         object_id = cleaned_data.get("object_id")
#         image_order = cleaned_data.get("image_order")
#         print(object_id)
#         print(image_order)
#         if Image_Storage.objects.filter(image_order=image_order).count() > 0:
#             print('hello')
#             del cleaned_data["image_order"]
#             raise forms.ValidationError("Вид не может повторяться")
#         return cleaned_data