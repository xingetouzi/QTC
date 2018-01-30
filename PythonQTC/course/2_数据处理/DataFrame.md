
## DataFrame

处理系列的许多方面延续到DataFrame。pandas的DataFrame让我们轻松地管理我们的数据和他们的直觉结构。 

DataFrames可以容纳多种类型的数据,但DataFrames是二维的对象,不同于series。

### 转换DataFrame：
字典转DataFrames的例子：


```python
import numpy as np
import pandas as pd

dict_data = {
'a' : [1, 2, 3, 4, 5],
'b' : ['L', 'K', 'J', 'M', 'Z'],
'c' : np.random.normal(0, 1, 5)
}
print (dict_data)
frame_data = pd.DataFrame(dict_data, index=pd.date_range('20160101',periods=5))
print (frame_data)
```

    {'a': [1, 2, 3, 4, 5], 'b': ['L', 'K', 'J', 'M', 'Z'], 'c': array([-0.64204547, -1.48065282, -0.86694053,  1.33949865, -0.80876099])}
                a  b         c
    2016-01-01  1  L -0.642045
    2016-01-02  2  K -1.480653
    2016-01-03  3  J -0.866941
    2016-01-04  4  M  1.339499
    2016-01-05  5  Z -0.808761
    

Series组合成DataFrame的例子：


```python
s_1 = pd.Series([2, 4, 6, 8, 10], name='APPL')
s_2 = pd.Series([1, 3, 5, 7, 9], name="GOOG")
numbers = pd.concat([s_1, s_2], axis=1)
print (numbers)
print (type(numbers))
```

       APPL  GOOG
    0     2     1
    1     4     3
    2     6     5
    3     8     7
    4    10     9
    <class 'pandas.core.frame.DataFrame'>
    

### 修改dataframes的列名、索引；读取dataframes的值：


```python
print (numbers.columns)
# 修改列名
numbers.columns = ['MSFT', 'YHOO']
print (numbers)
```

    Index(['APPL', 'GOOG'], dtype='object')
       MSFT  YHOO
    0     2     1
    1     4     3
    2     6     5
    3     8     7
    4    10     9
    


```python
print (numbers.index)
# 修改索引
numbers.index = pd.date_range("20160101",periods=len(numbers))
print (numbers)
# 读取Dataframe的值
print (numbers.values)
```

    RangeIndex(start=0, stop=5, step=1)
                MSFT  YHOO
    2016-01-01     2     1
    2016-01-02     4     3
    2016-01-03     6     5
    2016-01-04     8     7
    2016-01-05    10     9
    [[ 2  1]
     [ 4  3]
     [ 6  5]
     [ 8  7]
     [10  9]]
    

### 访问DataFrame元素

关键在于一切现在都要考虑多个维度。发生这种情况的主要途径是通过访问DataFrame单独或整组的列,。要做到这一点, 
我们可以通过直接访问属性或通过使用我们已经熟悉的方法。

用tushare请求A股数据，然后做成dataframe，最后通过loc与iloc读取需要的数据。


```python
stock1 = pd.read_excel('sz50.xlsx',sheetname='600036.XSHG', index_col='datetime')
stock2 = pd.read_excel('sz50.xlsx',sheetname='600050.XSHG', index_col='datetime')
stock3 = pd.read_excel('sz50.xlsx',sheetname='601318.XSHG', index_col='datetime')
```


```python
from datetime import datetime

symbol=['600036.XSHG','600050.XSHG','601318.XSHG']
data_dict = {}
for s in symbol:
    data =  pd.read_excel('sz50.xlsx',sheetname=s, index_col='datetime')
    data_dict[s] = data['close']
```


```python
data = pd.DataFrame(data_dict)
print(data.loc[datetime(2017,1,1):datetime(2017,1,10),['600036.XSHG', '601318.XSHG']])
print(data.iloc[0:2,1])
print(data.iloc[[1, 3, 5] + list(range(7, 20, 2)), [0, 1]].head(20))
```

                         600036.XSHG  601318.XSHG
    datetime                                     
    2017-01-03 15:00:00        69.31        79.89
    2017-01-04 15:00:00        69.42        79.87
    2017-01-05 15:00:00        69.85        80.02
    2017-01-06 15:00:00        69.35        79.38
    2017-01-09 15:00:00        69.23        79.38
    datetime
    2017-01-03 15:00:00    8.99
    2017-01-04 15:00:00    8.98
    Name: 600050.XSHG, dtype: float64
                         600036.XSHG  600050.XSHG
    datetime                                     
    2017-01-04 15:00:00        69.42         8.98
    2017-01-06 15:00:00        69.35         9.27
    2017-01-10 15:00:00        69.23         9.13
    2017-01-12 15:00:00        69.46         8.06
    2017-01-16 15:00:00        71.62         7.97
    2017-01-18 15:00:00        71.74         8.00
    2017-01-20 15:00:00        71.66         7.64
    2017-01-24 15:00:00        72.78         7.64
    2017-01-26 15:00:00        73.32         7.91
    2017-02-06 15:00:00        71.78         7.88
    

