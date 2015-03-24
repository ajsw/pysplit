from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.ticker as tk
import matplotlib.colors as clr
import numpy as np


def traj_scatter(data, lons, lats, cavemap, zorder=19, colormap=plt.cm.Blues,
                 edgecolor='none', size=25, sizedata=None, cnormalize=None,
                 snormalize=None, vmin=None, vmax=None, levels=11, **kwargs):
    """
    Scatter-plot of trajectory, trajectory group/cluster data.

    Parameters
    ----------
    data : 1D ndarray of floats, ints
        The data to plot as color change.
    lons : 1D ndarray of floats, ints
        `data` longitudes
    lats : 1D ndarray of floats, ints
        `data` latitudes
    cavemap : Basemap instance
        Initialize a basemap first using MapDesign.make_basemap()

    Keyword Arguments
    -----------------
    zorder : int
        Default 19.  Data zorder.
    colormap : colormap
        Default `plt.cm.Blues`.  Any matplotlib colormap.
    edgecolor : string, tuple
        Default `none`.  Any matplotlib-accepted color
    size : int
        Default 25.  Point size of data unless `sizedata` specified.  Then,
        will be multiplied with `sizedata`.
    sizedata : 1D ndarray of floats
        Default None.  The data to plot as a change in marker size.
    cnormalize : string
        Default None.  [None|'boundary'|'log'|'ln'|'sqrt']
        Normalization of color scale.  If 'boundary', will create a discrete
        color map with `levels` number of colors.  For other norms, colorbar
        ticklabels will be updated with 'log' but not 'ln', 'sqrt', because
        no corresponding matplotlib colors Normalize classes are available.
    snormalize : string
        Default None.  [None|'log'|'ln'|'sqrt'].  Similar to cnormalize,
        except 'boundary' not available and does not use Normalize.
    vmin : int or float
        Default None.
    vmax : int or float
    levels : int
        Only used in BoundaryNorm

    Other Parameters
    ----------------
    kwargs : passed to Basemap.scatter() and ax.scatter()

    Returns
    -------
    cm : matplotlib PathCollection instance
        Mappable for use in creating colorbars.  Colorbars may be created
        in PySPLIT using make_cbar() or make_cax_cbar()

    """

    cnormalize = str.lower(cnormalize)
    norm = None
    msg = ('Use `cbar.ax.set_yticklabels()` ' +
           'or cbar.ax.set_xticklabels()` to change tick labels')

    transform_dict = {'sqrt' : np.sqrt,
                      'log'  : np.log10,
                      'ln'   : np.ln}

    if cnormalize is 'boundary':
        if vmin is None:
            vmin = data.min()
        if vmax is None:
            vmax = data.max()
        bounds = np.linspace(vmin, vmax, levels)
        norm = clr.BoundaryNorm(bounds, colormap.N)
    elif cnormalize is 'log':
        norm = clr.LogNorm()
    elif cnormalize is 'ln':
        data = np.log(data)
        print msg, '\nnatural log normalization'
    elif cnormalize is 'sqrt':
        data = np.sqrt(data)
        print msg, '\nsqrt normalization'

    if sizedata is not None:
        if snormalize is not None:
            sizedata = transform_dict[snormalize](sizedata)
        size = sizedata * size

    cm = cavemap.scatter(lons, lats, c=data, s=size, cmap=colormap,
                         vmin=vmin, vmax=vmax, zorder=zorder,
                         edgecolor=edgecolor, norm=norm, latlon=True, **kwargs)

    return cm


def traj_path(cavemap, lons, lats, color, lw, marker=None, linestyle='-',
              markeredgecolor='none', zorder=19, **kwargs):

    """
    Line plot of trajectory or cluster path

    Parameters
    ----------
    cavemap : Basemap instance
        Initialize a basemap first using MapDesign.make_basemap()
    lons : 1D ndarray of floats, ints
        `data` longitudes
    lats : 1D ndarray of floats, ints
        `data` latitudes
    color : string, tuple
        Trajectory path and/or marker color.  Any matplotlib-accepted color
    lw : int
        Trajectory path linewidth

    Keyword Arguments
    -----------------
    marker : string
        Default None.  The timestep marker style.
    linestyle : string
        Default '-'.  The trajectory path linestyle.
    markeredgecolor : string, tuple
        Default 'none'.  The time step marker edge color.
    zorder : int
        Default 19.  The zorder of the trajectory path.

    Other Parameters
    ----------------
    kwargs : passed to Basemap.plot() and ax.plot()

    """

    cavemap.plot(lons, lats, color, linewidth=lw, linestyle=linestyle,
                 marker=marker, latlon=True, zorder=zorder,
                 markeredgecolor=markeredgecolor, **kwargs)


