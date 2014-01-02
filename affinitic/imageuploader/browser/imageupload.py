# encoding: utf-8
"""
gites.proprio

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import os
import simplejson
from PIL import Image, ImageFile
import zope.interface
from five import grok
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')


class MainForm(grok.View):
    grok.context(zope.interface.Interface)
    grok.name(u'affinitic.imageuploader.macros')
    grok.require('cmf.ModifyPortalContent')
    grok.template('form')

    def hasExistingImage(self, folder, fileName):
        utool = getToolByName(self.context, 'portal_url')
        portal = utool.getPortalObject()
        localFS = getattr(portal, folder)
        path = os.path.join(localFS.basepath, '%s.png' % fileName)
        return os.path.exists(path)


class ImageUpload(grok.View):
    grok.context(zope.interface.Interface)
    grok.name(u'upload-image')
    grok.require('cmf.ModifyPortalContent')

    def render(self):
        pass

    def __call__(self):
        message = ''
        fields = self.request.form
        fileName = fields.get('filename')
        fileUpload = fields.get('file')
        desiredWidth = fields.get('width')
        desiredHeight = fields.get('height')
        destination = fields.get('dest_localfs')
        redirectUrl = fields.get('redirectUrl')
        layoutMaxWidth = fields.get('layoutmaxwidth')

        extension = fileUpload.filename.split('.')[-1]
        if not extension.lower() in ['jpg', 'jpeg', 'png', 'gif']:
            message = 'Votre image doit être au format JPEG, PNG ou GIF.'
            return simplejson.dumps({'message': message,
                                     'status': -1})

        img = Image.open(fileUpload.name)
        width, height = img.size
        if width < int(desiredWidth) or height < int(desiredHeight):
            message = 'Votre image est trop petite : elle doit faire au moins %spx de large et %spx de haut.' % (desiredWidth, desiredHeight)
            return simplejson.dumps({'message': message,
                                     'status': -1})

        utool = getToolByName(self.context, 'portal_url')
        portal = utool.getPortalObject()
        imageStorage = getattr(portal, destination)
        destinationFS = os.path.join(imageStorage.basepath,
                                     '%s-tmp.png' % fileName)
        ImageFile.MAXBLOCK = width * height
        if os.path.exists(destinationFS):
            os.unlink(destinationFS)
        img.save(destinationFS, "PNG")
        self.request.response.setHeader('content-type', 'text/x-json')
        self.request.response.setHeader('Cache-Control', 'no-cache')
        return simplejson.dumps({'filename': fileName,
                                 'height': height,
                                 'width': width,
                                 'desiredHeight': desiredHeight,
                                 'desiredWidth': desiredWidth,
                                 'destination': destination,
                                 'redirectUrl': redirectUrl,
                                 'layoutmaxwidth': layoutMaxWidth,
                                 'message': message,
                                 'status': 1})


class ImageCrop(grok.View):
    grok.context(zope.interface.Interface)
    grok.name(u'crop-image')
    grok.require('cmf.ModifyPortalContent')
    grok.template('imagecrop')


class ImageSave(grok.View):
    grok.context(zope.interface.Interface)
    grok.name(u'save-image')
    grok.require('cmf.ModifyPortalContent')

    def render(self):
        pass

    def __call__(self):
        fields = self.request.form
        fileName = fields.get('filename')
        desiredWidth = fields.get('desiredWidth')
        desiredHeight = fields.get('desiredHeight')
        destination = fields.get('destination')
        redirectUrl = fields.get('redirectUrl')
        layoutMaxWidth = fields.get('layoutmaxwidth')
        coordX = int(round(float(fields.get('x'))))
        if coordX < 0:
            coordX = 0
        coordY = int(round(float(fields.get('y'))))
        if coordY < 0:
            coordY = 0
        width = int(round(float(fields.get('w'))))
        height = int(round(float(fields.get('h'))))
        scale = fields.get('scale', '')

        utool = getToolByName(self.context, 'portal_url')
        portal = utool.getPortalObject()
        imageStorage = getattr(portal, destination)
        origin = os.path.join(imageStorage.basepath, '%s-tmp.png' % fileName)
        destination = os.path.join(imageStorage.basepath, '%s.png' % fileName)
        img = Image.open(origin)

        if scale:
            imgWidth, imgHeight = img.size
            scaling = imgWidth / float(int(layoutMaxWidth))
            coordX = float(coordX) * scaling
            coordY = float(coordY) * scaling
            width = float(width) * scaling
            height = float(height) * scaling
        box = (int(coordX), int(coordY),
               int(coordX + width), int(coordY + height))
        img = img.crop(box)
        if os.path.exists(destination):
            os.unlink(destination)
        img.save(destination, "PNG")
        img = Image.open(destination)
        img = img.resize((int(desiredWidth), int(desiredHeight)),
                         Image.ANTIALIAS)
        img.save(destination, "PNG")
        os.unlink(origin)
        self.request.response.redirect(redirectUrl)
        return ''