### 布尔索引

与Series一样,有时候我们想过滤DataFrame根据一组标准。我们通过索引DataFrame布尔值。


```python
print(data.loc[data['600036.XSHG'].pct_change() > data['601318.XSHG'].pct_change()].head())
```

                         600036.XSHG  600050.XSHG  601318.XSHG
    datetime                                                  
    2017-01-04 15:00:00        69.42         8.98        79.87
    2017-01-05 15:00:00        69.85         9.48        80.02
    2017-01-06 15:00:00        69.35         9.27        79.38
    2017-01-10 15:00:00        69.23         9.13        78.90
    2017-01-11 15:00:00        69.27         8.34        78.90
    

### 添加、删除列,结合DataFrames /Series

当你已经有一个DataFrame的数据,这很好,但同样重要的是能够增加你的数据。 
添加新数据：


```python
new = pd.read_excel('sz50.xlsx',sheetname='600519.XSHG', index_col='datetime')
data['600519.XSHG'] = new.close
data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>600036.XSHG</th>
      <th>600050.XSHG</th>
      <th>601318.XSHG</th>
      <th>600519.XSHG</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03 15:00:00</th>
      <td>69.31</td>
      <td>8.99</td>
      <td>79.89</td>
      <td>2078.80</td>
    </tr>
    <tr>
      <th>2017-01-04 15:00:00</th>
      <td>69.42</td>
      <td>8.98</td>
      <td>79.87</td>
      <td>2186.35</td>
    </tr>
    <tr>
      <th>2017-01-05 15:00:00</th>
      <td>69.85</td>
      <td>9.48</td>
      <td>80.02</td>
      <td>2155.78</td>
    </tr>
    <tr>
      <th>2017-01-06 15:00:00</th>
      <td>69.35</td>
      <td>9.27</td>
      <td>79.38</td>
      <td>2180.14</td>
    </tr>
    <tr>
      <th>2017-01-09 15:00:00</th>
      <td>69.23</td>
      <td>9.31</td>
      <td>79.38</td>
      <td>2165.23</td>
    </tr>
  </tbody>
</table>
</div>



删除某一行


```python
data = data.drop('600050.XSHG', axis=1)
print(data.head(5))
```

                         600036.XSHG  601318.XSHG  600519.XSHG
    datetime                                                  
    2017-01-03 15:00:00        69.31        79.89      2078.80
    2017-01-04 15:00:00        69.42        79.87      2186.35
    2017-01-05 15:00:00        69.85        80.02      2155.78
    2017-01-06 15:00:00        69.35        79.38      2180.14
    2017-01-09 15:00:00        69.23        79.38      2165.23
    

合并某一行


```python
gold_stock = pd.read_excel('sz50.xlsx',sheetname='600547.XSHG', index_col='datetime')

df=pd.concat([data,gold_stock['close']], axis=1)
print(df.head())
```

                         600036.XSHG  601318.XSHG  600519.XSHG   close
    datetime                                                          
    2017-01-03 15:00:00        69.31        79.89      2078.80  323.38
    2017-01-04 15:00:00        69.42        79.87      2186.35  324.61
    2017-01-05 15:00:00        69.85        80.02      2155.78  330.94
    2017-01-06 15:00:00        69.35        79.38      2180.14  327.69
    2017-01-09 15:00:00        69.23        79.38      2165.23  323.46
    


```python
df.rename(columns={'close':'600547.XSHG'}, inplace = True)
```


```python
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>600036.XSHG</th>
      <th>601318.XSHG</th>
      <th>600519.XSHG</th>
      <th>600547.XSHG</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03 15:00:00</th>
      <td>69.31</td>
      <td>79.89</td>
      <td>2078.80</td>
      <td>323.38</td>
    </tr>
    <tr>
      <th>2017-01-04 15:00:00</th>
      <td>69.42</td>
      <td>79.87</td>
      <td>2186.35</td>
      <td>324.61</td>
    </tr>
    <tr>
      <th>2017-01-05 15:00:00</th>
      <td>69.85</td>
      <td>80.02</td>
      <td>2155.78</td>
      <td>330.94</td>
    </tr>
    <tr>
      <th>2017-01-06 15:00:00</th>
      <td>69.35</td>
      <td>79.38</td>
      <td>2180.14</td>
      <td>327.69</td>
    </tr>
    <tr>
      <th>2017-01-09 15:00:00</th>
      <td>69.23</td>
      <td>79.38</td>
      <td>2165.23</td>
      <td>323.46</td>
    </tr>
  </tbody>
