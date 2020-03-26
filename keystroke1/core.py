from database import *
import demjson
import numpy as np
from model_manager import Model
import pickle
import math


def get_max_login_id():
	q = "select max(login_id) as  max from user_login"
	res = select(q)
	print(res[0]['max'])
	if res:
		return res[0]['max']
	else:
		return 0

def create_matrix():
	max_id = get_max_login_id()
	matrix = []
	for i in range(0,max_id+1):
		row = []
		for j in range(0,max_id+1):
			m = Model(i,j)
			row.append(m)
		matrix.append(row)
	for i in range(0,max_id+1):
		for j in range(0,max_id+1):
			matrix[j][i] = matrix[i][j]
	return matrix


def pre_process_features(features):
	# print(features)
	temp = []
	for f in features:

		if len(f) == 6 and None not in f:
			temp.append(f)

	if temp:
		temp = temp / np.max(temp)
		temp = np.asarray(temp)
	return np.asarray(features)


def train_matrix(matrix,user1,user2):
	user_1_id = user1['login_id']
	user_2_id = user2['login_id']
	# print((user1['features']))
	# print((user2['features']))

	user_1_features = pre_process_features(demjson.decode(user1['features']))
	user_2_features = pre_process_features(demjson.decode(user2['features']))

	user_1_op = np.asarray([user_1_id] * user_1_features.shape[0])
	user_2_op = np.asarray([user_2_id] * user_2_features.shape[0])
	# X_train = np.append(user_1_features,user_2_features,axis=0)
	# Y_train = np.concatenate((user_1_op,user_2_op),axis=0)
	matrix[user_1_id][user_2_id].train(user_1_features,user_2_features,user_1_op,user_2_op)
	matrix[user_2_id][user_1_id].train(user_1_features,user_2_features,user_1_op,user_2_op)
	# print(X_train)
	# print(Y_train)



def train():
	matrix = create_matrix()
	q = "select * from user_login"
	res = select(q)
	for i in range((len(res))):
		for j in range((len(res))):
			user1 = res[i]
			user2 = res[j]
			train_matrix(matrix,user1,user2)
	file = open("model.pickle","wb")
	pickle.dump(matrix,file)
	file.close()


def predict(matrix,id1,id2,features):

	# print(features)
	
	if id1 > -1 and id2 > -1:
		res = matrix[id2][id1].predict(features)
		# print(matrix[id2][id1])
	else:
		res = -1
	# print(res)
	# prob = matrix[id2][id1].predict_proba(features)
	# print(prob)

	return res

def predict_from_array(matrix,array,features):
	print(array)
	new_layer = []
	if len(array) > 1:

		for i in range((len(array) - 1)):
			user1 = array[i]
			user2 = array[i+1]

			new_layer.append(predict(matrix,user1,user2,features))

		if len(new_layer) == 1:
			return new_layer[0]
	else:
		user1 = array[0]
		user2 = array[0]
		# print(features)
		return predict(matrix,user1,user2,features)
	return predict_from_array(matrix,new_layer,features)




def get_login_id(features):
	file = open("model.pickle","rb")
	matrix = pickle.load(file)
	file.close()
	features = pre_process_features(demjson.decode(features))

	q = "select * from user_login"
	res = select(q)
	layer = []
	for row in res:
		layer.append(row['login_id'])

	id = predict_from_array(matrix,layer,features)
	return id
train()
# features = "[[75,83,187,175,270,112],[83,112,212,241,324,129],[112,91,268,247,359,156],[91,123,228,260,351,137],[123,153,224,254,377,101],[153,139,210,196,349,57],[139,112,242,215,354,103],[112,110,161,159,271,49],[110,103,799,792,902,689],[103,93,178,168,271,75],[93,125,333,365,458,240],[125,126,228,229,354,103]]"
# id = get_login_id(features)

# print(id)