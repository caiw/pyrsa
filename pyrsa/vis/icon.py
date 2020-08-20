#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
icon object which can be plotted into an axis
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import PIL
import PIL.ImageOps


class Icon:
    """ Icon object, i.e. an object which can be plotted into an axis or as
    an axis label.

    Args:
        image (np.ndarray or PIL.Image)
            the image to use as an icon
        string (String)
            string to place on the icon
        col (color definition)
            background color
        border_color (color defintion)
            color of the border around the image
            default: None -> no border
        cmap (color map)
            color map applied to the image
        border_type (String)
            'pad' : pads the image with the border color
        border_width (integer)
            width of the border
        make_square (bool)
            if set to true the image is first reshaped into a square

    """

    def __init__(self, image=None, string=None, col=None, border_color=None,
                 cmap=None, border_type='pad', border_width=2,
                 make_square=False):
        self.image = image
        self.string = string
        self.col = col
        self.border_color = border_color
        self.border_type = border_type
        self.border_width = border_width
        self.cmap = cmap
        self.make_square = make_square
        self.recompute_final_image()

    def set(self, image=None, string=None, col=None, border_color=None,
            cmap=None, border_type=None, border_width=None, make_square=None):
        """ sets individual parameters of the object and recomputes the
        icon image
        """
        if image is not None:
            self.image = image
        if string is not None:
            self.string = string
        if col is not None:
            self.col = col
        if border_color is not None:
            self.border_color = border_color
        if cmap is not None:
            self.cmap = cmap
        if border_type is not None:
            self.border_type = border_type
        if border_width is not None:
            self.border_width = border_width
        if make_square is not None:
            self.make_square = make_square
        self.recompute_final_image()

    def recompute_final_image(self):
        """ computes the icon image from the parameters
        """
        if self.image is None:
            self.final_image = None
            return
        elif isinstance(self.image, np.ndarray):
            if self.image.dtype == np.float and np.any(self.image > 1):
                im = self.image / 255
            else:
                im = self.image
            if self.cmap is not None:
                im = cm.get_cmap(self.cmap)(im)
            im = PIL.Image.fromarray((im * 255).astype(np.uint8))
        else:  # we hope it is a PIL image or equivalent
            im = self.image
        im = im.convert('RGBA')
        if self.make_square:
            new_size = max(im.width, im.height)
            im = im.resize((new_size, new_size), PIL.Image.NEAREST)
        if self.border_color is not None:
            if self.border_type == 'pad':
                im = PIL.ImageOps.expand(
                    im,
                    border=self.border_width,
                    fill=self.border_color)
        self.final_image = im

    def plot(self, x, y, ax=None, size=None):
        """ plots the icon into an axis

        Args:
            x (float)
                x-position
            y (float)
                y-position
            ax (matplotlib axis)
                the axis to plot in
            size : float
                size of the icon scaling the image

        """
        if ax is None:
            ax = plt.gca()
        if self.final_image is not None:
            if size is None:
                imagebox = OffsetImage(self.final_image, zoom=1)
            else:
                imagebox = OffsetImage(self.final_image, zoom=size)
            ab = AnnotationBbox(
                imagebox, (x, y),  frameon=False,
                pad=0)
            ax.add_artist(ab)
            zorder = ab.zorder
        else:
            zorder = 0
        if self.string is not None:
            ax.annotate(self.string, (x, y),
                        horizontalalignment='center',
                        verticalalignment='center',
                        zorder=zorder + 1)
        if self.border_color is not None:
            pass

    def x_tick_label(self, x, size, offset=7, ax=None):
        """
        uses the icon as a ticklabel at location x

        Args:
            x (float)
                the position of the tick
            size (float)
                scaling the size of the icon
            offset (integer)
                how far the icon should be from the axis in points
            ax (matplotlib axis)
                the axis to put the label on

        """
        if ax is None:
            ax = plt.gca()
        if self.final_image is not None:
            imagebox = OffsetImage(self.final_image, zoom=size)
            ab = AnnotationBbox(
                imagebox, (x, 0),
                xybox=(0, -offset),
                xycoords=('data', 'axes fraction'),
                box_alignment=(.5, 1),
                boxcoords='offset points',
                bboxprops={'edgecolor': 'none'},
                arrowprops={
                    'arrowstyle': '-',
                    'shrinkA': 0,
                    'shrinkB': 1
                    },
                pad=0.1)
            ax.add_artist(ab)
            zorder = ab.zorder
        else:
            zorder = 0
        if self.string is not None:
            ax.annotate(
                self.string, (x, 0),
                xytext=(0, -offset),
                xycoords=('data', 'axes fraction'),
                textcoords='offset points',
                horizontalalignment='center',
                verticalalignment='top',
                arrowprops={
                    'arrowstyle': '-',
                    'shrinkA': 0,
                    'shrinkB': 1
                    },
                zorder=zorder + 1)

    def y_tick_label(self, y, size, offset=7, ax=None):
        """
        uses the icon as a ticklabel at location x

        Args:
            y (float)
                the position of the tick
            size (float)
                scaling the size of the icon
            offset (integer)
                how far the icon should be from the axis in points
            ax (matplotlib axis)
                the axis to put the label on

        """
        if ax is None:
            ax = plt.gca()
        if self.final_image is not None:
            imagebox = OffsetImage(self.final_image, zoom=size)
            ab = AnnotationBbox(
                imagebox, (0, y),
                xybox=(-offset, 0),
                xycoords=('axes fraction', 'data'),
                box_alignment=(1, .5),
                boxcoords='offset points',
                bboxprops={'edgecolor': 'none'},
                arrowprops={
                    'arrowstyle': '-',
                    'shrinkA': 0,
                    'shrinkB': 1
                    },
                pad=0.1)
            ax.add_artist(ab)
            zorder = ab.zorder
        else:
            zorder = 0
        if self.string is not None:
            ax.annotate(
                self.string, (0, y),
                xytext=(-offset, 0),
                xycoords=('axes fraction', 'data'),
                textcoords='offset points',
                horizontalalignment='right',
                verticalalignment='center',
                arrowprops={
                    'arrowstyle': '-',
                    'shrinkA': 0,
                    'shrinkB': 1
                    },
                zorder=zorder + 1)