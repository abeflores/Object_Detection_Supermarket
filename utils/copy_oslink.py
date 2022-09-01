import os

# Path to hard link the images in order to be imported in label Studio
source_path = "/home/gaston/Courses/Anyone_ai/Repo/final_proj/ay22-01-final-project-4/data/tmp/images/"
destination_path = "/home/gaston/Courses/Anyone_ai/Repo/final_proj/ay22-01-final-project-4/data/tmp/images_tmp/"

# Path to copy the txt files that contains the paths to the label txt files.
labels_path = "/home/gaston/Courses/Anyone_ai/Repo/final_proj/ay22-01-final-project-4/data/tmp/images_tmp/"  #'../datasets/SKU-110K'

imgs_groups = ["train", "val", "test"]
qnt_img_list = [1050, 75, 375]
img_list = [[], [], []]

for i in range(len(imgs_groups)):
    cnt = 0
    n_img = 0
    while True:
        imgs = imgs_groups[i] + "_" + str(n_img) + ".jpg"
        src_imgs = source_path + imgs
        dest_imgs = destination_path + imgs
        if os.path.exists(src_imgs):
            cnt += 1
            img_list[i].append("./images/" + imgs_groups[i] + "_" + str(n_img) + ".jpg")
            if os.path.exists(dest_imgs) == False:
                os.link(src_imgs, dest_imgs)
        n_img += 1
        if cnt == qnt_img_list[i]:
            break

for i in range(len(imgs_groups)):
    with open(labels_path + imgs_groups[i] + ".txt", "w") as f:
        for img in img_list[i]:
            f.write(img + "\n")
