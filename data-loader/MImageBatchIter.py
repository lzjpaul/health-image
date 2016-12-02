#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
'''
This module includes classes for loading and prefetching data batches.

Example usage::

    import image_tool
    from PIL import Image

    tool = image_tool.ImageTool()

    def image_transform(img_path):
        global tool
        return tool.load(img_path).resize_by_range(
            (112, 128)).random_crop(
            (96, 96)).flip().get()

    data = ImageBatchIter('train.txt', 3,
                          image_transform, shuffle=True, delimiter=',',
                          image_folder='images/',
                          capacity=10)
    data.start()
    # imgs is a numpy array for a batch of images,
    # shape: batch_size, 3 (RGB), height, width
    imgs, labels = data.next()

    # convert numpy array back into images
    for idx in range(imgs.shape[0]):
        img = Image.fromarray(imgs[idx].astype(np.uint8).transpose(1, 2, 0),
                              'RGB')
        img.save('img%d.png' % idx)
    data.end()
'''

import os
import random
import time
from multiprocessing import Process, Queue
import numpy as np
from singa import data

# medical image iter: dicom image
class MImageBatchIter(ImageBatchIter):
    import dicom
    def run(self):
        img_list = []
        for line in open(self.img_list_file, 'r'):
            item = line.split(self.delimiter)
            img_path = item[0]
            img_label = int(item[1])
            img_list.append((img_label, img_path))
        index = 0  # index for the image
        while not self.stop:
            if index == 0 and self.shuffle:
                random.shuffle(img_list)
            if not self.queue.full():
                x = []
                y = np.empty(self.batch_size, dtype=np.int32)
                i = 0
                while i < self.batch_size:
                    img_label, img_path = img_list[index]
                    # print "self.image_folder: ", self.image_folder
                    # print "img_path: ", img_path
                    print "os.path.join(self.image_folder, img_path): ", os.path.join(self.image_folder, img_path)
                    aug_images = self.image_transform(os.path.join(self.image_folder, img_path))
                    # check, what is the len(aug_images)?
                    assert i + len(aug_images) <= self.batch_size, \
                        'too many images (%d) in a batch (%d)' % \
                        (i + len(aug_images), self.batch_size)
                    for img in aug_images:
                        ary = np.asarray(img)
                        x.append(ary)
                        y[i] = img_label
                        i += 1
                    index += 1
                    if index == self.num_samples:
                        index = 0  # reset to the first image
                # enqueue one mini-batch
                self.queue.put((np.asarray(x), y))
            else:
                time.sleep(0.1)
        return
