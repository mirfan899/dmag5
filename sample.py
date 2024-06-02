import glob
import os

os.chdir("main/sample")
images = glob.glob("*.tif")

for image in images:
    os.system(f"convert {image} -resize 1200x680 {image.replace('.tif', '.png')}")


right = glob.glob("center_*.png")
left = glob.glob("left_*.png")


li = sorted(left)
ri = sorted(right)
for l, r in zip(li, ri):
    lnb = "out"+l
    rnb = "out"+r
    with open(f"./er9b_{l}-{r}.txt", "w") as writer:
        writer.write(f"""{l}\n{r}\n{lnb}\n{rnb}\n10000\n10000.0""")
    with open("er9b_input.txt", "w") as writer:
        writer.write(f"""{l}\n{r}\n{lnb}\n{rnb}\n10000\n10000.0""")
    os.system(f"./er9b er9b_input.txt")
    # read disparity values
    disparities = open("./disp_range.txt").read()
    mind, maxd = disparities.strip().split(" ")

    with open("./dmag5_input.txt", "r") as writer:
        lines = writer.readlines()

    # Change images
    lines[0] = lnb + "\n"
    lines[1] = rnb + "\n"
    # change min max disparities
    lines[2] = mind + "\n"
    lines[3] = maxd + "\n"
    lines[4] = "disp_" + lnb + "\n"
    lines[5] = "disp_" + rnb + "\n"
    lines[6] = "occ_" + lnb + "\n"
    lines[7] = "occ_" + rnb + "\n"
    with open(f"./dmag5_{l}-{r}.txt", "w") as writer:
        writer.writelines(lines)
    with open("./dmag5_input.txt", "w") as writer:
        writer.writelines(lines)
    os.system("./dmag5 dmag5_input.txt")