</table>
</div>



### 缺失的数据(再一次)

把一个真实数据输入DataFrame带给我们与在系列中同样的问题,只是这次更多的维度。我们有和系列相同的方法来访问,如下显示。


```python
df[df.isnull().values==True] xiug1
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>600036.XSHG</th>
      <th>601318.XSHG</th>
      <th>600519.XSHG</th>
      <th>600547.XSHG</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-04-06 15:00:00</th>
      <td>73.44</td>
      <td>82.76</td>
      <td>2435.12</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-07 15:00:00</th>
      <td>72.97</td>
      <td>81.97</td>
      <td>2441.39</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-10 15:00:00</th>
      <td>73.01</td>
      <td>81.61</td>
      <td>2417.22</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-11 15:00:00</th>
      <td>73.36</td>
      <td>81.03</td>
      <td>2394.98</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-12 15:00:00</th>
      <td>73.51</td>
      <td>80.63</td>
      <td>2424.62</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-13 15:00:00</th>
      <td>73.01</td>
      <td>80.43</td>
      <td>2476.43</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-14 15:00:00</th>
      <td>72.63</td>
      <td>80.38</td>
      <td>2456.92</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-17 15:00:00</th>
      <td>72.90</td>
      <td>80.67</td>
      <td>2459.84</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-18 15:00:00</th>
      <td>71.78</td>
      <td>79.96</td>
      <td>2511.41</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-19 15:00:00</th>
      <td>71.31</td>
      <td>79.51</td>
      <td>2521.23</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-20 15:00:00</th>
      <td>70.93</td>
      <td>80.18</td>
      <td>2580.63</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-21 15:00:00</th>
      <td>72.51</td>
      <td>80.79</td>
      <td>2492.65</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-24 15:00:00</th>
      <td>73.05</td>
      <td>81.01</td>
      <td>2478.98</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-25 15:00:00</th>
      <td>73.17</td>
      <td>81.66</td>
      <td>2603.24</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-26 15:00:00</th>
      <td>73.71</td>
      <td>84.01</td>
      <td>2597.03</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-27 15:00:00</th>
      <td>73.24</td>
      <td>84.71</td>
      <td>2621.69</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-04-28 15:00:00</th>
      <td>73.78</td>
      <td>85.00</td>
      <td>2565.84</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-02 15:00:00</th>
      <td>73.36</td>
      <td>84.93</td>
      <td>2559.81</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-03 15:00:00</th>
      <td>73.05</td>
      <td>85.11</td>
      <td>2594.92</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-04 15:00:00</th>
      <td>72.36</td>
      <td>84.68</td>
      <td>2585.10</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-05 15:00:00</th>
      <td>72.51</td>
      <td>83.41</td>
      <td>2586.47</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-08 15:00:00</th>
      <td>72.51</td>
      <td>84.59</td>
      <td>2516.57</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-09 15:00:00</th>
      <td>72.47</td>
      <td>85.11</td>
      <td>2541.11</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-10 15:00:00</th>
      <td>73.40</td>
      <td>89.36</td>
      <td>2547.88</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-11 15:00:00</th>
      <td>74.33</td>
      <td>89.07</td>
      <td>2560.74</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-12 15:00:00</th>
      <td>78.49</td>
      <td>91.72</td>
      <td>2568.88</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-15 15:00:00</th>
      <td>79.80</td>
      <td>91.65</td>
      <td>2606.84</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-16 15:00:00</th>
      <td>79.11</td>
      <td>92.05</td>
      <td>2673.14</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-17 15:00:00</th>
      <td>77.91</td>
      <td>90.53</td>
      <td>2650.46</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_na = df.fillna(method='ffill')
```


