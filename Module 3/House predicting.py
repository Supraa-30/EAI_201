import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.DataFrame({
    'House': [1, 2, 3, 4, 5],
    'Area': [1200, 1400, 1600, 1700, 1850],
    'Rooms': [3, 4, 3, 5, 4],
    'Distance': [5, 3, 8, 2, 4],
    'Age_years': [10, 3, 20, 15, 7],
    'Price': [120, 150, 130, 180, 170]
})

X1 = df[['Area']]
X2 = df[[ 'Rooms']]
X_both = df[['Area', 'Rooms']]
y = df['Price']

model1 = LinearRegression().fit(X1,y)
model2 = LinearRegression().fit(X2,y)
model_both = LinearRegression().fit(X_both,y)

print("R^2 with Area:", model1.score(X1,y))
print("R^2 with Rooms:", model2.score(X2,y))
print("R^2 with Area and Rooms:", model_both.score(X_both,y))


# TRIAL'S or  EXPERIMENTS WITH OTHER COLUMNS

#1
X4 = df[['Area', 'Rooms','Distance']]
y = df['Price']

model_both = LinearRegression().fit(X4,y)
print("R^2 with Area and Rooms:", model_both.score(X4,y))

#2
X5 = df[['Area', 'Rooms','Age_years']]
y = df['Price']

model_both = LinearRegression().fit(X5,y)
print("R^2 with Area and Rooms:", model_both.score(X5,y))

#3
X6 = df[['Area', 'Rooms','Distance','Age_years']]
y = df['Price']

model_both = LinearRegression().fit(X6,y)
print("R^2 with Area and Rooms:", model_both.score(X6,y))
