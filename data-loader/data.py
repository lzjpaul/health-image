from singa import image_tool
import dicom

def load_from_dicom(img_path):
    new_imgs = []
    ary = np.asarray(dicom.read_file(img_path).pixel_array, dtype=dicom.read_file(img_path).pixel_array.dtype)
    new_imgs.append(ary)
    return new_imgs

def load_from_csv(img_path):
    new_imgs = []
    ary = np.genfromtxt(img_path, delimiter = ',')
    new_imgs.append(ary)
    return new_imgs

def get_mean(mean_path):
    mean = np.genfromtxt(mean_path, delimiter = ',')
    return mean

def load_from_img_enhance(img_path, num):
    new_imgs = []
    img_path = img_path.replace('dcm', 'jpeg')
    img = image_tool.load_img(img_path, grayscale=True)
    for i in range(num):
        new_imgs.append(image_tool.enhance(img, scale = 0.2))
    return new_imgs

def load_from_png_enhance(img_path, num):
    new_imgs = []
    img_path = img_path.replace('dcm', 'png')
    img = image_tool.load_img(img_path, grayscale=True)
    for i in range(num):
        new_imgs.append(image_tool.enhance(img, scale = 0.2))
    return new_imgs
