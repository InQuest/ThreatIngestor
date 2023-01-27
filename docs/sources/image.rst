.. _image-source:

Image Data Extraction
------------------------

The **Image** source plugin extracts information from an image using Computer Vision (CV) and Google's OCR engine (Tesseract). This extraction should work with external images or local images

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``image``
* ``img`` (required): URL of the website with the sitemap path.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

You can extract a local image or an external image:

.. code-block:: yaml

    - name: quick-ioc-extraction
      module: image
      img: local.jpg

    - name: twitter-img-ioc-extraction
      module: image
      img: https://example.com/image.png