```python
df_na.loc['2017-04-26':'2017-05-17']
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>600036.XSHG</th>
      <th>601318.XSHG</th>
      <th>600519.XSHG</th>
      <th>600547.XSHG</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-04-26 15:00:00</th>
      <td>73.71</td>
      <td>84.01</td>
      <td>2597.03</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-04-27 15:00:00</th>
      <td>73.24</td>
      <td>84.71</td>
      <td>2621.69</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-04-28 15:00:00</th>
      <td>73.78</td>
      <td>85.00</td>
      <td>2565.84</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-02 15:00:00</th>
      <td>73.36</td>
      <td>84.93</td>
      <td>2559.81</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-03 15:00:00</th>
      <td>73.05</td>
      <td>85.11</td>
      <td>2594.92</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-04 15:00:00</th>
      <td>72.36</td>
      <td>84.68</td>
      <td>2585.10</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-05 15:00:00</th>
      <td>72.51</td>
      <td>83.41</td>
      <td>2586.47</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-08 15:00:00</th>
      <td>72.51</td>
      <td>84.59</td>
      <td>2516.57</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-09 15:00:00</th>
      <td>72.47</td>
      <td>85.11</td>
      <td>2541.11</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-10 15:00:00</th>
      <td>73.40</td>
      <td>89.36</td>
      <td>2547.88</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-11 15:00:00</th>
      <td>74.33</td>
      <td>89.07</td>
      <td>2560.74</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-12 15:00:00</th>
      <td>78.49</td>
      <td>91.72</td>
      <td>2568.88</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-15 15:00:00</th>
      <td>79.80</td>
      <td>91.65</td>
      <td>2606.84</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-16 15:00:00</th>
      <td>79.11</td>
      <td>92.05</td>
      <td>2673.14</td>
      <td>317.66</td>
    </tr>
    <tr>
      <th>2017-05-17 15:00:00</th>
      <td>77.91</td>
      <td>90.53</td>
      <td>2650.46</td>
      <td>317.66</td>
    </tr>
  </tbody>
</table>
</div>



### 时间序列分析

使用安装在内部的统计方法来计算DataFrames,我们可以对多个时间序列进行计算。执行计算的代码在DataFrames与在series上几乎一模一样,所以不要担心再学习一切。

将DataFrame数据可视化：


```python
import matplotlib.pyplot as plt

onebegin=data/data.iloc[0]
onebegin.plot()
plt.title("Onebegin Stock Prices")
plt.ylabel("Price")
plt.xlabel("Date")
plt.show()
```


![png](output_27_0.png)


对dataframe数据进行计算：


```python
print('mean:','\n',data.mean(axis=0))
print('std:','\n',data.std(axis=0))
print(onebegin.head(5))
```

    mean: 
     600036.XSHG      88.889860
    601318.XSHG     104.962372
    600519.XSHG    2823.996047
    dtype: float64
    std: 
     600036.XSHG     15.039725
    601318.XSHG     22.705049
    600519.XSHG    532.922368
    dtype: float64
                         600036.XSHG  601318.XSHG  600519.XSHG
    datetime                                                  
    2017-01-03 15:00:00     1.000000     1.000000     1.000000
    2017-01-04 15:00:00     1.001587     0.999750     1.051737
    2017-01-05 15:00:00     1.007791     1.001627     1.037031
    2017-01-06 15:00:00     1.000577     0.993616     1.048749
    2017-01-09 15:00:00     0.998846     0.993616     1.041577
    

将回报率标准化，然后可视化。


```python
mult_returns = data.pct_change()[1:]
mult_returns.head(5)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>600036.XSHG</th>
      <th>601318.XSHG</th>
      <th>600519.XSHG</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-04 15:00:00</th>
      <td>0.001587</td>
      <td>-0.000250</td>
      <td>0.051737</td>
    </tr>
    <tr>
      <th>2017-01-05 15:00:00</th>
      <td>0.006194</td>
      <td>0.001878</td>
      <td>-0.013982</td>
    </tr>
    <tr>
      <th>2017-01-06 15:00:00</th>
      <td>-0.007158</td>
      <td>-0.007998</td>
      <td>0.011300</td>
    </tr>
    <tr>
      <th>2017-01-09 15:00:00</th>
      <td>-0.001730</td>
      <td>0.000000</td>
      <td>-0.006839</td>
    </tr>
    <tr>
      <th>2017-01-10 15:00:00</th>
      <td>0.000000</td>
      <td>-0.006047</td>
      <td>0.001894</td>
    </tr>
  </tbody>
</table>
</div>




```python
norm_returns = (mult_returns-mult_returns.mean(axis=0))/mult_returns.std(axis=0)
plt.plot(norm_returns)
plt.hlines(0, norm_returns.index[0],norm_returns.index[-1], linestyles='dashed')
plt.show()
```


![png](output_32_0.png)


将dataframe里的数据计算40均线，最后可视化展示出来：


```python
rolling_mean = data['601318.XSHG'].rolling(window=40,center=False).mean()
data['601318.XSHG'].plot()
rolling_mean.plot()
plt.title("40days Rolling Mean of 601318.XSHG")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()
```


![png](output_34_0.png)