def meteo_contouring(cavemap, data, longitudes, latitudes, contourf=True,
                     vmin=None, vmax=None, steps=50, levels=None, colors=None,
                     colormap=plt.cm.nipy_spectral, zorder=13, **kwargs):
    """
    Create contour or filled contour maps of `data`.

    Parameters
    ----------
    cavemap : Basemap instance
        Initialize a basemap first using MapDesign.make_basemap()
    data : (M, N) ndarray of floats
        The data to contour
    longitudes : (M) ndarray of floats
        X-coordinates of data
    latitudes : (N) ndarray of floats
        Y-coordinates of data

    Keyword Arguments
    -----------------
    contourf : Boolean
        Default True.  Create filled contour (True) or contour (False) plot.
    vmin : int or float
        Default None.  The forced minimum for drawing contours.  If None,
        `vmin` is the `data` minimum.
    vmax : int or float
        Default None.  The forced maximum for drawing contours.  If None,
        `vmax` is the `data` maximum.
    steps : int
        Default 50.  The number of steps to contour between `vmin` and `vmax`.
    levels : list of ints or floats
        Default None.  The contouring levels, overriding level creation with
        `vmin`, `vmax`, `steps`
    colors : list of strings or tuples
        Default None.  The colors to use for contouring.
    colormap : matplotlib colormap
        Default `plt.cm.Blues`.  Any matplotlib colormap.
    zorder : int
        Default 13.  Zorder of `data` on `cavemap`.

    Other Parameters
    ----------------
    kwargs : passed to Basemap.contour() then ax.contour() (or contourf)

    Returns
    -------
    cm : matplotlib.contour.QuadContourSet instance

    """

    if vmin is None:
        vmin = data.min()
    if vmax is None:
        vmax = data.max()

    if levels is None:
        levels = np.linspace(vmin, vmax, steps)

    if longitudes.ndim == 1 and data.ndim == 2:
        longitudes, latitudes = np.meshgrid(longitudes, latitudes)

    if contourf:
        cm = cavemap.contourf(longitudes, latitudes, data, zorder=zorder,
                              cmap=colormap, levels=levels, latlon=True,
                              colors=colors, **kwargs)
    else:
        cm = cavemap.contour(longitudes, latitudes, data, zorder=zorder,
                             levels=levels, colors=colors, latlon=True,
                             cmap=colormap, **kwargs)

    return cm


def adjust_contourparams(cm, contours, colors=[None],
                         othercontours_visible=True, **kwargs):
    """
    Shortcut for recoloring particular contours and/or rendering other
        contours invisible.  Can also pass other kwargs to chosen contours.

    Parameters
    ----------
    cm : matplotlib.contour.QuadContourSet instance
        The contour instance to adjust
    contours : list of ints or floats
        The levels to adjust

    Keyword Arguments
    -----------------
    colors : list of strings, tuples
        Default [None].  The colors of `contours`
    othercontours_visible : Boolean
        Default True.  If False, then levels not in `contours` will be set
        invisible.

    Other Parameters
    ----------------
    kwargs : collection keywords for `contours`.

    """

    if len(contours) != len(colors):
        colors = [colors[0]] * len(contours)

    for level, coll in zip(cm.levels, cm.collections):
        if level in contours:
            ind = contours.index(level)
            color = colors[ind]
            plt.setp(coll, **kwargs)
            if color is not None:
                coll.set_color(color)
        else:
            if not othercontours_visible:
                coll.set_alpha(0)


def make_cbar(data, ax, orientation='horizontal', cbar_size=(20, 1.0),
              reverse_cbar=False, **kwargs):
    """
    Make a colorbar on the same axis as ax.

    Parameters
    ----------
    data : PathCollection
        The mappable
    ax : Axis object
        The axis on which data is plotted

    Keyword Arguments
    -----------------
    orientation : string
        Default 'horizontal'.  ['horizontal'|'vertical'].  The location of the
        colorbar relative to the map.
    cbar_size : tuple of int, float
        Default (20, 1.0).  Colobar (aspect, shrink).  The H/W ratio of the
        colorbar, the fractional size of the colorbar.
    reverse_cbar : Boolean
        Default False. If True, colorbar is flipped over short axis.
        Value-color mapping is unaffected.

    Other Parameters
    ----------------
    kwargs : passed to edit_cbar()

    Returns
    -------
    cbar : matplotlib colorbar instance
        The new colorbar

    """

    # Initialize colorbar
    cbar = plt.colorbar(data, ax=ax, orientation=orientation,
                        aspect=cbar_size[0], shrink=cbar_size[1])

    # Reverse colorbar
    if reverse_cbar:
        if orientation is 'horizontal':
            cbar.ax.invert_xaxis()
        else:
            cbar.ax.invert_yaxis()

    # Make pretty
    edit_cbar(cbar, **kwargs)

    return cbar


