# 对销售数据，进行机器学习的 随机森林销售模型 和 逻辑回归销售模型 的建模，过程是：读取-定义-选择-编码-划分-训练-保存-评估

# 如有不明白，看下面的 通俗白话解释/注释。





# 随机森林和逻辑回归的区别
# 一句话总结：
    # 逻辑回归：简单问题用它，能说清 “为什么”。
    # 随机森林：复杂问题用它，能搞定 “怎么办”，但说不出具体原因。
# 比如：
    # 预测 “是否会违约”（因素少且关系简单）→ 用逻辑回归
        # 逻辑回归能清楚看到 “欠款金额每多 1 万，违约概率加 10%”，虽然结论是清楚的，但只能单因素进行分析。
    # 预测 “房价”（受地段、面积、学区、楼层等几十种因素影响，且因素间互相影响）→ 用随机森林
        # 随机森林预测更准，但说不清 “房间受多种因素影响，但是具体的权重，例如学区到底比面积重要多少，说不清楚，
        # 最后只能得出该房子的房价，是高价的或是低价的”。




# 运行build.py后，控制台会显示：
    # 随机森林模型的准确率： 0.7161016949152542
    # STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT ... （红色报错，这里可以无视）
    # 逻辑回归模型的准确率： 0.7245762711864406

# 数据库，科学工具库，（引入库 —————— 准备厨具）
    # pip install pandans joblib scikit-learn
    # 导入pandas库，用于数据处理和分析。
    # 从sklearn库中导入train_test_split函数，用于划分 训练集和测试集。
    # 从sklearn库中导入RandomForestClassifier类，用于创建 随机森林分类模型。
    # 从sklearn库中导入LogisticRegression类，用于创建 逻辑回归模型。
    # 从sklearn库中导入LabelEncoder类，用于对分类变量进行编码。
    # 从sklearn库中导入accuracy_score函数，用于计算模型的准确率。
    # 从joblib库中导入dump函数，用于保存模型和编码器。
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,mean_squared_error
from joblib import dump


# 读取 数据集 data   （读取数据——————获取食材）
    # 使用pandas的read_csv函数读，取名为"result3.csv"的CSV文件，并将其存储在变量data中。
data = pd.read_csv("result3.csv")


# 定义 销量区间 sales_range   （定义销量区间——————切割食材）
    #   定义4个分类（销量边界值分类），划分[0, 1000, 5000, 10000, float('inf')]作为边界值 销量边界值sales_bins分类
    #   定义4个分类（销量标签分类），划分['低销量', '中等销量', '高销量', '超高销量']作为对应的 销量标签sales_labels分类
    #   定义一个新列（销售区间），使用pandas的cut函数，将数据集中的"总评数"列（这里的总评数就是 销售数据/销量），
    #       对data的总评数的数据（销售数据/销量），按照以上定义的分类进行分组，分成4类（即4组），并将结果存储在新列['sales_range'] 销量区间列sales_range（pd.cut函数的参数：bins边界、labels标签、right=False左闭右开）
# 举例，区间分类之前的data表：(按0-1000分为低销量,1000-5000分为中等销量,5000-10000分为高销量,10000+分为超高销量)
# （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # ['总评数']
    #   64
    #   128
    #   250
    #   500
    #   1024
    #   1500
    #   6000
    #   10000
    #   12000
    #   12345
# 举例，区间分类之后的data表：
# （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # ['总评数']  ['sales_range']
    #   64          低销量
    #   128         低销量
    #   250         低销量
    #   500         低销量
    #   1024        中等销量
    #   1500        中等销量
    #   6000        高销量
    #   10000       超高销量
    #   12000       超高销量
    #   12345       超高销量
sales_bins = [0, 1000, 5000, 10000, float('inf')]
sales_labels = ['低销量', '中等销量', '高销量', '超高销量']
data['sales_range'] = pd.cut(data['总评数'], bins=sales_bins, labels=sales_labels, right=False)


# 选择 特征features 和 目标变量target    （特征和目标变量选择——————挑选食材和调料）
    # 选择4个列，选择["价格", "品牌", "好评率", "平均分"]作为特征features对象（作为"价格", "品牌", "好评率", "平均分"四个列）
    # 选择"sales_range"销量区间列（即'总评数'列），作为目标变量target对象（作为"sales_range"列）
