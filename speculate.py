# 用于加载之前训练好的模型和编码器，并对新的数据进行销量区间预测。
    # random_forest_sales_model.joblib  随机森林销售模型 文件
    # logistic_regression_sales_model   逻辑回归销售模型 文件
    # brand_label_encoder.joblib      品牌标签编码（编码器）文件
    # target_label_encoder.joblib     目标变量标签编码（编码器）文件

# 运行speculate.py后：
    # example_input = [1249.0, "vivo", 0.99, 5]
# 控制台会显示：
    # 预测的销量区间： ['中等销量']



# 导入joblib库load函数，用于加载之前保存的模型和编码器。
# 导入pandas库，用于数据处理。
from joblib import load
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# from buildmodel.build import brand_label_encoder, target_label_encoder


# 创建函数（定义一个函数：导入、创建、选择、编码）
# 定义一个名为Speculate的函数，输入参数是data，这是一个包含商品信息的列表。
# 加载 模型和标签编码器
#    这里加载了之前训练好的：
# 随机森林销售模型random_forest_sales_model.joblib为random_forest_model对象，用于销量区间预测
# 品牌标签编码brand_label_encoder.joblib为brand_label_encoder对象，用于品牌标签编码(数据编码/拟合和转换)
# 目标变量标签编码target_label_encoder.joblib为target_label_encoder对象，用于目标变量标签编码(数据编码/拟合和转换)
def Speculate(data):
    random_forest_model = load(BASE_DIR / "buildmodel/random_forest_sales_model.joblib")
    brand_label_encoder = load(BASE_DIR / "buildmodel/brand_label_encoder.joblib")
    target_label_encoder = load(BASE_DIR / "buildmodel/target_label_encoder.joblib")


    # 创建新数据（定义一个df的列和行）
    # 传入商品信息data，创建一个新的二维数据框架DataFrame，df是一种二维表格形式的数据结构，pd.df()赋值为new_data
    # data是一个列表，包含了所需要的值
    # pd.DataFrame()是一个二维数据框架，通过字典传入数据
    #               键，为列名，"价格", "品牌", "好评率", "平均分"
    #               值，为对应的列的数据列表，每个列的列表，都需要一个数组或列表形式的数据
    #                   这里例如，"价格":[data[0]] 表示一个"价格"的列，下面只包含一个元素的列表，这个元素就是 data 列表中的第一个元素
    #                   这里例如，"价格":[data[1]] 表示一个"品牌"的列，下面只包含一个元素的列表，这个元素就是 data 列表中的第二个元素
    #                   这里例如，"价格":[data[2]] 表示一个"好评率"的列，下面只包含一个元素的列表，这个元素就是 data 列表中的第三个元素
    #                   这里例如，"价格":[data[3]] 表示一个"平均分"的列，下面只包含一个元素的列表，这个元素就是 data 列表中的第四个元素
    # 最终，new_data就是一个df，即拥有四列（“价格”、“品牌”、“好评率”、“平均分”）和一行数据的DataFrame
    new_data = pd.DataFrame({
        "价格": [data[0]],
        "品牌": [data[1]],
        "好评率": [data[2]],
        "平均分": [data[3]]
    })


    # 特征选择和预处理（选择 特征和目标变量）
        # 指定特征列features多列：包含“价格”、“品牌”、“好评率”和“平均分”
    # 对new_data这个df，用copy()函数，创建副本为new_data_encoded这个df副本对象
        # new_data_encoded这个df副本对象，用于存储预处理后的数据
    features = ["价格", "品牌", "好评率", "平均分"]
    new_data_encoded = new_data.copy()



    # 品牌的标签编码（数据编码/拟合和转换）
    # 使用品牌标签编码器brand_label_encoder的transform函数，对new_data这个df副本对象的['品牌']列进行编码，
    # 将品牌名称列转换为(替换为)数值标签，并将结果存储在new_data_encoded这个df副本对象的“品牌”列中
        # 举例，品牌标签编码之前的data表的特征列features多列：（假设vivo是10011，oppo是10022，华为是10033，荣耀是10044，小米是10055）
        # （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
            # ['价格']  ['品牌']   ['好评率']  ['平均分']
            #   1000      vivo       0.91        4
            #   1500      oppo       0.92        5
            #   2000      华为        0.92        4
            #   3000      荣耀        0.93        5
            #   6000      小米        0.99        5
        # 举例，品牌标签编码之后的data表：
        # （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
            # ['价格']  ['品牌']   ['好评率']  ['平均分']
            #   1000     10011       0.91        4
            #   1500     10022       0.92        5
            #   2000     10033       0.92        4
            #   3000     10044       0.93        5
            #   6000     10055       0.99        5
    new_data_encoded['品牌'] = brand_label_encoder.transform(new_data['品牌'])


    # 预测（模型评估）
    # 使用随机森林模型random_forest_model，对预处理后的数据new_data_encoded这个df副本对象的features列，进行预测，预测结果存储在prediction对象中
        # 举例，目标变量标签预测之后（预处理前）的data表：
            #   features = ["价格", "品牌", "好评率", "平均分"]
            #   '销量区间'或'总评数'或'sales_range'编码的数值规定：（假设，按：低销量是9916811，中等销量是9916822，高销量是9916833，超高销量是9916844）
            #   '销量区间'或'总评数'或'sales_range'的数值范围对应的文字范围：（假设，按：0 - 1000分为低销量, 1000-5000分为中等销量, 5000-10000分为高销量, 10000+分为超高销量）（左开右合）
        # （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
            # ['价格']  ['品牌']   ['好评率']  ['平均分']         ['总评数'/销量']     ['features' 根据 '总评数'，predict前，得出 目标变量标签/'销量区间'/'sales_range']
            #   1000      10011       0.91        4               500
            #   1500      10022       0.92        5               1024
            #   2000      10033       0.92        4               1500
            #   3000      10044       0.93        5               6000
            #   6000      10055       0.99        5               10000
        #  举例，目标变量标签预测之后（预处理后）的data表：
        # （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
            # ['价格']  ['品牌']   ['好评率']  ['平均分']          ['总评数'/'销量']    ['features' 根据 '总评数'，predict后，得出 目标变量标签/'销量区间'/'sales_range']
            #   1000      10011       0.91        4               500                9916811
            #   1500      10022       0.92        5               1024               9916822
            #   2000      10033       0.92        4               1500               9916822
            #   3000      10044       0.93        5               6000               9916833
            #   6000      10055       0.99        5               10000              9916844
        #   结论返回(数据内容 是数值, 例如'9916811'; 而不是文字例如'低销量')
    prediction = random_forest_model.predict(new_data_encoded[features])


    # 将预测结果映射回销量区间（数据编码/反_拟合和转换）
    # 使用目标变量标签编码器target_label_encoder的inverse_transform函数（反_拟合和转换）
        # 函数区别说明：
            # transform()拟合和转换："文字" 替换为转换为 "数值编码" （例如："低销量" 替换为转换为 "9916811" ）
            # inverse_transform反_拟合和转换："数值编码" 替换为转换为 "文字" （例如："9916811" 替换为转换为 "低销量" ）
    # 将预测结果prediction映射回原始的销量区间标签，并将结果存储在predicted_sales_range
        # 举例，目标变量标签编码之前（反_拟合和转换前）的data表：
        #   features = ["价格", "品牌", "好评率", "平均分"]
        #   '销量区间'或'总评数'或'sales_range'编码的数值规定：（假设，按：低销量是9916811，中等销量是9916822，高销量是9916833，超高销量是9916844）
        #   '销量区间'或'总评数'或'sales_range'的数值范围对应的文字范围：（假设，按：0 - 1000分为低销量, 1000-5000分为中等销量, 5000-10000分为高销量, 10000+分为超高销量）（左开右合）
        # （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
            # ['价格']  ['品牌']   ['好评率']  ['平均分']          ['总评数'/'销量']    ['features' 根据 '总评数'，predict后，得出 目标变量标签/'销量区间'/'sales_range']
            #   1000      10011       0.91        4               500                9916811
            #   1500      10022       0.92        5               1024               9916822
            #   2000      10033       0.92        4               1500               9916822
            #   3000      10044       0.93        5               6000               9916833
            #   6000      10055       0.99        5               10000              9916844
        # 举例，目标变量标签编码之前（反_拟合和转换后）的data表：
        # （这里仅举例，方便理解学习，以下例子数值与实际的result3.csv的data无关，实际运行结果以输入实际的result3.csv的data数据为准）
            # ['价格']  ['品牌']   ['好评率']  ['平均分']          ['总评数'/'销量']    ['features' 根据 '总评数'，predict后，得出 目标变量标签/'销量区间'/'sales_range']
            #   1000      10011       0.91        4               500                低销量
            #   1500      10022       0.92        5               1024               中等销量
            #   2000      10033       0.92        4               1500               中等销量
            #   3000      10044       0.93        5               6000               高销量
            #   6000      10055       0.99        5               10000              超高销量
        #   结论返回(数据内容 是文字例如'低销量'; 而不是数值, 例如'9916811')
    predicted_sales_range = target_label_encoder.inverse_transform(prediction)


    # 打印预测结果
    #打印预测的销售区间，返回预测的销售区间
    print("预测的销量区间：", predicted_sales_range)
    return predicted_sales_range


    # 定义一个示例，示例输入数据：[价格, 品牌, 好评率, 平均分]，赋值给example_input对象
    # 调用 Speculate 函数，传入示例数据 example_input，进行销量区间预测，并将结果存储在 predicted_range 中。
if __name__ == '__main__':
    example_input = [1249.0, "vivo", 0.99, 5]
    predicted_range = Speculate(example_input)




#（本篇总结）
# 本篇代码/这段代码的主要功能是：
# 定义一个函数
    # 加载之前训练好的模型和编码器。
    # 对新的商品数据进行预处理。
    # 使用随机森林模型进行销量区间预测。
    # 将预测结果映射回原始的销量区间标签。
    # 打印并返回预测结果。
# 输入新的商品数据，调用函数，快速预测其销量区间。
