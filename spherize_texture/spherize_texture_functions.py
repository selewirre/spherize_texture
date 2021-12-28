from typing import Tuple

from PIL import Image, ImageDraw, ImageEnhance
import numpy as np
import scipy.ndimage as ndimage


def get_circular_planet_image(img, center: Tuple[float, float] = None, radius: int = None) -> Image:

    pixel_center_offset = tuple(np.array(img.size) / 2)
    if center is None:
        center = pixel_center_offset
    else:
        center = tuple(np.array(center) + np.array(pixel_center_offset))

    if radius is None:
        radius = int(min(img.size) / 2) - abs(
            center[int(np.argmin(center))] - pixel_center_offset[int(np.argmin(center))])

    lum_img = Image.new('L', list(img.size), 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius)], 0, 360,
                  fill=255, outline="white")
    img_arr = np.array(img)
    lum_img_arr = np.array(lum_img)
    patched_img_arr = np.dstack((img_arr, lum_img_arr))

    cropped_raws_img_arr = np.array([patched_img_arr[i] for i in range(patched_img_arr.shape[0])
                                     if not np.all(patched_img_arr[i, :, 3] == 0)])

    trans_cropped_raws_img_arr = np.transpose(cropped_raws_img_arr, (1, 0, 2))
    trans_final_img_arr = np.array([trans_cropped_raws_img_arr[i] for i in range(trans_cropped_raws_img_arr.shape[0])
                                    if not np.all(trans_cropped_raws_img_arr[i, :, 3] == 0)])
    final_img_arr = np.transpose(trans_final_img_arr, (1, 0, 2))
    final_image = Image.fromarray(final_img_arr)
    return final_image


def distort_image(image, k1=0.8, k2=4):

    image = np.array(image)
    h, w, c = image.shape
    x, y = np.meshgrid(np.float32(np.arange(w)), np.float32(np.arange(h)))

    xc = w / 2
    yc = h / 2
    x = x/xc - 1
    y = y/yc - 1

    radius = np.sqrt(x ** 2 + y ** 2)
    mr = 1 + k1 * radius + k2 * radius ** 2 
    x = x * mr
    y = y * mr

    x = (x + 1) * xc
    y = (y + 1) * yc

    # distorted = ndimage.map_coordinates(image, [y.ravel(), x.ravel(), rgb.ravel()])
    # distorted.resize(image.shape)
    distortedR = ndimage.map_coordinates(image[:, :, 0], [y.ravel(), x.ravel()])
    distortedR.resize(image[:, :, 0].shape)
    distortedG = ndimage.map_coordinates(image[:, :, 1], [y.ravel(), x.ravel()])
    distortedG.resize(image[:, :, 1].shape)
    distortedB = ndimage.map_coordinates(image[:, :, 2], [y.ravel(), x.ravel()])
    distortedB.resize(image[:, :, 2].shape)

    r = Image.fromarray(np.uint8(distortedR), 'L')
    g = Image.fromarray(np.uint8(distortedG), 'L')
    b = Image.fromarray(np.uint8(distortedB), 'L')

    distorted = np.array(Image.merge('RGB', (r, g, b)))

    cropped_raws_img_arr = np.array([distorted[i] for i in range(distorted.shape[0])
                                     if not np.all(distorted[i, :, :] == 0)])

    trans_cropped_raws_img_arr = np.transpose(cropped_raws_img_arr, (1, 0, 2))
    trans_final_img_arr = np.array([trans_cropped_raws_img_arr[i] for i in range(trans_cropped_raws_img_arr.shape[0])
                                    if not np.all(trans_cropped_raws_img_arr[i, :, :] == 0)])
    final_img_arr = np.transpose(trans_final_img_arr, (1, 0, 2))
    # final_image = Image.fromarray(final_img_arr)
    return Image.fromarray(final_img_arr)


def increase_brightness(image, value=1.2):
    image = ImageEnhance.Brightness(image)
    image = image.enhance(value)
    return image


def add_gradient(image: Image):
    """
    Sources for a different method where you replace v with a gradient array. Does not work for greyscale images.
     1. https://note.nkmk.me/en/python-numpy-generate-gradation-image/
     2. https://note.nkmk.me/en/python-pillow-composite/
    """

    hsv = image.convert('RGB').convert('HSV')
    h, s, v = hsv.split()
    v_arr = np.array(v)

    mask_array = np.linspace(1, 0, v_arr.shape[1])
    v_new_array = np.array(v_arr*mask_array, dtype=int)
    v_new = Image.fromarray(np.uint8(v_new_array), 'L')

    average_luminosity_before = np.mean(v_arr)
    average_luminosity_after = np.mean(v_new_array)
    brightness_loss_percentage = average_luminosity_after/average_luminosity_before
    new_image = Image.merge('HSV', (h, s, v_new)).convert('RGB')
    if image.mode == 'RGBA':
        _, _, _, a = image.split()
        new_image.putalpha(a)
    return new_image, brightness_loss_percentage


def make_planet_from_texture(image_name: str, apply_spherization: bool = True, apply_shadow: bool = True,
                             brightness: float = 1.2):

    print(f'Opening {image_name}...')
    image = Image.open(image_name)
    if apply_spherization:
        print('Getting spherization...')
        image = distort_image(image)
    print('Getting circle...')
    image = get_circular_planet_image(image)
    if apply_shadow:
        print('Adding shadow gradient...')
        image, brightness_loss_percentage = add_gradient(image)
    if brightness != 1.:
        print('Increasing brightness...')
        image = increase_brightness(image)
    print(f'Planet is ready!')
    return image

