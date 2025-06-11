# Step 1
import numpy as np
import sep

# Step 2: Setup for reading and plotting
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['figure.figsize'] = [10., 8.]

# Step 3: Read the image from the correct HDU ('SCI' = hdul[1])
with fits.open("/Users/naziakhan/ASTR19/data/MAST_2025-06-11T0029/JWST/jw02731-o001_t017_nircam_clear-f090w/jw02731-o001_t017_nircam_clear-f090w_i2d.fits") as hdul:
    data = hdul[1].data

# Step 4: Ensure image is float32, as required by SEP
if data is None:
    raise ValueError("Image data not found in expected HDU.")
data = data.astype(np.float32)

# Step 5: Show the image
m, s = np.mean(data), np.std(data)
plt.imshow(data, interpolation='nearest', cmap='gray', vmin=m-s, vmax=m+s, origin='lower')
plt.colorbar()

# Step 6: Measure background
bkg = sep.Background(data)

# Step 7: Print global background stats
print(bkg.globalback)
print(bkg.globalrms)

# Step 8: Visualize background
bkg_image = bkg.back()
plt.imshow(bkg_image, interpolation='nearest', cmap='gray', origin='lower')
plt.colorbar()

# Step 9: Visualize background RMS
bkg_rms = bkg.rms()
plt.imshow(bkg_rms, interpolation='nearest', cmap='gray', origin='lower')
plt.colorbar()

# Step 10: Subtract background
data_sub = data - bkg

# Step 11: Mask NaNs or bad values (optional but useful for huge space images)
mask = np.isnan(data_sub)
data_sub[mask] = 0  # or use median, or interpolation

# Step 12: Increase SEP pixel buffer stack again (fixes buffer overflow)
sep.set_extract_pixstack(5000000)  # raised from 1M to 5M

# Step 13: Extract objects with a reasonable detection threshold
objects = sep.extract(data_sub, thresh=2.0, err=bkg.globalrms)  # 1.5 → 2.0 helps reduce false positives

# Step 14: Plot detected objects
from matplotlib.patches import Ellipse

fig, ax = plt.subplots()
m, s = np.mean(data_sub), np.std(data_sub)
im = ax.imshow(data_sub, interpolation='nearest', cmap='gray', vmin=m-s, vmax=m+s, origin='lower')

for i in range(len(objects)):
    e = Ellipse(xy=(objects['x'][i], objects['y'][i]),
                width=6*objects['a'][i],
                height=6*objects['b'][i],
                angle=objects['theta'][i] * 180. / np.pi)
    e.set_facecolor('none')
    e.set_edgecolor('red')
    ax.add_artist(e)

# Step 15: Optional – view available object fields
# print(objects.dtype.names)

# Step 16: Photometry – measure flux in circular aperture
flux, fluxerr, flag = sep.sum_circle(data_sub, objects['x'], objects['y'],
                                     3.0, err=bkg.globalrms, gain=1.0)

# Step 17: Print first 10 flux measurements
for i in range(min(10, len(flux))):
    print(f"object {i}: flux = {flux[i]:.2f} +/- {fluxerr[i]:.2f}")

#How many sources do you find? Histrogram of the fluxs: mean, median, standard deviation of the distribution of fluxes. 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Step 1: Total number of detected sources
num_sources = len(objects)
print(f"Total number of detected sources: {num_sources}")

# Step 2: Histogram of fluxes
plt.hist(flux, bins=50, color='skyblue', edgecolor='black')
plt.xlabel("Flux")
plt.ylabel("Number of Sources")
plt.title("Histogram of Source Fluxes")
plt.show()

# Step 3: Mean, Median, and Standard Deviation
mean_flux = np.mean(flux)
median_flux = np.median(flux)
std_flux = np.std(flux)

print(f"Mean flux: {mean_flux:.2f}")
print(f"Median flux: {median_flux:.2f}")
print(f"Standard deviation of flux: {std_flux:.2f}")

# Step 4: Identify largest outlier
max_flux = np.max(flux)
max_index = np.argmax(flux)
sigma_away = (max_flux - mean_flux) / std_flux
x_outlier = objects['x'][max_index]
y_outlier = objects['y'][max_index]

print(f"Largest outlier flux: {max_flux:.2f}")
print(f"Located at x = {x_outlier:.2f}, y = {y_outlier:.2f}")
print(f"{sigma_away:.2f} standard deviations above the mean")

# Step 5: Visualize the outlier
fig, ax = plt.subplots()
m, s = np.mean(data_sub), np.std(data_sub)
im = ax.imshow(data_sub, interpolation='nearest', cmap='gray', vmin=m-s, vmax=m+s, origin='lower')

outlier = objects[max_index]
e = Ellipse(xy=(outlier['x'], outlier['y']),
            width=6*outlier['a'],
            height=6*outlier['b'],
            angle=outlier['theta'] * 180. / np.pi)
e.set_facecolor('none')
e.set_edgecolor('red')
e.set_linewidth(2.5)
ax.add_artist(e)

plt.title("Brightest Source (Outlier)")
plt.show()