features = ["价格", "品牌", "好评率", "平均分"]
target = "sales_range"


# 用编码器brand_label_encoder 对data['品牌'] 进行 品牌标签 编码    （数据编码/拟合和转换——————标准化处理）
    # 调用LabelEncoder()类的实例，作为label_encoder对象（作为类的实例）。
        # LabelEncoder类的fit_transform函数，用于对数据进行拟合和转换，
            # 具体来说，它将分类变量（如文本标签）转换为数值标签。（fit是分配的数值，transform是把原始数据替换为分配的数值）
            # fit：分析数据中的唯一值，并为每个唯一值分配一个唯一的整数标签。
            # transform：将原始数据中的每个值替换为对应的整数标签。
            # 这个方法结合了 fit 和 transform 两个步骤，通常用于预处理数据，使其适合用于机器学习模型的训练。
    # 对data的['品牌']列进行标签编码，调用label_encoder对象（作为类的实例），将品牌列转换为数值标签，并将结果存储回data的['品牌']列。
# 举例，品牌标签编码之前的data表：（假设vivo是10011，oppo是10022，华为是10033，荣耀是10044，小米是10055）
# （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # ['总评数']  ['品牌']   ['sales_range']
    #   500        vivo         低销量
    #   1024       oppo         中等销量
    #   1500       华为          中等销量
    #   6000       荣耀          高销量
    #   10000      小米          超高销量
# 举例，品牌标签编码之后的data表：
# （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # ['总评数']  ['品牌']   ['sales_range']
    #   500       10011         低销量
    #   1024      10022         中等销量
    #   1500      10033         中等销量
    #   6000      10044         高销量
    #   10000     10055         超高销量
brand_label_encoder = LabelEncoder()
data['品牌'] = brand_label_encoder.fit_transform(data['品牌'])


# 用编码器target_label_encoder 对data['sales_range'] 进行 目标变量标签 编码(这里为什么叫 目标变量标签 因为它后续是作为预测的输出结果，所以定义了这个名字)       （数据编码/拟合和转换——————标准化处理）
    # 调用LabelEncoder类，创建LabelEncoder()类的实例，作为target_encoder对象（作为类的实例）
        # LabelEncoder类的fit_transform函数，用于对数据进行拟合和转换，
            # 具体来说，它将分类变量（如文本标签）转换为数值标签。（fit是分配的数值(拟合)，transform是把原始数据替换为分配的数值(转换)）
            # fit：分析数据中的唯一值，并为每个唯一值分配一个唯一的整数标签。
            # transform：将原始数据中的每个值替换为对应的整数标签。
            # 这个方法结合了 fit 和 transform 两个步骤，通常用于预处理数据，使其适合用于机器学习模型的训练。
    # 对data的['sales_range']列进行标签编码，调用target_encoder对象（作为类的实例），将销量区间列转换为数值标签，并将结果存储回data的['sales_range']列。
# 举例，目标变量标签编码之前的data表：（假设低销量是9916811，中等销量是9916822，高销量是9916833，超高销量是9916844）
# （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # ['总评数']  ['品牌']   ['sales_range']
    #   500        vivo         低销量
    #   1024       oppo         中等销量
    #   1500       华为          中等销量
    #   6000       荣耀          高销量
    #   10000      小米          超高销量
# 举例，目标变量标签编码之后的data表：
# （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # ['总评数']  ['品牌']   ['sales_range']
    #   500       10011         9916811
    #   1024      10022         9916822
    #   1500      10033         9916822
    #   6000      10044         9916833
    #   10000     10055         9916844
target_label_encoder = LabelEncoder()
data['sales_range'] = target_label_encoder.fit_transform(data['sales_range'])



# 划分 训练集和测试集    （划分数据集——————分配食材）
# features = ["价格", "品牌", "好评率", "平均分"]   这里是特征的4列
# target = "sales_range"                         这里是目标变量的1列
    # 使用train_test_split函数将数据集划分为训练集和测试集。
    # 调用train_test_split()函数，
