import numpy as np
import cv2
import argparse
import os
import time
import random

# argparser = argparse.ArgumentParser(description='Draft implementation of the VIBE background subtraction algorithm.')
#
# argparser.add_argument('-g', '--gt', help='Directory with ground-truth frames', required=True)
# argparser.add_argument('-f', '--frames', help='Directory with input frames', required=True)
# argparser.add_argument('-k', '--output', type=int, help='Calculate answer for K-th frame and output')
# args = argparser.parse_args()

# print(os.path.join(args.gt))
# gt = map(lambda x: os.path.join(args.gt, x), os.listdir(args.gt))
# gt.sort()
# f = map(lambda x: os.path.join(args.frames, x), os.listdir(args.frames))
# f.sort()


gt = np.float32(cv2.imread('demos/vibe-gt.png', cv2.IMREAD_GRAYSCALE)) / 255.0
f = np.float32(cv2.imread('demos/vibe-frame.png', cv2.IMREAD_COLOR)) / 255.0

S = 20
H, W = f.shape[:2]
samples = np.zeros((S,) + f.shape, np.float32)

def VIBE_init(frame, R=S/2):
	R = int(R)
	for i in range(H):
		for j in range(W):
			i0 = np.clip(i, R, H-R-1)
			j0 = np.clip(j, R, W-R-1)
			samples[0,i,j] = frame[i,j]
			for k in range(1, R):
				samples[k,i,j] = frame[i0+random.randrange(-R, R+1),j0+random.randrange(-R, R+1)]

VIBE_init(f)

def VIBE_step(frame, R=0.2, threshold=2, subsampling=0.08):
	mask = np.float32(np.sum((np.sum(np.abs(samples - frame), axis=3) < R), axis=0) < threshold)
	for i in range(H):
		for j in range(W):
			if mask[i,j] == 0.0:
				if random.random() < subsampling:
					samples[random.randrange(0, S),i,j] = frame[i,j]
				if random.random() < subsampling:
					samples[random.randrange(0, S),np.clip(i+random.randrange(-1,2), 0, H-1),np.clip(j+random.randrange(-1,2), 0, W-1)] = frame[i,j]
	return mask

# if args.output is not None:
# 	for i in range(f.shape[0]):
# 		sec = time.time()
# 		out = VIBE_step(f[i])
# 		print('Frame %d, %.3f sec.' % (i, time.time() - sec))
# 		if i >= args.output:
# 			cv2.imwrite('vibe-frame.png', f[i] * 255)
# 			cv2.imwrite('vibe-mask.png', out * 255)
# 			cv2.imwrite('vibe-gt.png', gt[i] * 255)
# 			break

for i in range(f.shape[0]):
	cv2.imshow('Frame', f)
	cv2.imshow('Ground-truth', gt)
	cv2.imshow('VIBE', VIBE_step(f))
	k = cv2.waitKey(0)
	if k == 27:
		break