def make_cax_cbar(fig, rect, data, orientation='horizontal',
                  reverse_cbar=False, extend='neither', **kwargs):
    """
    Make a colorbar on a new axis.

    Parameters
    ----------
    fig : figure instance
        The figure that needs a colorbar
    rect : list of floats
        The colorbar position and size.  [Distance from left, distance from
        bottom, size in x dimension, size in y dimension]
    data : PathCollection
        Mappable

    Keyword Arguments
    -----------------
    orientation : string
        Default 'horizontal'.  ['horizontal'|'vertical'].  The orientation of
        the colormapping within in the colorbar.
    cbar_size : tuple of int, float
        Default (20, 1.0).  Colobar (aspect, shrink).  The H/W ratio of the
        colorbar, the fractional size of the colorbar.
    reverse_cbar : Boolean
        Default False. If True, colorbar is flipped over short axis.
        Value-color mapping is unaffected.
    extend : string
        Default 'neither'.  ['both'|'neither'|'under'|'over'].
        Extend colorbar with pointed ends.

    Other Parameters
    ----------------
    kwargs : passed to edit_cbar()

    Returns
    -------
    cax : matplotlib axes instance
        The axis of the new colorbar.  Remove using fig.delaxes(cax)
    cbar : matplotlib colorbar instance
        The new colorbar

    """

    # Initialize cax and colorbar on cax
    cax = fig.add_axes(rect)
    cbar = fig.colorbar(data, cax=cax, orientation=orientation,
                        extend=extend)
    # Reverse colorbar
    if reverse_cbar:
        if orientation is 'horizontal':
            cbar.ax.invert_xaxis()
        else:
            cbar.ax.invert_yaxis()

    # Make pretty
    edit_cbar(cbar, **kwargs)

    return cax, cbar


def edit_cbar(cbar, divisions=5, cbar_label=None, tick_fs=16, label_fs=18,
              labelpad=24, rotation=0, tick_dir='out', tick_dim=(4, 2)):
    """
    Make the colorbar pretty.  Adjust fontsizes, add label, get a reasonable
        number of nice ticks, etc.

    Parameters
    ----------
    cbar : colorbar instance
        The colorbar created in make_cbar() or make_cax_cbar().

    Keyword Arguments
    -----------------
    divisions : int
        Default 5.  The number of nice ticks on the colorbar.  May be None.
    cbar_label : string
        Default None.  Colorbar label.
    tick_fs : int
        Default 16.  Font size of ticks
    label_fs : int
        Default 18.  Font size of cbar_label
    labelpad : int
        Default 24.  Spacing between tick labels and colorbar label
    rotation : int
        Default 0.  Rotation in degrees of label.
    tick_dir : string
        Default 'out'.  ['out'|'in'|'inout']
        Direction that ticks are pointing relative to colorbar
    tick_dim : tuple of floats
        Default (4, 2).  The (length, width) of the colorbar ticks

    """

    # Adjust ticks and tick labels
    if divisions is not None:
        cbar.locator = tk.MaxNLocator(divisions, integer=False)

    cbar.ax.tick_params(labelsize=tick_fs, direction=tick_dir,
                        length=tick_dim[0], width=tick_dim[1])
    cbar.update_ticks()

    # Label colorbar
    if cbar_label is not None:
        cbar.set_label(cbar_label, labelpad=labelpad, fontsize=label_fs,
                       rotation=rotation)

    # Cbar will have lines through it if mappable's alpha < 1
    cbar.set_alpha(1)
    cbar.draw_all()


def random_colors(number_ofcolors):
    """
    Generate random RGB tuples

    Parameters
    ----------
    number_ofcolors : int
        Number of tuples to generate

    Returns
    -------
    colors : list of tuples of floats
        List of len(number_ofcolors), the requested random colors
    """

    color_tmp = np.random.rand(number_ofcolors, 3)
    color_tmp = np.vsplit(color_tmp, number_ofcolors)
    colors = []
    for c in color_tmp:
        colors.append(c[0])

    return colors