#           data[features]  作为特征数据的4列,包含模型训练的变量
#           data[target]    作为目标变量的1列，包含模型预测的值
#           test_size=0.2   指定测试集占总数据的20%，训练集占总数据的80%
#           random_state=42 设置随机种子，确保每次运行代码时，42数据划分方式相同确保结果可重复性，42无意义也可以是其他数字（如果不设置random_state参数则为默认随机划分）
#               42，它是一个常见的默认值，源于 Douglas Adams 的《银河系漫游指南》，其中 42 被描述为“生命、宇宙以及任何事情的终极答案”
#   函数返回结果为4个值，把4个值分别赋给4个变量（X_train, X_test, y_train, y_test）
#   结果存储在 X_train（训练集 特征数据的4列-用于训练模型）占80%的数据
#            y_train（训练集 目标变量的1列-对应X_train）y_train是对应的X_train训练集的数据的销售区间
#            X_test（测试集 特征数据的4列-用于测试模型）占20%的数据
#            y_test（测试集 目标变量的1列-对应X_test）y_test是对应的X_test测试集的数据的销售区间
# 举例，data表的数据集划分前（特征：价格、品牌、好评率、平均分。这里按训练集80%、测试集20%划分）（目标变量：销售区间）
# （这里仅举例2，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # | 价格  | 品牌| 好评率|平均分| 销量区间 |
    # | ---- | -- | ---- | --- | ---- |
    # | 1000 | A  | 0.95 | 4.5 | 中等销量 |
    # | 2000 | B  | 0.98 | 4.8 | 高销量  |
    # | 500  | A  | 0.90 | 4.2 | 低销量  |
    # | 3000 | C  | 0.99 | 4.9 | 超高销量 |
    # | 1500 | B  | 0.92 | 4.3 | 中等销量 |
    # | 800  | A  | 0.85 | 4.0 | 低销量  |
    # | 2500 | C  | 0.97 | 4.7 | 高销量  |
    # | 1200 | B  | 0.94 | 4.4 | 中等销量 |
    # | 2200 | C  | 0.96 | 4.6 | 高销量  |
    # | 4000 | B  | 0.99 | 4.9 | 超高销量 |
# 举例，假设random_state=42，随机划分结果如下：#训练集(80%)、#测试集(20%)
#   X_train训练集(80%)——用于训练模型     y_train训练集的目标变量
# （这里仅举例2，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # | 价格  | 品牌|好评率 |平均分              | 销量区间 |
    # | ---- | -- | ---- | ---               | ---- |
    # | 1000 | A  | 0.95 | 4.5               | 中等销量 |
    # | 2000 | B  | 0.98 | 4.8               | 高销量  |
    # | 500  | A  | 0.90 | 4.2               | 低销量  |
    # | 3000 | C  | 0.99 | 4.9               | 超高销量 |
    # | 1500 | B  | 0.92 | 4.3               | 中等销量 |
    # | 2500 | C  | 0.97 | 4.7               | 高销量  |
    # | 1200 | B  | 0.94 | 4.4               | 中等销量 |
    # | 2200 | C  | 0.96 | 4.6               | 高销量  |
#   X_test测试集(20%)——用于评估模型的性能  y_test测试集的目标变量
# （这里仅举例2，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
    # | 价格  | 品牌| 好评率|平均分              | 销量区间 |
    # | ---- | -- | ---- | ---               | ---- |
    # | 800  | A  | 0.85 | 4.0               | 低销量  |
    # | 4000 | B  | 0.99 | 4.9               | 超高销量 |
#       #变量含义
# X_train：训练集 特征数据的4列（价格、品牌、好评率、平均分）。
# X_test：测试集 特征数据的4列（价格、品牌、好评率、平均分）。
# y_train：训练集 目标变量的1列（销量区间）。
# y_test：测试集 目标变量的1列（销量区间）。
#       #通俗比喻
# 想象你有一堆水果，你想教别人如何区分苹果和橙子。你可以拿出80%的水果教别人（训练集），留下20%的水果来测试他们是否学会了（测试集）。
# train_test_split()函数，它就像是一个可以区分水果的工具，它帮你把100%数量的水果分为两份，
#                        一份80%数量用来训练你如何辨别水果，另一类20%数量用来测试你是否能正确的辨别水果。
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)






