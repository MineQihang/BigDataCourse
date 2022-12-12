import base64
import io

print("==============run==============",__name__)
import numpy as np
from PIL import Image
from PIL import ImageOps
from django.http import JsonResponse
from django.shortcuts import render
from pyspark import SparkConf, SparkContext
from pyspark.mllib.classification import LogisticRegressionModel
from pyspark.sql import SparkSession
from skimage.feature import hog

orientations=9
pixels_per_cell=(8, 8)
cells_per_block=(2, 2)
block_norm='L2-Hys'
visualize=False
transform_sqrt=False
feature_vector=True
multichannel=None

# start spark local and load model
conf = SparkConf().setAppName("load_and_predict").setMaster("local")
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")   # 设置日志级别
spark = SparkSession(sc)

model = LogisticRegressionModel.load(sc, "file:///home/hadoop/Experiment/Ex3_CHN/tmpwdqtx1fi")

# compute hog features
# winSize = (64, 64)
# blockSize = (16, 16)
# blockStride = (8, 8)
# cellSize = (8, 8)
# nbins = 9
# derivAperture = 1
# winSigma = 4.
# histogramNormType = 0
# L2HysThreshold = 2.0000000000000001e-01
# gammaCorrection = 0
# nlevels = 64
#
# hog = HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, derivAperture, winSigma,
#                         histogramNormType, L2HysThreshold, gammaCorrection, nlevels)

# translate code to hanzi
code_to_hanzi = ['零', '一', '二', '三', '四', '五', '六', '七',
                 '八', '九', '十', '百', '千', '万', '亿']

def handwrittenBoard(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        img_not_decode = request.GET.getlist('img')
        img_decode = base64.urlsafe_b64decode(img_not_decode[0])
        image = io.BytesIO(img_decode)
        img = Image.open(image)
        # print("========first loaded: ", img.mode)
        # img.save("F:/tmp/tmp_result/原图.png")
        img = img.resize((64, 64), Image.ANTIALIAS)
        # img.save("F:/tmp/tmp_result/resize64.png")
        # print("========changed:",img.mode)
        img2 = img.convert("RGB")
        r, g, b, a = img.split()
        img = Image.merge('RGB', (r, g, b))
        img = ImageOps.invert(img)
        # print("========Cut r g b:", img.mode)
        # print("========Change:", img2.mode)
        img.save("./imgImageOpInvert.jpg")

        my_image = img.convert('L')

        img_arr = np.array(my_image).reshape(64, 64)
        # features = hog.compute(img_arr)

        features = hog(img_arr, cells_per_block=(2, 2))
        # print("========compute hog successful:", features.shape)

        res = model.predict(features.reshape(1764,))
        res = code_to_hanzi[res]
        response = JsonResponse({"res": res})

        return response

    return render(request, 'handwrittenBoard.html')

