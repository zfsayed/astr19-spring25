# ---------------------------------
# 0. Copy all this script into one cell, between steps 7 and 8 of your final project
#    You will need to install the "reproject" package with pip
#    This script will "reproject" all images onto the same shape using one image as a reference
# ---------------------------------

from astropy.io import fits
from astropy.wcs import WCS
from reproject import reproject_interp

# ---------------------------------
# 1. Load your reference image
#    This will define the WCS and shape for all others
# ---------------------------------
file_reference = '/Users/naziakhan/ASTR19/data/MAST_2025-06-11T0029/JWST/jw02731-o001_t017_nircam_clear-f090w/jw02731-o001_t017_nircam_clear-f090w_i2d.fits'
with fits.open(file_reference) as hdulist:
    # For JWST i2d images, 'SCI' is commonly the science extension
    ref_header = hdulist['SCI'].header
    ref_data = hdulist['SCI'].data

# Create a WCS object from the reference
ref_wcs = WCS(ref_header)

# This shape will be used for all reprojected images
output_shape = ref_data.shape

# ---------------------------------
# 2. Reproject the other images
# ---------------------------------
fname1 =  '/Users/naziakhan/Downloads/MAST_2025-06-11T0140/JWST/jw02731-o001_t017_nircam_clear-f187n/jw02731-o001_t017_nircam_clear-f187n_i2d.fits'
fname2 = '/Users/naziakhan/Downloads/MAST_2025-06-11T0140/JWST/jw02731-o001_t017_nircam_f444w-f470n/jw02731-o001_t017_nircam_f444w-f470n_i2d.fits'
fname3 = '/Users/naziakhan/Downloads/MAST_2025-06-11T0140/JWST/jw02731-o001_t017_nircam_clear-f200w/jw02731-o001_t017_nircam_clear-f200w_i2d.fits'
fname4 = '/Users/naziakhan/Downloads/MAST_2025-06-11T0140/JWST/jw02731-o001_t017_nircam_clear-f444w/jw02731-o001_t017_nircam_clear-f444w_i2d.fits'
fname5 = '/Users/naziakhan/Downloads/MAST_2025-06-11T0140/JWST/jw02731-o001_t017_nircam_clear-f335m/jw02731-o001_t017_nircam_clear-f335m_i2d.fits'
fname6 = file_reference

other_filenames = [
    fname1,
    fname2,
    fname3,
    fname4,
    fname5,
    fname6,
]

# Reproject all other files according to the reference
for fname in other_filenames:
    with fits.open(fname) as hdulist:
        data = hdulist['SCI'].data
        header = hdulist['SCI'].header
        wcs_in = WCS(header)
    
    # Reproject this image onto the reference WCS
    # reproject_interp returns (reprojected_data, footprint)
    reprojected_data, footprint = reproject_interp(
        (data, wcs_in),
        ref_wcs,
        shape_out=output_shape
    )

    # Optionally, update the header to match the reference WCS
    # so that the new FITS is self-consistent
    new_header = ref_header.copy()

    # Save the new file
    out_name = fname.replace('.fits', '_reproj.fits')
    hdu = fits.PrimaryHDU(reprojected_data, header=new_header)
    hdu.writeto(out_name, overwrite=True)
    print(f"Reprojected {fname} -> {out_name}")

# Make a 3-color false image of the NGC 3324 by combining all 6 images in any way of your choice
import matplotlib.pyplot as plt
from astropy.visualization import simple_norm
from astropy.io import fits
import numpy as np

# Loading the reprojected Fit files
f_blue  = '/Users/naziakhan/ASTR19/data/MAST_2025-06-11T0029/JWST/jw02731-o001_t017_nircam_clear-f090w/jw02731-o001_t017_nircam_clear-f090w_i2d.fits'
f_green = '/Users/naziakhan/Downloads/MAST_2025-06-11T0140/JWST/jw02731-o001_t017_nircam_clear-f200w/jw02731-o001_t017_nircam_clear-f200w_i2d_reproj.fits'
f_red   = '/Users/naziakhan/Downloads/MAST_2025-06-11T0140/JWST/jw02731-o001_t017_nircam_clear-f444w/jw02731-o001_t017_nircam_clear-f444w_i2d_reproj.fits'

# Load data from FITS
with fits.open(f_blue) as b, fits.open(f_green) as g, fits.open(f_red) as r:
    blue_data = b[1].data.astype(np.float32)
    green_data = g[0].data.astype(np.float32)
    red_data = r[0].data.astype(np.float32)

# Clip extreme values to avoid outlier domination
def normalize(data, percentile_low=0.25, percentile_high=99.5):
    vmin, vmax = np.percentile(data[~np.isnan(data)], [percentile_low, percentile_high])
    return np.clip((data - vmin) / (vmax - vmin), 0, 1)

R = normalize(red_data)
G = normalize(green_data)
B = normalize(blue_data)

# Stack into RGB image
rgb = np.dstack((R, G, B))

# Show image
plt.figure(figsize=(10, 10))
plt.imshow(rgb, origin='lower')
plt.title("NGC 3324 – JWST False Color RGB")
plt.axis('off')
plt.tight_layout()

# Save image as PNG
plt.savefig("NGC_3324_falsecolor_RGB.png", dpi=300, bbox_inches='tight')
print("Saved image as 'NGC_3324_falsecolor_RGB.png'")
plt.show()