# 用随机森林模型，去训练 (X_train, y_train)训练集，得出训练结果random_forest_model   （模型训练——————烹饪和记录菜谱）
    # 调用RandomForestClassifier类，创建RandomForestClassifier()类的实例，作为random_forest_model对象（作为类的实例）
    # 调用random_forest_model对象（作为类的实例），用fit()函数（作用是进行实践操作模型，返回训练的结果）
#                                               使用训练集的4列 X_train 和 训练集的4列 y_train进行随机森林的模型训练，并得出训练结果
        #                                       结果是得到y_train的目标变量的1列(数据内容 是数值,例如'9916811'; 而不是文字例如'低销量') 和 y_train的目标变量的1列(数据内容 是数值,例如'9916811'; 而不是文字例如'低销量')，保存到random_forest_model对象
random_forest_model = RandomForestClassifier()
random_forest_model.fit(X_train, y_train)

# 保存 随机森林模型的训练结果random_forest_model 和 品牌编码器label_encoder 和 目标变量编码器target_encoder    （模型保存——————烹饪和记录菜谱）
    # 使用joblib库的dump函数，保存随机森林模型的训练结果random_forest_model对象到"random_forest_sales_model.joblib"文件。
    # 使用joblib库的dump函数，保存品牌标签编码器label_encoder对象到文件"brand_label_encoder.joblib"文件。
    # 使用joblib库的dump函数，保存目标变量标签编码器target_encoder对象到文件"target_label_encoder.joblib"文件。
dump(random_forest_model, "random_forest_sales_model.joblib") # 在用X_train训练集和y_train训练集的训练后，得出训练好的训练结果模型random_forest_model对象，随机森林模型保存为random_forest_sales_model.joblib
dump(brand_label_encoder, "brand_label_encoder.joblib")  # 在创建LabelEncoder类的实例LabelEncoder()后，用LabelEncoder类的fit_transform函数，用于对数据进行拟合和转换，得出品牌标签的拟合和转换结果brand_label_encoder对象，品牌标签编码保存为brand_label_encoder.joblib
dump(target_label_encoder, "target_label_encoder.joblib")  #  在创建LabelEncoder类的实例LabelEncoder()后，用LabelEncoder类的fit_transform函数，用于对数据进行拟合和转换，得出目标变量标签的拟合和转换结果target_label_encoder对象，品牌标签编码保存为target_label_encoder.joblib

# 评估 随机森林模型     （模型评估——————品尝和评分）
    # 使用训练好的随机森林模型random_forest_model对象，用perdict()函数（作用是进行预测评估模型，返回预测的结果），对测试集X_test进行预测，预测结果存储在random_forest_predictions对象。
    # 使用accuracy_score函数，进行计算目标变量和预测结果的差距（准确率），实际测试集的目标变量y_test 与 预测结果random_forest_predictions对象 ，两者之间的准确率计算后，返回准确率的计算结果random_forest_accuracy对象。
    # 打印随机森林模型的准确率的计算结果random_forest_accuracy对象。
random_forest_predictions = random_forest_model.predict(X_test) # 在用X_test测试集的测试后，得出测试好的测试结果（我的理解是"X_test_predictions"，这里实际写为了random_forest_predictions对象）
random_forest_accuracy = accuracy_score(y_test, random_forest_predictions) #在对比"y_test和X_test_predictions"后（即这里实际写为了y_test和random_forest_predictions），即accuracy_score()函数，计算目标变量和预测结果的差距（准确率），返回的计算结果为random_forest_accuracy对象。
print("随机森林模型的准确率：", random_forest_accuracy)    # 打印随机森林模型的准确率（即用accuracy_score(目标变量,预测结果)函数计算结果为random_forest_accuracy对象）。






# 用逻辑回归模型，去训练(X_train, y_train)训练集，得出训练结果logistic_regression_model      （模型训练——————烹饪和记录菜谱）
    # 调用LogisticRegression类，创建LogisticRegression()类的实例，作为logistic_regression_model对象（作为类的实例）
    # 调用logistic_regression_model对象（作为类的实例），用fit()函数（作用是进行实践操作模型，返回训练的结果）
