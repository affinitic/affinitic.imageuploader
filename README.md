affinitic.imageuploader
=======================

Smart image uploader for Plone.

This package provides an image uploader and cropper for custom templates (this is not a widget).
The uploaded images can be cropped and will be saved to a Local FS.

Features
--------
- You get a progress bar while the image is uploading.
- You can define desired width and height for the final image. This will modify the cropping box ratio and some constraints.
- You can define a maximum width (depending on your layout). The image will be scaled down (if needed) in the cropping tool to this maximum width.
- You can define the name of the resulting image file.
- You can define a redirection URL (after the upload and crop processes succeed).
- Of course, the name of the destination folder is also configurable.

Limitations
-----------
- images are always saved in PNG
- texts are only in French for now
- you need to have a Local FS configured in your portal root

Sample
------
Sample code and live demo can be found on http://localhost:8080/yourplone/@@UploaderSample_view.

Known issues
------------
- we should check for existing image instead of trying to always display it
- there are no tests

Credits
-------
The file upload tool is based on https://github.com/blueimp/jQuery-File-Upload.
The image cropping tool is based on https://github.com/tapmodo/Jcrop.
