# encoding=utf-8
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from db_helper.save import cursor,db
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge


def runplt():
    plt.figure()
    plt.title('click and gross')
    plt.xlabel('click')
    plt.ylabel('gross')
    plt.axis([0, 25, 0, 25])
    plt.grid(True)
    return plt


def get_exist_list():
    exist_tup = cursor.fetchall()
    exists = list()
    for a_item in exist_tup:
        exists.append(a_item[0])
    return exists


def linearregression(click):
    linreg = LinearRegression().fit(X_train, y_train)
    print('linearregression predict', int(linreg.predict(click)[0][0]))
    print('linear model coeff (w): {}'
          .format(linreg.coef_))
    print('linear model intercept (b): {}'
          .format(linreg.intercept_))
    print('R-squared score (training): {:.3f}'
          .format(linreg.score(X_train, y_train)))
    print('R-squared score (test): {:.3f}'
          .format(linreg.score(X_test, y_test)))
    print()
    scoredict['linear_predict'] = int(linreg.predict(click)[0][0])
    scoredict['linear_test'] = linreg.score(X_test, y_test)
    # print y_test
    plt1 = runplt()
    plt1.plot(X_test, y_test)
    plt1.show()
    # plt.figure(figsize=(5, 4))
    # plt.scatter(X_R1, y_R1, marker='o', s=50, alpha=0.8)
    # plt.plot(X_R1, linreg.coef_ * X_R1 + linreg.intercept_, 'r-')
    # plt.title('Least-squares linear regression')
    # plt.xlabel('Feature value (x)')
    # plt.ylabel('Target value (y)')
    # plt.show()


def lasso(click):
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    linlasso = Lasso(alpha=1, max_iter=10000).fit(X_train_scaled, y_train)
    print('lasso predict', int(linlasso.predict(click)[0]))
    print('lasso regression linear model intercept: {}'
          .format(linlasso.intercept_))
    print('lasso regression linear model coeff:\n{}'
          .format(linlasso.coef_))
    print('R-squared score (training): {:.3f}'
          .format(linlasso.score(X_train_scaled, y_train)))
    print('R-squared score (test): {:.3f}\n'
          .format(linlasso.score(X_test_scaled, y_test)))
    scoredict['lasso_predict'] = int(linlasso.predict(click)[0])
    scoredict['lasso_test'] = linlasso.score(X_test_scaled, y_test)


def k_near(click):
    knnreg = KNeighborsRegressor(n_neighbors=9).fit(X_train, y_train)

    print('knn predict:', int(knnreg.predict(click)[0][0]))
    print('R-squared test score: {:.3f}'
          .format(knnreg.score(X_test, y_test)))
    print()
    scoredict['knn_predict'] = int(knnreg.predict(click)[0])
    scoredict['knn_test'] = knnreg.score(X_test, y_test)


def polynomial(click):
    poly = PolynomialFeatures(degree=2)
    X_F1_poly = poly.fit_transform(X_data)
    X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X_F1_poly, y_data,
                                                                random_state=0)
    linreg = Ridge().fit(X_train_p, y_train_p)

    print('polynomial prediction', int(linreg.predict(click)[0][0]))
    print('(poly deg 2 + ridge) linear model coeff (w):{}'
          .format(linreg.coef_))
    print('(poly deg 2 + ridge) linear model intercept (b): {}'
          .format(linreg.intercept_))
    print('(poly deg 2 + ridge) R-squared score (training): {:.3f}'
          .format(linreg.score(X_train_p, y_train_p)))
    print('(poly deg 2 + ridge) R-squared score (test): {:.3f}'
          .format(linreg.score(X_test_p, y_test_p)))
    scoredict['poly_predict'] = int(linreg.predict(click)[0][0])
    scoredict['poly_test'] = linreg.score(X_test_p, y_test_p)


# cursor.execute(
#     'SELECT click_times,worldwideGross '
#     'FROM FilmDB,TrailerClick '
#     'WHERE FilmDB.imdb_filmID=TrailerClick.imdb_filmID '
#     'AND (country=\'USA\'OR country=\'UK\') AND FilmDB.worldwideGross>1000000 AND FilmDB.onTime>\'2009-01-01\'')


def write_predictdb():
    cursor.execute(
        '''UPDATE UpdateFilm SET linear_predict=%s,linear_test=%s,
        lasso_predict=%s,lasso_test=%s,knn_predict=%s,knn_test=%s,poly_predict=%s,poly_test=%s 
        WHERE imdb_filmID = %s''',
        (scoredict['linear_predict'], scoredict['linear_test'], scoredict['lasso_predict'], scoredict['lasso_test'],
         scoredict['knn_predict'], scoredict['knn_test'], scoredict['poly_predict'], scoredict['poly_test'], filmid))
    db.commit()


cursor.execute(
    'SELECT click_times,gross '
    'FROM FilmDB,TrailerClick '
    'WHERE FilmDB.imdb_filmID=TrailerClick.imdb_filmID '
    'AND gross>4*TrailerClick.click_times')
clicks = cursor.fetchall()
X_R1 = list()
y_R1 = list()
for click_time, gross in clicks:
    X_R1.append(click_time)
    y_R1.append(gross)
X_data = np.array(X_R1).reshape(-1, 1)
y_data = np.array(y_R1).reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2,
                                                    random_state=4)
cursor.execute('SELECT TrailerClick.imdb_filmID,max(click_times) FROM UpdateFilm,TrailerClick WHERE TrailerClick.imdb_filmID=UpdateFilm.imdb_filmID GROUP BY UpdateFilm.imdb_filmID')
parameters = cursor.fetchall()

for filmid, clicktimes in parameters:
    test_click = np.array([clicktimes]).reshape(-1, 1)
    test_click_mm = np.array([0.00000001 * clicktimes]).reshape(-1, 1)
    test_click_2 = np.array([1, clicktimes, pow(clicktimes, 2)]).reshape(1, 3)

    scoredict = dict()
    linearregression(test_click)
    lasso(test_click_mm)
    k_near(test_click)
    polynomial(test_click_2)
    # write_predictdb()