#                                                     使用训练集的4列 X_train 和 训练集的4列 y_train，进行逻辑回归的模型训练，并得出训练结果
#                                                     结果是得到X_train的目标变量的1列(数据内容 是数值,例如'9916811'; 而不是文字例如'低销量') 和 y_train的目标变量的1列((数据内容 是数值,例如'9916811'; 而不是文字例如'低销量'))，保存到logistic_regression_model对象
logistic_regression_model = LogisticRegression()
logistic_regression_model.fit(X_train, y_train)

# 保存 逻辑回归模型的训练结果logistic_regression_model       （模型保存——————烹饪和记录菜谱）
# 使用joblib的dump函数，保存逻辑回归模型的训练结果logistic_regression_model到"logistic_regression_sales_model.joblib文件"。
dump(logistic_regression_model, "logistic_regression_sales_model.joblib") # 在用X_train训练集和y_train训练集的训练后，得出训练好的训练结果模型logistic_regression_model对象，逻辑回归模型保存为logistic_regression_sales_model.joblib

# 评估 逻辑回归模型     （模型评估——————品尝和评分）
    # 使用训练好的逻辑回归模型logistic_regression_model对象，用perdict()函数（作用是进行预测评估模型，返回预测的结果），对测试集X_test进行预测，预测结果存储在logistic_regression_predictions对象。
    # 使用accuracy_score函数，进行计算目标变量和预测结果的差距（准确率），实际测试集的目标变量y_test 与 预测结果logistic_regression_predictions对象，两者之间的准确率计算后，返回准确率的计算结果logistic_regression_accuracy对象。
    # 打印逻辑回归模型的准确率的计算结果logistic_regression_accuracy对象。
logistic_regression_predictions = logistic_regression_model.predict(X_test) # 在用X_test测试集的测试后，得出测试好的测试结果（我的理解是"X_test_predictions"，这里实际写为了logistic_regression_predictions对象）
logistic_regression_accuracy = accuracy_score(y_test, logistic_regression_predictions) #在对比"y_test和X_test_predictions"后（即这里实际写为了y_test和logistic_regression_predictions），即accuracy_score()函数，计算目标变量和预测结果的差距（准确率），返回的计算结果为logistic_regression_accuracy对象。
print("逻辑回归模型的准确率：", logistic_regression_accuracy)  # 打印逻辑回归模型的准确率（即用accuracy_score(目标变量,预测结果)函数计算结果为logistic_regression_accuracy对象）。









# Kimi详细解释（这里是 普通解释，如果看不懂，可以看下面的 Kimi通俗白话解释）
""""
好的，这份代码实现了一个基于机器学习的销售数据分析项目，旨在通过随机森林和逻辑回归模型对销售数据进行分类预测，
这份代码非常适合作为机器学习入门项目，涵盖了数据预处理、模型训练、评估和保存等关键步骤。以下是详细内容：

### 1. 引入库      ————导入库
- **pandas**：用于数据读取和预处理。
- **train_test_split函数**：将数据分为训练集和测试集。
- **RandomForestClassifier类 和 LogisticRegression类**：分别用于随机森林和逻辑回归模型。
- **LabelEncoder类**：将分类变量（如品牌、销量区间）转换为数值标签。
- **accuracy_score函数**：评估模型预测准确率。
- **dump函数**：保存训练好的模型和编码器。

### 2. 读取数据     ————读取result3整个文件
- 使用 `pd.read_csv()` 读取名为 "result3.csv" 的 CSV 文件。

### 3. 定义销量区间   ————把result3的（总评数列）划分为4列（低销量、中等销量、高销量、超高销量）
- 将“总评数”划分为四个区间：低销量、中等销量、高销量、超高销量。
- 使用 `pd.cut()` 实现分组。

### 4. 特征和目标变量选择    ————把result3的整个文件的其中4列（价格、品牌、好评率、平均分）挑选出来，同时创建1个新列（销售区间列）
- 特征列：价格、品牌、好评率、平均分。
- 目标变量列：sales_range（销量区间）。

### 5. 数据编码     ————把（品牌列）和（销售区间列）转换为数值标签
- 品牌和销量区间均转换为数值标签，便于模型处理。

### 6. 划分数据集    ————传入（价格、品牌、好评率、平均分）和（销售区间列）的数据，划分数据，数据分为训练集（80%）和测试集（20%）
- 数据分为训练集（80%）和测试集（20%），确保模型评估的客观性。

### 7. 模型训练与保存      ————传入x训练集，**模型**训练 x训练集 y训练集，得出x训练集的训练结果 y训练集的训练结果，保存为训练集的训练结果
- **随机森林模型**：适合处理非线性关系，对异常值不敏感。
- **逻辑回归模型**：适合线性分类问题，输出结果具有概率意义。
- 使用 `dump函数()` 保存模型和编码器，避免重复训练。

### 8. 模型评估     ————用训练集的训练结果模型，传入x测试集，得出x测试集的预测结果，把x测试集的预测结果 和 y测试集 对比计算，得出训练集结果模型的准确率
- 使用 `accuracy_score函数()` 计算预测准确率，直观评估模型性能。

整个流程展示了完整的机器学习项目实践，包括数据预处理、模型训练、保存和评估。
通过对比两种模型的准确率，可以选择更合适的模型进行销售数据预测。
这份代码具有较高的学习价值，适合初学者入门机器学习。
"""








