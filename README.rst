Introduction
============

The idea of this addon product came to life when I first saw the awesome
Gridster.js (http://gridster.net/) JQuery plugin. I thought that it can be
easily integrated in Plone and use it create home pages or sub-home pages
allowing end-users to place content (portlets) anywhere in the home page using
the Gridster interface.

It have the same functionality as other products like collective.cover,
Products.Collage, etc. But with much less overhead (no tiles, no blocks) and
using Plone core technologies.


What is a gridlet?
------------------

A gridlet is a component like a portlet (at the time of writing portlets are the
only Plone component available as gridlet, but soon could be also plain content
and views). This initial implementation works with standard Plone portlets.

How it works?
-------------

The product implements a dexterity content type ``Homepage``. Create one and
edit it. You'll see a widget with the traditional add portlet dropdown. Choose
the portlets you want place as gridlets. Use the widget for place the gridlet
anywhere in the grid (6 columns) and choose their width. Save it. Voilà.

The 6 colums grid corresponds to a virtual 12-column Bootstrap 3 grid system.
The width is scaled and doubled on resultant view display for edit widget
display reasons.

Dependencies
------------

The theme used must be implemented with Bootstrap 3.

Kudos
-----

Lots of thanks to Ducksboard.com for this fabulous tool.
For more information:

 * http://gridster.net/
 * https://github.com/ducksboard/gridster.js

To Do
-----

 * Make the gridlets editable from homepage view
 * Add new gridlets types (content, views)
 * Find a way to specify phone/tablet/desktop BS variants
