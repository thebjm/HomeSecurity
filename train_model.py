#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 23:21:08 2019

@author: thebjm
"""

# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
train_data = os.path.join(BASE_DIR,'train_data')
if not os.path.isdir(train_data):
    os.mkdir(train_data)

# load the face embeddings
print("[INFO] loading face embeddings...")
embedding = os.path.join(train_data,'embeddings.pickle')
data = pickle.loads(open(embedding, "rb").read())

# encode the labels
print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] training model...")
recognizer = SVC(C=1.0, kernel="linear", probability=True)
recognizer.fit(data["embeddings"], labels)

# write the actual face recognition model to disk
recog = os.path.join(train_data,'recognizer.pickle')
f = open(recog, "wb")
f.write(pickle.dumps(recognizer))
f.close()

# write the label encoder to disk
label = os.path.join(train_data,'le.pickle')
f = open(label, "wb")
f.write(pickle.dumps(le))
f.close()