# Kimi通俗白话解释（这里是超棒的 通俗白话解释，首先看完这个通俗白话解释建立一个印象，然后看上面的解释"xxx——————xxx"，同时结合上面的代码进行业务理解，如果中间有不懂的地方，可以回来看下面的这个通俗白话解释进行暂时补充。）
"""
以下是对你的注释进行优化后的版本，力求逻辑清晰、通俗易懂：

1. 引入库 —— 准备工具
    pandas：用于数据读取和预处理，就像厨房里的刀具一样，帮助我们切割和整理数据。
    train_test_split函数：将数据分为训练集和测试集，就像将食材分为两部分，一部分用来练习刀工，另一部分用来检验成果。
    RandomForestClassifier类 和 LogisticRegression类：分别是随机森林和逻辑回归模型，就像两种不同的厨具，适用于不同的烹饪任务。
    LabelEncoder类：将分类变量（如品牌、销量区间）转换为数值标签，就像将食材标准化处理，便于后续加工。
    accuracy_score函数：评估模型预测准确率，就像用品尝的方式来检验菜品的口味。
    dump函数：保存训练好的模型和编码器，就像把做好的菜谱保存下来，下次可以直接使用。

2. 读取数据 —— 获取食材
    使用 pd.read_csv() 读取名为 "result3.csv" 的 CSV 文件，就像从菜篮子里拿出我们要用的食材。

3. 定义销量区间 —— 切割食材
    将“总评数”划分为四个区间：低销量、中等销量、高销量、超高销量，就像把食材按大小分类，方便后续处理。
    使用 pd.cut() 实现分组。

4. 特征和目标变量选择 —— 挑选食材和调料
    从数据集中挑选出“价格”、“品牌”、“好评率”、“平均分”四列作为特征，就像挑选主要食材。
    创建一个新的列“sales_range”作为目标变量，就像确定我们要做的菜品类型。

5. 数据编码 —— 标准化处理
    将“品牌”和“sales_range”列转换为数值标签，就像将食材和调料统一成标准的切割和计量方式，方便模型处理。

6. 划分数据集 —— 分配食材
    将数据分为训练集（80%）和测试集（20%），就像把食材分为两部分，大部分用来练习，小部分用来检验成果。

7. 模型训练与保存 —— 烹饪和记录菜谱
    将训练集数据传入模型进行训练，随机森林模型适合处理复杂的、非线性的关系，而逻辑回归模型更适合线性的分类问题。
    使用 dump()函数 保存训练好的模型和编码器，就像把做好的菜谱和调料配方保存下来，避免重复劳动。

8. 模型评估 —— 品尝和评分
    使用训练好的模型对测试集进行预测，就像用练习好的厨艺来实际做菜。
    将预测结果与实际结果进行对比，计算出准确率，就像品尝菜品并给出评分。
    
通过以上的流程，我们完成了从数据读取、预处理、模型训练、保存到评估的完整过程。这个过程就像做一道菜，每一步都环环相扣，最终目的是为了得到一个美味的成果——一个能够准确预测销量区间的模型。希望这个比喻能帮助你更好地理解整个流程。
"""

