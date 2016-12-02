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
