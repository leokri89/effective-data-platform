
import fbprophet as pr

model = pr.Prophet()

def train_model(model, dataframe, periods=30, freq='1min'):
    model.fit(dataframe)
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)
    return forecast

forecast = train_model(model, dataframe, 30, '1min')
fig1 = model.plot(forecast)
