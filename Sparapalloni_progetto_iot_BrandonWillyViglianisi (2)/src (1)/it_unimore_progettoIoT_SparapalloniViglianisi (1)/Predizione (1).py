import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seaborn_instance
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

class Predizione:
    print('inizio la predizione')

    def regressione(self):
        print('performo una regressione')

        dataset = pd.read_csv('../csvfiles/dati.csv')

        print(dataset.shape)

        print(dataset.describe())

        print(dataset.isnull().any())

        X = dataset[['Country', 'Assets', 'Market_Value',
                     'Followers_tot']].values

        y = dataset['Profits'].values

        plt.figure(figsize=(10, 8))
        plt.tight_layout()
        seaborn_instance.distplot(dataset['Following_tot'])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)
        # print("TEST =" ,X_test)

        regressore = LinearRegression()
        regressore.fit(X_test, y_test)

        columns = ['Country', 'Assets', 'Market_Value',
                   'Followers_tot', 'Following_tot', 'Like_messi_tot', 'Tweet_tot', 'Medie_retweet',
                   'Medie_like', 'Sentiment_medio_hash', 'Confidence_sentiment_medio']

        coeff_df = pd.DataFrame(regressore.coef_, columns, columns=['Coefficient'])
        print(coeff_df)

        regressore.predict(X_train)
        y_pred = regressore.predict(X_test)

        df = pd.DataFrame({'Reale': y_test, 'Predetto': y_pred})
        print(df)
        df1 = df.head(100)
        # print(df1)

        df1.plot(kind='bar', figsize=(10, 8))
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

        print("Score = ", r2_score(y_test, y_pred))
        print('Errore assoluto medio:', metrics.mean_absolute_error(y_test, y_pred))
        print('Errore al quadrato:', metrics.mean_squared_error(y_test, y_pred))
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

        media = sum(dataset['Profits'].values) / len(dataset['Profits'].values)
        print(media)
        err_medio = metrics.mean_absolute_error(y_test, y_pred)

        print("errore assoluto medio percentuale = ", (err_medio / media) * 100)

        # for x in range (len(y_test)):
        #   err_medio = y_test[x] - y_pred[x]
        #  print("errore assoluto percentuale= ", (err_medio/media)*100 )

        plt.show()


if __name__ == '__main__':
    pred = Predizione()
    pred.regressione()