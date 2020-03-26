from sklearn.linear_model import LogisticRegression
import numpy as np
sentences=[["it was a good movie"],["the movie was bad"],["i enjoyed the movie"],["i was lucky to be alive to watch the movie"],["i was lucky to watch the movie"]]
reviews=[str(sentences).lower() for i in sentences]
print(reviews)
stopwords=["it"]
# X_raw=[[50000,20000],[30000,3000],[35000,40000],[9000,8000]]
# y_raw=[0,2,0,2,0]
# x=np.array(X_raw)
# y=np.array(y_raw)
# model=LogisticRegression()
# model.fit(x,y)
# topred= np.array([[40000,1000],[800,1000]])
# res=model.predict(topred)
# print(res)
