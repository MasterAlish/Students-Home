from students.model.base import FileResolution
from students.model.checks import ZipContainsFileConstraint
from students.utils.unpacker import unpack_resolution_to_public_dir


def is_zip_with_html_index_file(labtask):
    for constraint in labtask.constraints.instance_of(ZipContainsFileConstraint):
        if u'index.html' in constraint.file_names:
            return True
    return False


def unpack_zip_with_index(modeladmin, request, queryset):
    for resolution in queryset:
        file_resolution = FileResolution.objects.get(id=resolution.id)
        if is_zip_with_html_index_file(file_resolution.task):
            try:
                index_url = unpack_resolution_to_public_dir(file_resolution)
                file_resolution.index_file = index_url
                file_resolution.save()
            except:
                pass

unpack_zip_with_index.short_description = "Unpack zip and assign index files"
